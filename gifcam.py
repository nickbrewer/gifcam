import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string
import toml

########################
#
# Behaviour Variables
#
########################
#num_frame = 20       # Number of frames in Gif
#gif_delay = 5      # Frame delay [ms]
#rebound = True      # Create a video that loops start <=> end
#tweet = False       # Tweets the GIF after capturing


########################
#
# Mastodon (Optional)
# Ensure 'post' behaviour-variable is True if you want to tweet pictures.
#
########################
APP_KEY = 'YOUR API KEY'
APP_SECRET = 'YOUR API SECRET'
OAUTH_TOKEN = 'YOUR ACCESS TOKEN'
OAUTH_TOKEN_SECRET = 'YOUR ACCESS TOKEN SECRET'

#  Config
with open('config.toml', 'r') as file:
  config = toml.load(file)

# Gif Config
gif_config = config.get('gif', {})
num_frame = gif_config.get('num_frame')
gif_delay = gif_config.get('delay')
rebound = gif_config.get('rebound')

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
led_1 = 12 #Status LED GPIO Pin
GPIO.setup(led_1, GPIO.OUT)
buttonLed = GPIO.PWM(led_1, 10)
led_2 = 21 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)
statusLed = GPIO.PWM(led_2, 2)


########################
#
# Camera
#
########################
camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
##GPIO.output(led_2, 1)

# Indicate ready status
buttonLed.start(100)
statusLed.start(0)

print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def post_to_bereal():
  pass

def post_to_mastodon():
    try:
      print("Posting to Mastodon")
      media_ids = mastodon.media_post(filename, mime_type='image/gif')
      mastodon.status_post(mastodon_status, media_ids=media_ids)
   except:
      # Display error with long status light
      statusLed.ChangeDutyCycle(100)
      buttonLed.ChangeDutyCycle(0)
      sleep(2)

try:
    while True:
        if GPIO.input(button) == False: # Button Pressed
            ### TAKING PICTURES ###
            print('Gif Started')
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(50)

            randomstring = random_generator()
            for i in range(num_frame):
                camera.capture('{0:04d}.jpg'.format(i))

            ### PROCESSING GIF ###
            statusLed.ChangeDutyCycle(50)
            buttonLed.ChangeDutyCycle(0)
            if rebound == True: # make copy of images in reverse order
                for i in range(num_frame - 1):
                    source = str(num_frame - i - 1) + ".jpg"
                    source = source.zfill(8) # pad with zeros
                    dest = str(num_frame + i) + ".jpg"
                    dest = dest.zfill(8) # pad with zeros
                    copyCommand = "cp " + source + " " + dest
                    os.system(copyCommand)
                    
            filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
            print('Processing')
            graphicsmagick = "gm convert -delay " + str(gif_delay)) + " " + "*.jpg " + filename + ".gif" 
            os.system(graphicsmagick)
            os.system("rm ./*.jpg") # cleanup source images

            ### TWEETING ###
            if bereal_config.get('enabled'):
                statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                post_to_bereal()
            if mastodon_config.get('enabled'):
                statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                post_to_mastodon()

            print('Done')
            print('System Ready')

        else : # Button NOT pressed
            ### READY TO MAKE GIF ###
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(100)
            sleep(0.05)
           
except:
    GPIO.cleanup()
