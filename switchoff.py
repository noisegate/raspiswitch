#THIS CODE HAS NOT BEEN TESTED
#USE AT OWN RISK
#http://www.raspberry-pi-geek.com/Archive/2013/01/Adding-an-On-Off-switch-to-your-Raspberry-Pi

# This is OBSOLETE
# Import the modules to send commands to the system and access GPIO pins
#
#to auto start this script do:
#  sudo nano /etc/rc.local
#
#add this line
#  python /home/pi/PiSupply/softshut.py
#before
#  exit 0
##
# NEW APPROACH
# ----------------------------
# In Jessie we do it this way:
# ----------------------------
# now do this
# make /lib/systemd/system/myscript.service
# and add
#
#[Unit]
#Description=My Script Service
#After=multi-user.target
#
#[Service]
#Type=idle
#ExecStart=/usr/bin/python /home/pi/switchoff.py
#
#[Install]
#WantedBy=multi-user.targe
#
#sudo chmod 644 /lib/systemd/system/myscript.service
#sudo systemctl daemon-reload
#sudo systemctl enable myscript.service
#the reboot
#to check if it works
#sudo systemctl status myscript.service
#to log output of the script:
#add ExecStart=/usr/bin/python /home/pi/myscript.py > /home/pi/myscript.log 2>&1 to
#script file
#http://www.raspberrypi-spy.co.uk/2015/10/how-to-autorun-a-python-script-on-boot-using-systemd/


from subprocess import call
import RPi.GPIO as gpio
import time

class Shutdown(object):

    def __init__(self, inputpin = 7, keep_powered_pin=8):
        self.inputpin = inputpin
	self.keep_powered_pin = keep_powered_pin

    # Define a function to run when an interrupt is called
    def shutdown(self, pin):
        gpio.output(self.keep_powered_pin, 0)
        call('halt', shell=False)

    def setup(self):
        gpio.setmode(gpio.BOARD) # Set pin numbering to board numbering
        gpio.setup(self.inputpin, gpio.IN) # Set up pin 7 as an input
        # Set up an interrupt to look for button presses
        gpio.add_event_detect(self.inputpin, gpio.RISING, callback=self.shutdown, bouncetime=200)
        gpio.setup(self.keep_powered_pin, gpio.OUT, initial=gpio.HIGH)

    def loop(self):
	while True:
            time.sleep(10)

if __name__ == '__main__':
    instance = Shutdown()
    instance.setup()
    instance.loop()

