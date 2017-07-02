import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string
from twython import Twython

import pygame
from pygame.locals import *
pygame.init()
WIDTH = 800
HEIGHT = 600
windowSurface = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)


########################
#
# Behaviour Variables
#
########################
num_frame = 8       # Number of frames in Gif
gif_delay = 15      # Frame delay [ms]
rebound = True      # Create a video that loops start <=> end
tweet = False       # Tweets the GIF after capturing


########################
#
# Twitter (Optional)
# Ensure 'tweet' behaviour-variable is True if you want to tweet pictures.
#
########################
APP_KEY = 'YOUR API KEY'
APP_SECRET = 'YOUR API SECRET'
OAUTH_TOKEN = 'YOUR ACCESS TOKEN'
OAUTH_TOKEN_SECRET = 'YOUR ACCESS TOKEN SECRET'

#setup the twitter api client
twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


########################
#
# Define GPIO
#
########################
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

button = 24 #Button GPIO Pin
GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_UP)
led_1 = 4 #Status LED GPIO Pin
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
camera.resolution = (800, 600)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
##GPIO.output(led_2, 1)

# Indicate ready status
buttonLed.start(100)
statusLed.start(0)


img = pygame.image.load("home.png")
windowSurface.blit(img, (0, 0))
pygame.display.flip()


print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

def tweet_pics():
    try:
        print('Posting to Twitter')
        photo = open(filename + ".gif", 'rb')
        response = twitter.upload_media(media=photo)
        twitter.update_status(status='Taken with #PIX-E Gif Camera', media_ids=[response['media_id']])
    except:
        # Display error with long status light
        statusLed.ChangeDutyCycle(100)
        buttonLed.ChangeDutyCycle(0)
        sleep(2)
        

try:
    while True:
        if GPIO.input(button) == False: # Button Pressed
        
            img = pygame.image.load("in 3 seconds.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(3)
            
            img = pygame.image.load("ready.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(1)
            
            img = pygame.image.load("3.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(1)
                        
            img = pygame.image.load("2.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(1)
                        
            img = pygame.image.load("1.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(1)
                        
            img = pygame.image.load("shooting.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()
            time.sleep(1)

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

            img = pygame.image.load("processing.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()


            graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
            os.system(graphicsmagick)
            os.system("rm ./*.jpg") # cleanup source images

            ### TWEETING ###
            if tweet == True:
                statusLed.ChangeDutyCycle(25)
                buttonLed.ChangeDutyCycle(0)
                tweet_pics()
            
            print('Done')

            img = pygame.image.load("done.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()


            print('System Ready')
            img = pygame.image.load("home.png")
            windowSurface.blit(img, (0, 0))
            pygame.display.flip()


        else : # Button NOT pressed
            ### READY TO MAKE GIF ###
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(100)
            sleep(0.05)
           
except:
    GPIO.cleanup()
