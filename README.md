# Control [OBS Studio](https://obsproject.com/) with Open Sound Control

This project was forked from https://github.com/CarloCattano/ObSC as the way I want to handle OSC differs from the original.

### Uses [Python-osc](https://pypi.org/project/python-osc/)   
### [OBS web socket](https://github.com/Palakis/obs-websocket/releases/tag/4.7.0)


## Control Obs from any OSC capable app running on the same network :
### * the script connects python to obs websocket on port 4444 in localhost using default credentials ( you might want to change that if you stream :-) 

 * you can get all the needed stuff with pip install -r requirements.txt
 * An osc listener runs on port 4444 and listens for /Scene message  

Requirements:
Developed on macOS 10.15 using Python3

To use this:
- Install OBS
- Install the OBS web socket
     - Set a password for the WebSockets Server Settings from the Tools menu in OBS.  You may need to restart OBS after installing.
- Change password listed in ObSC.py to match the one entered above
- CD into the directory (using Terminal)
- pip3 install -r requirements.txt
- python3 ObSC.py

Addresses will be printed into the terminal when it starts up.
