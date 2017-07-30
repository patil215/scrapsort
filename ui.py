import rainbowhat
import time
import threading

status_lock = threading.Condition()
status = "ready"

# each color is a tuple (r, g, b)
status_colors = {
	"ready": (0, 1, 0),
	"classifying": (0, 0, 1),
	"recycling": (0, 1, 1),
	"trash": (1, 0, 1),
}


def display_message(message):
    rainbowhat.display.print_str(message)
    rainbowhat.display.show()



def display_long_message(message, delay=.25):
	for i in range(len(message)):
		time.sleep(delay)
		display_message(message[i : min(i + 4, len(message))])
	display_message("    ") # clear the display


def set_all_pixels(*args, **kwargs):
	for pixel in range(7):
		rainbowhat.rainbow.set_pixel(pixel, *args, **kwargs)
	rainbowhat.rainbow.show()


def show_status(status):
	if status == "ready":
		set_all_pixels(0, 1, 0, brightness=1)
	else:
		set_all_pixels(1, 0, 0, brightness=1)
	display_long_message(status)

# def show_decision(is_trash):
# 	if is_trash:
# 		set_all_pixels(1, 0, 0)
# 		display_long_message("TRASH")
# 	else:
# 		set_all_pixels(0, 1, 0)
# 		display_long_message("RECYCLING")


class StatusShower(threading.Thread):
	def run(self):
		global status
		while True:
			status_lock.acquire()
			s = status
			status_lock.release()

			color = status_colors[s]
			set_all_pixels(*color, brightness=1)
			display_long_message(s)

			time.sleep(1)

def start_status_shower_thread():
	return StatusShower()

def set_status(s):
	global status 
	status_lock.acquire()
	status = s
	status_lock.release()



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
