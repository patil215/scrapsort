import wiringpi
import time

initialized = False

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period= 0.01
initialized = True

def move(position):
#	initialize()
	wiringpi.pwmWrite(18, position)
	time.sleep(1)
