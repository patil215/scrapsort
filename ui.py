import rainbowhat
import time

def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()


def display_long_message(message, n = 1, delay=.25):
	for i in range(n):
		for j in range(len(message)):
			time.sleep(delay)
			display_message(message[j : min(j + 4, len(message))])
		display_message("    ") # clear the display
		if i < (n - 1):
			time.sleep(1) # sleep after each loop except the last 

def set_all_pixels(*args, **kwargs):
	for pixel in range(7):
		rainbowhat.rainbow.set_pixel(pixel, *args, **kwargs)
	rainbowhat.rainbow.show()

def show_decision(is_trash):
	if is_trash:
		set_all_pixels(1, 0, 0)
		display_long_message("TRASH")
	else:
		set_all_pixels(0, 1, 0)
		display_long_message("RECYCLING")

@rainbowhat.touch.A.press()
def press_a(channel):
    display_message("A")
    rainbowhat.lights.rgb(1,0,0)

@rainbowhat.touch.B.press()
def press_b(channel):
    display_message("B")
    rainbowhat.lights.rgb(0,1,0)

@rainbowhat.touch.C.press()
def press_c(channel):
    display_message("C")
    rainbowhat.lights.rgb(0,0,1)


if __name__ == '__main__':
	show_decision(False)

	try:
		while True:
			pass
	except KeyboardInterrupt:
		pass
