#Gifcam Code for PIX-E Gif Camera

######A DIY Raspberry Pi Zero based camera:
- Creates animated gifs
- Optionally can post gifs to twitter or save directly to usb

##3D Printer Files:
- Download Here - http://www.thingiverse.com/thing:1761082

##This requires:
  - PiCamera -- http://picamera.readthedocs.org/ 
  - Gitcore
  - GraphicsMagick -- http://www.graphicsmagick.org/
  - (Optional) twython -- https://github.com/ryanmcgrath/twython

##Steps:
  - Run -- sudo apt-get update
  - Run -- sudo apt-get upgrade
  - Install PiCamera -- sudo apt-get install python-picamera
  - Install GraphicsMagick -- sudo apt-get install graphicsmagick
  - Install Gitcore -- sudo apt-get install git-core
  - Install GifCam -- sudo git clone https://github.com/nickbrewer/gifcam.git
  - Optional, Install twython -- https://github.com/ryanmcgrath/twython
  - Optional, install mount USB - http://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/

##Create Autorun Script:
  - Run -- sudo crontab -e
  - add this line to end of that file - @reboot sh /home/pi/gifcam/launcher.sh
  
  (The launcher.sh in this git is setup for the basic gifcam, if you want to use twython or USB you'll have to modify this)
  
##Permissions:
  - If hitting "permission denied" run - sudo chown -R pi /home/pi/gifcam/


  
