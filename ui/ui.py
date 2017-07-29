import rainbowhat

def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()

def show_decision(isTrash):
	display_message("T" if isTrash else "R")
	if isTrash:
		display_message("T")
		rainbowhat.lights.rgb(1, 0, 0)
	else:
		display_message("R")
		rainbowhat.lights.rgb(0, 1, 0)

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

show_decision(False)

try:
	while True:
		pass
except KeyboardInterrupt:
	pass
