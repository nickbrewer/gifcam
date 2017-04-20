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

## Change Camera Behaviour
The behaviour of the camera is controlled by a few _Behaviour Variables_. These are in `gifcam.py`.
With these variables you can change the frame-number and time duration of gifs, and control tweeting behaviour.
- `tweet = True/False` Enables or Disables an automatic tweet of the captured gif. This significantly increases the time needed in between GIF captures.
- `num_frame` Sets the number of frames in the gif
- `gif_delay` Sets the number of milliseconds a frame is displayed in the gif.
- `rebound = True/False` Create a gif that loops start <=> end

For now these variables are programmed into the script, but it would be trivial to connect extra switches to your Pi that control these variables. Perhaps a rotary switch to select frame number, and sliding switches to control rebound and tweet behaviour.

## 3D Printer Files:
- Download Here - http://www.thingiverse.com/thing:1761082

## Minimum Requirements:
  - PiCamera -- http://picamera.readthedocs.org/ 
  - Gitcore
  - GraphicsMagick -- http://www.graphicsmagick.org/
  - (Optional) twython -- https://github.com/ryanmcgrath/twython

## Basic Setup (if you already have a working Pi):
Detailed steps on how to get your Pi Zero W up and running without a keyboard, monitor or mouse are covered at the bottom of this text, in the _In-Depth Instructions_
Here I'm assuming we're starting with a clean install of Raspbian Jessie Lite. If you're running the full version of Raspbian instead, several of these steps will be redundant - it won't hurt to execute each install command though, you'll just be notified that you already have a given software package.

### Install Dependencies
  - Run -- `sudo apt-get update`
  - Run -- `sudo apt-get upgrade`
  - Install PiCamera -- `sudo apt-get install python-picamera`
  - Make sure camera interface is enabled with `sudo raspi-config` > Interfacing Options > Camera
  - Install GraphicsMagick -- `sudo apt-get install graphicsmagick`
  - Install Gitcore -- `sudo apt-get install git-core`
  - Install GifCam -- `git clone https://github.com/michaelruppe/gifcam.git`
  - Install pip: `sudo apt-get install python-pip`
  - Install twython: `sudo pip install twython` -- https://github.com/ryanmcgrath/twython
  - Create a twitter app at https://apps.twitter.com/ and populate `gifcam.py` with the necessary credentials. If you don't want to tweet your GIFs, don't create the app, and disable the functionality by setting `tweet = False` in `gifcam.py`.
  - Optional; Install mount USB if you want to use the `gifcamusb.py` script instead (no twitter, good for Pis without wifi. http://www.raspberrypi-spy.co.uk/2014/05/how-to-mount-a-usb-flash-disk-on-the-raspberry-pi/
  - To access your GIFs over WiFi, configure the gif directory as a samba shared directory


### Create Autorun Script:
  - Run -- `crontab -e`
  - add this line to end of that file - `@reboot sh /home/pi/gifcam/launcher.sh`
  
  
### Permissions:
  - If hitting "permission denied" run - `sudo chown -R pi /home/pi/gifcam/`
  
### Optional: Setup a Samba shared directory to access your GIFs over WiFi
  - Install samba: `sudo apt-get install samba samba-common-bin`
  - Create a backup of the default samba configuration: `sudo cp /etc/samba/smb.conf /etc/samba/smb.conf_$(date +%F)`
    This will create a copy, with today's date on the extension.
  -  Set the gif directory as a shared directory: `sudo nano /etc/samba/smb.conf` and add the following chunk:
  ```
  [gifs]
    comment = GIF share
    path = /home/pi/gifcam/gifs
    browseable = yes
    read only = no
  ```
  - Create samba users: execute `sudo smbpasswd -a pi` and enter your desired password. Whether you choose to keep this as the default (unsecure) is up to you. This will be the username and password required to access the shared folder.
  - Note: the gifs directory does not exist yet. It will be created when you snap your first GIF, or if you manually create it with `mkdir /home/pi/gifcam/gifs`.
  
## In-Depth instructions (Pi Zero W from first boot. These instructions will work for other models except for USB OTG steps)
  - Flash SD card with Jessie Lite
  - Setup USB OTG network access. This will allow you to always SSH into the Pi via a direct connection through USB - useful if you have problems with WiFi at any point.
    - Open the boot partition (in Windows Explorer, Finder etc) and add to the bottom of the `config.txt` file `dtoverlay=dwc2` on a new line, then save the file.
    - Open `cmdline.txt`. Very careful with the syntax in this file: Each parameter is seperated by a single space (it does not use newlines). Insert `modules-load=dwc2,g_ether` after rootwait
  - Setup WiFi access for first boot:
    - Create a file called `wpa_supplicant.conf` in the boot parition.
    - Paste the following text into the file, filling in your own WiFi SSID (network name) and password.
      ```
      network={
        ssid="SSID"
        psk="password"
        key_mgmt=WPA-PSK
      }
      ```
    - You can follow this process at any time to overwrite the WiFi credentials if you have to.
  - Enable SSH: create an empty file called `ssh` in the boot partition. Make sure there is no file extension.
  - Power the Pi and open an SSH session. If you're accessing over wifi, SSH to `pi@raspberrypi`. If you're accessing over USB OTG, SSH to `pi@raspberrypi.local`
  - On first boot give the Pi a meaningful hostname, like `gifcam`. This will avoid hostname conflicts on your network if you deploy another Raspberry Pi.
  - Now follow the _Basic Setup_ instructions


## ToDo:
- working directory referencing, this is so you can cleanup source images with: `rm $workingDir/\*.jpg` rather than from within the repo main directory
- samba shared folder to pull images off over wifi (Pi Zero W)
- smart twitter handling for when gifs are taken and you're not on wifi? If an image upload fails it gets pushed onto a re-attempt stack, which attempts to pop each time a gif is taken / an upload button pressed!
