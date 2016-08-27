import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import shutil
from twython import Twython

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
button = 26 #Button GPIO Pin
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led = 21 #LED GPIO Pin
GPIO.setup(led, GPIO.OUT)

########################
### Variables Config ###
########################
num_pics = 8 #Number of pictures to take in Gif
gif_delay = 15 #How much delay in between those pictures (in milliseconds)

APP_KEY = 'OqzPbTq3Ms0h3LXOE2Mh4EbDr'
APP_SECRET = 'dTrgSZaNf7ik9KCresmwGQZJ3Y6x3j74HAXQ3J6KAsqWKBbSzb'
OAUTH_TOKEN = '15090610-Wu9x4Xj03ClefFoCLSgo48K9eV2UKuj7KMNHuaNbr'
OAUTH_TOKEN_SECRET = 'kHsvgnEpO7JVPuvB3JhJE0DnQZHeWo0B9lfryBWc7Vg56'

#setup the twitter api client
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def tweet_pics():
    print('Posting to Twitter')
    photo = open(filename + ".gif", 'rb')
    response = twitter.upload_media(media=photo)
    twitter.update_status(status='Taken with #Pix-E LoFi Gif Camera', media_ids=[response['media_id']])     

camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
print('System Ready')

while True:
    input_state = GPIO.input(button) # Sense the button 
    now = time.strftime("%Y%m%d%H%M%S")
    if input_state == False:
    	# Switch off LED
        GPIO.output(led, 1)
        print('Gif Started')
        for i in range(num_pics):
    		camera.capture('image{0:04d}.jpg'.format(i))
        filename = '/home/pi/photos/gifs/' + now + '-0'
        GPIO.output(led, 0)
    	print('Processing')
        graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
        os.system(graphicsmagick)
        tweet_pics()
        print('Done')
    else :
        # Switch on LED
        GPIO.output(led, 1)
        time.sleep(0.35)
        GPIO.output(led, 0)
        time.sleep(0.35)
        
       