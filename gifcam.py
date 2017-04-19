import picamera
from time import sleep
import time
import RPi.GPIO as GPIO
from os import system
import os
import random, string

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
### Variables Config ###
########################
num_pics = 8        # Number of pictures to take in Gif
gif_delay = 15      # How much delay in between those pictures (in milliseconds)
rebound = True      # create a video that loops start <=> end

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

try:
    while True:
        input_state = GPIO.input(button) # Sense the button
        
        if input_state == False:

            ### TAKING PICTURES ###
            print('Gif Started')
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(50)

            randomstring = random_generator()
            for i in range(num_pics):
                camera.capture('{0:04d}.jpg'.format(i))

            ### PROCESSING PICTURES ###
            statusLed.ChangeDutyCycle(50)
            buttonLed.ChangeDutyCycle(0)
            if rebound == True: # make copy of images in reverse order
                for i in range(num_pics - 1):
                    source = str(num_pics - i - 1) + ".jpg"
                    source = source.zfill(8) # pad with zeros
                    dest = str(num_pics + i) + ".jpg"
                    dest = dest.zfill(8) # pad with zeros
                    copyCommand = "cp " + source + " " + dest
                    os.system(copyCommand)
                    
            filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
            print('Processing')
            graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
            os.system(graphicsmagick)
            os.system("rm ./*.jpg") # cleanup source images
            print('Done')
            print('System Ready')

        else :
            ### READY TO TAKE PICTURES ###
            statusLed.ChangeDutyCycle(0)
            buttonLed.ChangeDutyCycle(100)
            
           
except:
    GPIO.cleanup()
