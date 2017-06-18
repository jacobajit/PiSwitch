from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub
from pubnub.enums import PNStatusCategory
from pubnub.callbacks import SubscribeCallback
import json,time
import os

##try:
##    import RPi.GPIO as GPIO
##except RuntimeError:
##    print "Error importing RPi.GPIO!  This is probably because you need superuser privileges.  You can achieve this by using 'sudo' to run your script"

#setup servod
#filepath = os.path.join('~/Downloads/PiBits/ServoBlaster/user', '/servod')
os.system('sudo /home/pi/Documents/PiSwitch/PiBits/ServoBlaster/user/servod --idle-timeout=2000 --min=800us --max=2200us')

#Setup GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)

#Setup PubNub
pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-c72d9fd4-9212-11e6-a68c-0619f8945a4f'
pnconfig.publish_key = 'pub-c-6e839019-682d-44bf-9f0a-1f15abd00dc8' 
pubnub = PubNub(pnconfig)

#pubnub = PubNub(publish_key="pub-c-6e839019-682d-44bf-9f0a-1f15abd00dc8",subscribe_key="sub-c-c72d9fd4-9212-11e6-a68c-0619f8945a4f")
pubnubChannelName = 'gpio-raspberry-control'


#Setup Glow Status Flow
glow = False
################################################3
class MyListener(SubscribeCallback):
    def status(self, pubnub, status):
        if status.category == PNStatusCategory.PNConnectedCategory:
            pass
 
    def message(self, pubnub, message):
        global glow

        respstring = ''
	command = message.message

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
		pubnub.publish().channel(pubnubChannelName).message(respmsg).sync()

        pass
 
    def presence(self, pubnub, presence):
        pass
 
my_listener = MyListener()
 
pubnub.add_listener(my_listener)
 
pubnub.subscribe().channels(pubnubChannelName).execute()




##
##if __name__ == '__main__':
##
##	GPIO.setup(15, GPIO.OUT)
##
##	#pubnub.subscribe(channels=pubnubChannelName, callback=gpioCallback, error=gpioError)
##	pubnub.add_listener(SubscribeListener())	
##	pubnub.subscribe().channels('pubnubChannelName').execute()
##	while True:
##
##		time.sleep(5000)
##
##		if(GPIO.gpio_function(15)):
##			#All is over
##			break

