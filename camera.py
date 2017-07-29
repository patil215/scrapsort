import picamera

""" Takes a photo and saves it to the /img directory. """
def takePhoto(filepath):
	camera = picamera.PiCamera()
	camera.capture(filepath)

