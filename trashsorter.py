import wiringpi
import time

wiringpi.wiringPiSetupGpio()

wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)

wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)

wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

delay_period= 0.01

while True:
	wiringpi.pwmWrite(18, 10)
	time.sleep(1)
	wiringpi.pwmWrite(18, 170)
	time.sleep(1)

#def main():

#if __name__ == '__main__':
	#main()
