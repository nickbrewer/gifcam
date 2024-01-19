import requests
import pickle
import os
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
    if (response.status_code == 201):
      response_json = response.json()
      #self.otp_session = response_json["data"]["otpSession"]["otpSesion"]
      self.verify(input("OTP Code: "))
    else:
      print("Error sending OTP Code")

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
      print(response.text)
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
      print(response.text)
    return response

  def refresh(self):
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
      print(response.text)
    return response

  def post_comment(self):
    pass

  def delete_comment(self):
    pass

  def get_upload_tokens(self):
    endpoint = "/post/upload/getData"
    url = self.base_url + endpoint
    headers = {"accept": "application/json", "token": self.jwt_token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
       return response.json()["data"]
    else:
       error_msg = f"Failed to get upload tokens. Status code: {response.status_code}. Response: {response.text}"
       raise Exception(error_msg)

  def upload_photo(self, token_data, img_path, resize=True):
    endpoint = "/post/upload/photo"
    url = self.base_url + endpoint
    headers = {"token": self.jwt_token}
    files = {"img": open(img_path, "rb")}
    data = {"tokenData": token_data, "resize": resize}
    response = requests.put(url, headers=headers, files=files, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        error_msg = f"Failed to upload photo. Status code: {response.status_code}. Response: {response.text}"
        raise Exception(error_msg)
  
  def upload_post_data(self, post_data, token_data):
    endpoint = "/post/upload/data"
    url = self.base_url + endpoint
    headers = {"token": self.jwt_token}
    data = {"postData": post_data, "tokenData": token_data}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        return response.json()
    else:
       error_msg = f"Failed to upload post data. Status code: {response.status_code}. Response: {response.text}"
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
