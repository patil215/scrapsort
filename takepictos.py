import camera
import time
count = 33

while True:
	nothing = raw_input("picture time")
	camera.takePhoto("img/bottles/bottle%d.jpg" % (count))
	count = count + 1
