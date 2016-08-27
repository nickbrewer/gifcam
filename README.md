#Gifcam Code for Pix-E LoFi Gif Camera

##A DIY Raspberry Pi based camera that:
- Creates animated gifs
- Optionally can post gifs to twitter

##This requires:
  - PiCamera -- http://picamera.readthedocs.org/ 
  - Gitcore
  - GraphicsMagick -- http://www.graphicsmagick.org/
  - (Optional) twython -- https://github.com/ryanmcgrath/twython

##Steps:
  - Install PiCamera -- sudo apt-get install python-picamera
  - Install GraphicsMagick -- sudo apt-get install graphicsmagick
  - Install Gitcore -- sudo apt-get install git-core
  - Optional, Install twython -- https://github.com/ryanmcgrath/twython
  - Create Autorun Script - http://www.instructables.com/id/Raspberry-Pi-Launch-Python-script-on-startup/
  
  (The launcher.sh in this git is setup for the basic gifcam, if you want to use twython you'll have to modify this)
  
