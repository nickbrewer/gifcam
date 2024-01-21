import requests
import pickle
import os
import geocoder
import base64
import json
import time

import socket
import http.server
import socketserver
import threading

class HttpOTPServer:
    def __init__(self, callback, port=8090):
        self.callback = callback
        self.port = port

    def start_server(self):
        class OTPRequestHandler(http.server.BaseHTTPRequestHandler):
            def do_GET(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write("""
                    <html>
                    <body>
                    <form method="post">
                    OTP Code: <input type="text" name="otp">
                    <input type="submit" value="Submit">
                    </form>
                    </body>
                    </html>
                """.encode())

            def do_POST(self):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                otp = post_data.split("=")[1]
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(f"""
                    <html>
                    <body>
                    <h1>Submitted OTP: {otp}</h1>
                    </body>
                    </html>
                """.encode())
                self.server.callback(otp)
                self.server.shutdown()

        ip_address = '0.0.0.0'
        self.server = socketserver.TCPServer((ip_address, self.port), OTPRequestHandler)
        threading.Thread(target=self.server.serve_forever).start()
        return f"http://{ip_address}:{self.port}"


class BeReal:

  DEFAULT_API_URL = "https://berealapi.fly.dev"

  def __init__(self, phone_number, api_url=None):
    self.phone_number = phone_number
    self.otp_session = None
    self.jwt_token = None
    if (api_url):
      self.base_url = api_url
    else:
      self.base_url = self.DEFAULT_API_URL
    self.load_state() # Load existing JWT variables

  def authenticate(self):
    response = self.send_code()
    if response.status_code == 201:
      self.verify(input("OTP: "))
      #otp_server = HttpOTPServer(self.verify)
      #otp_url = otp_server.start_server()
      #print(f"Visit {otp_url} in your web browser to enter the OTP.")
    else:
      error_msg = f"Failed to authenticate: {response.text}"
      print(error_msg)
      Exception(error_msg)


  def ping(self):
    pass

  def send_code(self, vonage=False):
    endpoint = "/login/send-code"
    url = self.base_url + endpoint
    data = {
      "phone": self.phone_number
    }
    response = requests.post(url, json=data)
    if (response.status_code == 201):
      response_json = response.json()
      self.otp_session = response_json["data"]["otpSession"]
    else:
      error_msg = f"Failed to send OTP: {response.text}"
      print(error_msg)
      Exception(error_msg)
    return response

  def verify(self, otp_code, vonage=False):
    endpoint = "/login/verify"
    url = self.base_url + endpoint
    data = {
      "code" : otp_code,
      "otpSession" : self.otp_session
    }
    response = requests.post(url, json=data)
    if (response.status_code == 201):
      response_json = response.json()
      self.jwt_token = response_json["data"]["token"]
      self.save_state() # Save new JWT Token to state
    else:
      error_msg = f"Failed to verify OTP: {response.text}"
      print(error_msg)
      Exception(error_msg)

    return response

  def refresh(self):
    try:
      endpoint = "/login/refresh"
      url = self.base_url + endpoint
      data = {
        "token": self.jwt_token
      }
      response = requests.post(url, json=data)
      if (response.status_code == 201):
        response_json = response.json()
        self.jwt_token = response_json["data"]["token"]
        self.save_state() # Save new JWT Token to state
      else:
        error_msg = f"Failed to refresh token: {response.text}"
        Exception(error_msg)
    except:
      self.authenticate() # reauthenticate
    return response

  def post_comment(self):
    pass

  def delete_comment(self):
    pass

  def get_upload_tokens(self):
    print("Getting upload tokens")
    endpoint = "/post/upload/getData"
    url = self.base_url + endpoint
    headers = {"accept": "application/json", "token": self.jwt_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
       return response.json()["data"]
    else:
       error_msg = f"Failed to get upload tokens. Status code: {response.status_code}. Response: {response.text}"
       raise Exception(error_msg)

  def upload_photo(self, token_data, img_path, resize=False):
    print("Uploading photos")
    endpoint = "/post/upload/photo"
    url = self.base_url + endpoint
    headers = {"token": self.jwt_token, "Authorization": f"Bearer {self.jwt_token}"}

    with open(img_path, "rb") as img_file:
      files = {"img": img_file}
      data = {
        "tokenData": token_data,
        "resize": resize
      }
      response = requests.put(url, headers=headers, files=files, data=data)
      if response.status_code == 201:
          print(response.json())
          return response.json()
      else:
          error_msg = f"Failed to upload photo. Status code: {response.status_code}. Response: {response.text}"
          raise Exception(error_msg)

  def upload_post_data(self, post_data, token_data):
    print("Uploading post")
    endpoint = "/post/upload/data"
    url = self.base_url + endpoint
    headers = {"token": token_data, "accept": "application/json"}
    data = {"postData": post_data, "tokenData": self.jwt_token}
    response = requests.post(url, headers=headers,  data=data)
    if response.status_code == 200:
        return response.json()
    else:
       error_msg = f"Failed to upload post data. Status code: {response.status_code}. Response: {response.text}"
       print(error_msg)
       raise Exception(error_msg)


  def get_feed(self):
    pass

  def get_friends_of_friends(self):
    pass

  def get_info(self):
    pass

  def me(self):
    pass

  def get_memories(self):
    pass

  def save_state(self):
    os.makedirs("bereal_states", exist_ok=True)
    filename = f"bereal_states/{self.phone_number}.pickle"
    with open(filename, "wb") as file:
      pickle.dump(self, file)

  def load_state(self):
    filename = f"bereal_states/{self.phone_number}.pickle"
    if os.path.exists(filename):
      with open(filename, "rb") as file:
        obj = pickle.load(file)
        self.phone_number = obj.phone_number
        self.otp_session = obj.otp_session
        self.jwt_token = obj.jwt_token

  def get_latlng(self):
    print(geocoder.ip('me').latlng)
    return geocoder.ip('me').latlng
