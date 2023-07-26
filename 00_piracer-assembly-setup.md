
## Introduction
This documentation consists of the assembly process of the JetRacer(PiRacerStandard), setup of the raspberry Pi 4 and the testrun of the powertrain, steering and camera.

## Contents  
- [Step 1: Assemble PiRacer](#step-0-assemble-piracer) 
- [Step 1: Install OS](#step-1-install-os) 
- [Step 2: SSH & Network Configuration](#step-2-ssh-&-network-configuration)  
- [Step 3: Add additional ubuntu sources & install dependencies](#step-3-add-additional-ubuntu-sources-&-install-dependencies)  
- [Step 4: Setup periphery](#step-4-setup-periphery) 
- [Step 5: Install piracer-py package](#step-5-Install-piracer-py-package)  
- [Step 6: Run Examples & Test PiRacer](#step-6-run-examples-&-test-piracer)  

## Assemble PiRacer

First, assemble the piracer/jetracer under guidance of the waveshare wiki.
https://www.waveshare.com/wiki/JetRacer_Assembly_Manual

## Install OS

For the installation, use the Raspberry Pi imager (https://www.raspberrypi.com/software/)

Hardware:
	• Raspberry Pi 4 Model B 4GB
Distribution:
	• Ubuntu Desktop 20.04.2 LTS (64-Bit)

### SSH & Network Configuration

To activate SSH on an Ubuntu , you'll need to follow these steps:

**Step 1: Connect to Your Server & Check if SSH is Installed**
You'll need to have physical access to the server.
Open a terminal and  check if the SSH server is installed by running the following command:

```bash
sudo systemctl status ssh
```

If it's installed, you'll see the status of the SSH service. If it's not installed, you will see an error message, and you can proceed to Step 3.

**Step 2: Update the Server (Optional)**
Before installing SSH, it's a good idea to update the package list and upgrade the installed packages to their latest versions. Run the following commands:

```bash
sudo apt update
sudo apt upgrade
```

**Step 3: Install SSH (If Not Installed)**
If SSH is not installed, you can install it using the package manager (apt). Run the following command to install the OpenSSH server:

```bash
sudo apt install openssh-server
```

**Step 4: Enable and Start SSH**
After installing SSH, you need to enable and start the SSH service. Run the following commands:

```bash
sudo systemctl enable ssh
sudo systemctl start ssh
```

**Step 5: Allow SSH Through the Firewall (If Applicable)**
If you have a firewall running on your server (e.g., UFW), you need to allow SSH traffic. If UFW is installed, you can enable the SSH rule with the following command:

```bash
sudo ufw allow ssh
```

**Step 6: Connect via SSH**
With SSH now installed and running, you should be able to connect to your Ubuntu server remotely via SSH using an SSH client. You can use the terminal on macOS and Linux or an application like PuTTY on Windows.

For example, to connect via the terminal, use the following command:

```bash
ssh username@server_ip_address
```

Replace `username` with your username on the server, and `server_ip_address` with the actual IP address of your Ubuntu server. Make sure you replace the default SSH port (if you changed it) and use the appropriate credentials to log in.

We highly recommend to use Visual Studio Code with the "Remote-SSH" Extentions. 

https://linuxize.com/post/how-to-enable-ssh-on-ubuntu-20-04/

Note: The network config file can be edited via terminal using these guides:
 https://linuxconfig.org/ubuntu-20-04-connect-to-wifi-from-command-line 
 &
 https://tttapa.github.io/Pages/Raspberry-Pi/Installation+Setup/WiFi-Setup.html

### Add additional ubuntu sources & install dependencies
Add the following sources:
```bash
	sudo -s
    echo "deb http://archive.raspberrypi.org/debian/ buster main" >> /etc/apt/sources.list
    apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 7FA3303E
    apt update
    exit
```
	
If you're facing messages like the following when trying to install packages via apt:
```bash
    pi@ubuntu:/home/pi# sudo apt install PACKAGES…
    Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It is held by process 1807 (unattended-upgr)
```
Disable the unattended upgrade feature by running the following command to disable:
```bash
	sudo dpkg-reconfigure unattended-upgrades
```

Install the following depencencies: 

```bash
    sudo apt update
    sudo apt install 
        git \ 
        gcc \
        v4l-utils \
        i2c-tools \
        raspi-config \
        python3-dev \
        python3-setuptools \
        python3-venv \
        libopencv-dev
```

If the raspi-config installation does not work (found on Ubuntu Server 20.04. LTS) use the following process (https://raspberrypi.stackexchange.com/questions/111728/how-to-get-raspi-config-on-ubuntu-20-04) Using V(20211019) https://archive.raspberrypi.org/debian/pool/main/r/raspi-config/)

## Setup periphery
First, Mount boot partition (Ubuntu only). 
On Ubuntu it is necessary to explicitly mount the boot partition before enabling the i2c controller and camera:
```bash
    mount /dev/mmcblk0p1 /boot/
```

Enable i2c and camera in raspi-config.
```bash
    sudo raspi-config
```

Use the arrow keys to navigate through the raspi-config tool and enable the following peripherals:
	• Interface Options > I2C
	• Interface Options > (Legacy) Camera

Afterwards, reboot:
```bash
	sudo reboot
```

Note: Somehow the sequence in which the interfaces are activated is important. If the camera does not work after setup, disable all interfaces in config tool, restart the pi and then re-enable in the order shown above. 

If the camera configuration is done & the pi is running again. The following terminal commands (or the "cheese" camara application) can be used to test the camera.
```bash
    vcgencmd get_camera
```
Check if a camera is detected, the ouptut should look like this:  
```bash
    supported=1 detected=1 
```
Install Camera dependemcies if needed. 
```bash
	sudo apt updatesudo apt install -y python3-picamera
```

## Install piracer-py package

Git clone the piracer_py repository (insert link!) & create project folder on Pi's directory: 
```bash
    cd ~
    mkdir piracer_test/
    cd piracer_test/
    python3 -m venv venv
    source venv/bin/activate
    pip install piracer-py
```	
	
## Run Examples & Test PiRacer

The following examples will show the basic functionality of the piracer-py package. 
Make sure the virtual environment from step Install piracer-py package is activated.
Note: use class PiRacerStandard from piracer.vehicles !

### Test power train & steering.
Paste the following code into basic_example.py

```python
    import time
    # from piracer.vehicles import PiRacerPro
    from piracer.vehicles import PiRacerStandard
    if __name__ == '__main__':
    piracer = PiRacerPro()
        # piracer = PiRacerStandard()
    # Forward
        piracer.set_throttle_percent(0.2)
        time.sleep(2.0)
    # Brake
        piracer.set_throttle_percent(-1.0)
        time.sleep(0.5)
        piracer.set_throttle_percent(0.0)
        time.sleep(0.1)
    # Backward
        piracer.set_throttle_percent(-0.3)
        time.sleep(2.0)
    # Stop
        piracer.set_throttle_percent(0.0)
    # Steering left
        piracer.set_steering_percent(1.0)
        time.sleep(1.0)
    # Steering right
        piracer.set_steering_percent(-1.0)
        time.sleep(1.0)
    # Steering neutral
        piracer.set_steering_percent(0.0)
```	

Run in terminal:
```bash
    python basic_example.py
```	

### Test remote control 
The following example will let you control the PiRacer with the ShanWan Gamepad that is shipped with the PiRacer package.
Make sure the dongle is connected to your Raspberry Pi.
Paste the following code into rc_example.py:
```python
    # from piracer.vehicles import PiRacerPro
    from piracer.vehicles import PiRacerStandard
    from piracer.gamepads import ShanWanGamepad
    if __name__ == '__main__':
    shanwan_gamepad = ShanWanGamepad()
        piracer = PiRacerPro()
        # piracer = PiRacerStandard()
    while True:
            gamepad_input = shanwan_gamepad.read_data()
    throttle = gamepad_input.analog_stick_right.y * 0.5
            steering = -gamepad_input.analog_stick_left.x
    print(f'throttle={throttle}, steering={steering}')
    piracer.set_throttle_percent(throttle)
            piracer.set_steering_percent(steering)
```	
Run it with:
```bash
    python rc_example.py
```	

(insert image of driving car here!)

### Test grab images
With the following example you can grab and save images from the Raspberry Pi camera.
Paste the following code into camera_grab_example.py:

import cv2
```python
from piracer.cameras import Camera, MonochromeCamera
if __name__ == '__main__':
    camera = MonochromeCamera()
image = camera.read_image()
    cv2.imwrite('image.png', image)
Run it with:
python camera_grab_example.py
```	
Run it with:
```bash
    python grab_image_example.py
```	

(insert test image here!)
