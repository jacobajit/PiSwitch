
from pubnub import Pubnub
import json,time
import os

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print "Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script"

#setup servod
#filepath = os.path.join('~/Downloads/PiBits/ServoBlaster/user', '/servod')
os.system('sudo /home/pi/Documents/PiSwitch/PiBits/ServoBlaster/user/servod --idle-timeout=2000 --min=800us --max=2200us')

#Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#Setup PubNub
pubnub = Pubnub(publish_key="pub-c-6e839019-682d-44bf-9f0a-1f15abd00dc8",subscribe_key="sub-c-c72d9fd4-9212-11e6-a68c-0619f8945a4f")
pubnubChannelName = 'gpio-raspberry-control'


#Setup Glow Status Flow
glow = False

#PubNub Channel Subscribe Callback
def gpioCallback(msg,channel):

	global glow

	respstring = ''
	command = msg

	print "Command is : " + str(command)

	if('req' in command):
		if(command['req'] == 'toggle'):

			if(glow == False):
				glow = True
				respstring = 'off'
			else:
				glow = False
				respstring = 'on'

			#GPIO.output(15, glow)
			if(glow == True):
				os.system("echo P1-12=100% > /dev/servoblaster")
			else:
				os.system("echo P1-12=0% > /dev/servoblaster")

			
			respmsg = {"resp" : respstring }
			pubnub.publish(pubnubChannelName, respmsg)


#PubNub Channel Subscribe Callback
def gpioError(msg):
	print 'Error :' + msg




if __name__ == '__main__':

	GPIO.setup(15, GPIO.OUT)

	pubnub.subscribe(channels=pubnubChannelName, callback=gpioCallback, error=gpioError)

	while True:

		time.sleep(5000)

		if(GPIO.gpio_function(15)):
			#All is over
			break

