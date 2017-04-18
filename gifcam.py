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
led_2 = 21 #ON/OFF LED Pin
GPIO.setup(led_2, GPIO.OUT)

########################
### Variables Config ###
########################
num_pics = 8        # Number of pictures to take in Gif
gif_delay = 15      # How much delay in between those pictures (in milliseconds)
boomerang = True    # create a video that loops start <=> end

camera = picamera.PiCamera()
camera.resolution = (540, 405)
camera.rotation = 90
#camera.brightness = 70
camera.image_effect = 'none'
GPIO.output(led_2, 1)
print('System Ready')

def random_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for x in range(size))

while True:
    input_state = GPIO.input(button) # Sense the button
    randomstring = random_generator()
    if input_state == False:
        GPIO.output(led_1, 1)
        print('Gif Started')
        for i in range(num_pics):
            camera.capture('{0:04d}.jpg'.format(i))

        if boomerang == True: # make copy of images in reverse order
            for i in range(num_pics - 1):
                source = str(num_pics - i - 1) + ".jpg"
                source = source.zfill(8) # pad with zeros
                dest = str(num_pics + i) + ".jpg"
                destpad = dest.zfill(8) # pad with zeros
                copyCommand = "cp " + source + " " + destpad
                os.system(copyCommand)
                
        filename = '/home/pi/gifcam/gifs/' + randomstring + '-0'
        GPIO.output(led_1, 0)
        print('Processing')
        graphicsmagick = "gm convert -delay " + str(gif_delay) + " " + "*.jpg " + filename + ".gif" 
        os.system(graphicsmagick)
        os.system("rm ./*.jpg") # cleanup source images
        print('Done')
        print('System Ready')
    else :
        # Switch on LED
        GPIO.output(led_1, 1)
        time.sleep(0.35)
        GPIO.output(led_1, 0)
        time.sleep(0.35)
        
       
