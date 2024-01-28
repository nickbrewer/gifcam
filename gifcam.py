from picamera2 import Picamera2
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string
import imageio
import toml
from mastodon import Mastodon
from concurrent.futures import ThreadPoolExecutor
from libcamera import ColorSpace
import numpy as np
import threading
from picamera2.encoders import H264Encoder, Quality
from picamera2.outputs import FileOutput
import shutil
import subprocess

#  Config
with open('config.toml', 'r') as file:
  config = toml.load(file)

# Gif Config
gif_config = config.get('gif', {})
num_frame = gif_config.get('num_frame')
gif_delay = gif_config.get('delay')
rebound = gif_config.get('rebound')
resolution = gif_config.get('resolution')

# Bereal Config
bereal_config = config.get('bereal', {})

# Mastodon Config
mastodon_config = config.get('mastodon', {})
access_token = mastodon_config.get('access_token')
server = mastodon_config.get('server')
mastodon_status = mastodon_config.get('status')
mastodon = Mastodon(
    access_token=access_token,
    api_base_url=server
)

########################
#
# Define GPIO
#
########################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 19 #Button GPIO Pin
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led_1 = 21 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
buttonLed = GPIO.PWM(led_1, 10)
#led_2 = 21 #ON/OFF LED Pin
#GPIO.setup(led_2, GPIO.OUT)
#statusLed = GPIO.PWM(led_2, 2)


########################
#
# Camera
#
########################
color_space = ColorSpace.Rec2020()
camera = Picamera2()
camera_config = camera.create_still_configuration(main={"size": resolution}, colour_space=color_space)
stream_config = {"size" : (640, 480)}
vid_config = camera.create_video_configuration(stream_config)
camera.configure(vid_config)
camera.start()

import os
import shutil

def transcode_h264_to_mp4(input_file, output_file):
    # Use FFmpeg to transcode the H.264 stream to MP4
    subprocess.run([
        'ffmpeg', '-y',  '-i', input_file, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental', output_file
    ], check=True)


def capture_preview():
    while True:
        # Start a new recording
        with open('/home/tom/gifcam/static/stream/preview_stream.h264', 'wb') as stream_file:
            output = FileOutput(stream_file)
            camera.start_recording(encoder=H264Encoder(), output=output)
            try:
                # Wait for 10 seconds
                time.sleep(10)
            finally:
                # Stop the recording
                camera.stop_recording()
                # Transcode the H.264 stream to MP4
                transcode_h264_to_mp4('/home/tom/gifcam/static/stream/preview_stream.h264', '/home/tom/gifcam/static/stream/preview_stream.mp4')
                # Delete the existing preview_stream.h264 file
                os.remove('/home/tom/gifcam/static/stream/preview_stream.h264')
                # Create a new empty preview_stream.h264 file for the next recording
                with open('/home/tom/gifcam/static/stream/preview_stream.h264', 'wb'):
                    pass



preview_thread = threading.Thread(target=capture_preview)
preview_thread.start()
#camera.resolution = (800, 800)
#camera.rotation = 90
#camera.brightness = 70
#camera.image_effect = 'none'
##GPIO.output(led_2, 1)

# Indicate ready status
buttonLed.start(100)
#statusLed.start(0)

print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def load_image(file):
    image = imageio.imread(file)
    return np.rot90(image, k=1, axes=(0, 1))

def post_to_bereal():
  pass

def post_to_mastodon(file):
  try:
    print("Posting to Mastodon")
    #sleep(60)
    media_ids = mastodon.media_post(file, mime_type='image/gif')
    sleep(30)
    print(mastodon.status_post(mastodon_status, media_ids=media_ids))
  except Exception as e:
    print(e)
    # Display error with long status light
    #statusLed.ChangeDutyCycle(100)
    buttonLed.ChangeDutyCycle(0)
    sleep(2)

try:
    while True:
        if GPIO.input(button) == False: # Button Pressed
            ### TAKING PICTURES ###
            print('Gif Started')
            #statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(50)

            randomstring = random_generator()
            print(f"Capturing {num_frame} frames")
            for i in range(num_frame):
                print(f"Capturing {i}")
                camera.capture_file('{0:04d}.jpg'.format(i))

            ### PROCESSING GIF ###
            #statusLed.ChangeDutyCycle(50)
            buttonLed.ChangeDutyCycle(0)
            if rebound == True: # make copy of images in reverse order
                for i in range(num_frame - 1):
                    source = str(num_frame - i - 1) + ".jpg"
                    source = source.zfill(8) # pad with zeros
                    dest = str(num_frame + i) + ".jpg"
                    dest = dest.zfill(8) # pad with zeros
                    copyCommand = "cp " + source + " " + dest
                    os.system(copyCommand)

            filename = '/home/tom/gifcam/gifs/' + randomstring + '-0.gif'
            input_dir = "/home/tom/gifcam/"
            files = sorted([os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith(".jpg")])
            images = []
            # Use ThreadPoolExecutor to load images in parallel
            with ThreadPoolExecutor() as executor:
              images = list(executor.map(load_image, files))
            #for file in files:
            #  images.append(imageio.imread(file))

            imageio.mimsave(filename, images, duration=0.1)
            print('Processing')
            #graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
            #os.system(graphicsmagick)
            os.system("rm ./*.jpg") # cleanup source images

            ### TWEETING ###
            if bereal_config.get('enabled'):
                #statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                post_to_bereal()
            if mastodon_config.get('enabled'):
                #statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                post_to_mastodon(filename)

            print('Done')
            print('System Ready')

        else : # Button NOT pressed
            ### READY TO MAKE GIF ###
            #statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(100)
            sleep(0.05)
           
except Exception as e:
    print(e)
    GPIO.cleanup()
