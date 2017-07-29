import rainbowhat

def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()

def set_all_pixels(*args, **kwargs):
	for pixel in range(7):
		rainbowhat.rainbow.set_pixel(pixel, *args, **kwargs)
	rainbowhat.rainbow.show()

def show_decision(isTrash):
	if isTrash:
		set_all_pixels(1, 0, 0)
		display_message("T")
	else:
		set_all_pixels(0, 1, 0)
		display_message("R")

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
