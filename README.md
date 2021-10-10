# PTSrpi-Mini
Pan / Tilt / Slider App for Raspberry Pi - 800 x 480 touchscreen.<br>
YouTube tutorial: https://youtu.be/wbUkVF55yrs

Designed for use with Isaac879's Pan Tilt Slider mount (https://www.youtube.com/c/isaac879)

Built for use with:<br>
Raspberry Pi 4 (https://amzn.to/2Yy1b1B)<br>
800x480 touchscreen (https://amzn.to/3AuYOKn)

Opional:<br>
PS4 Dualshock controller (https://amzn.to/3oKYCV7)<br>
XBOX 360 USB controller (https://amzn.to/3lzJIiB)

Drag both files to the desktop for easy access.

Connect your Raspberry Pi to your PTS mount via bluetooth.<br>
To get the MAC address of the bluetooth in your PTS mount, in terminal run:
```
hcitool scan
```
Replace the MAC address in the file "btcomm.sh", you may run the file from within the PTSrpi app.

To make the application executable, in terminal, change directory to the Desktop and change the file permissions:
```
cd Dekstop
chmod +x PTSrpi.py
```
When double clicking on PTSrpi.py, choose "Execute in Terminal" so you can connect to your PTS mount. "Connect" needs a running Terminal to work.
Click "FS" to come out of FullScreen and monitor the terminal there. Note, it may take several attempts to connect. If you click the BlueTooth icon, you should see a greem tick next to the BT device when it's connected.
