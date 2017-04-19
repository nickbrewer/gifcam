## Features
- Creates a GIF at the press of a button and saves it locally
- Optionally tweet the created GIF
- The GIF can be made to run START => END or "rebound" START <=> END
- Status LEDs keep the user informed as to what's going on

## How To Use the Camera
- Power on the camera.
- The button will illuminate when the camera is ready to make a GIF.
- When you press the button, the button LED will strobe to indicate that the camera is recording.
- When recording finishes, the button LED will switch off.
- The status LED will blink while the GIF is being processed (and optionally, tweeted)
- When processing is finished, the camera will return to the READY state, and the button LED will illuminate.

## ToDo:
- working directory referencing, this is so you can cleanup source images with: `rm $workingDir/\*.jpg` rather than from within the repo main directory
- samba shared folder to pull images off over wifi (Pi Zero W)
- smart twitter handling for when gifs are taken and you're not on wifi? If an image upload fails it gets pushed onto a re-attempt stack, which attempts to pop each time a gif is taken / an upload button pressed!

## 3D Printer Files:
- Download Here - http://www.thingiverse.com/thing:1761082

## This requires:
  - PiCamera -- http://picamera.readthedocs.org/ 
  - Gitcore
  - GraphicsMagick -- http://www.graphicsmagick.org/
  - (Optional) twython -- https://github.com/ryanmcgrath/twython

## Steps:
  - Run -- sudo apt-get update
  - Run -- sudo apt-get upgrade
  - Install PiCamera -- sudo apt-get install python-picamera
  - Install GraphicsMagick -- sudo apt-get install graphicsmagick
  - Install Gitcore -- sudo apt-get install git-core
  - Install GifCam -- sudo git clone https://github.com/nickbrewer/gifcam.git
  - Optional, Install twython -- https://github.com/ryanmcgrath/twython
  - Optional, install mount USB - http://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/

## Create Autorun Script:
  - Run -- sudo crontab -e
  - add this line to end of that file - @reboot sh /home/pi/gifcam/launcher.sh
  
  (The launcher.sh in this git is setup for the basic gifcam, if you want to use twython or USB you'll have to modify this)
  
## Permissions:
  - If hitting "permission denied" run - sudo chown -R pi /home/pi/gifcam/


  
