import picamera

camera = picamera.PiCamera()

""" Takes a photo and saves it to the /img directory. """
def takePhoto(filepath):
	camera.capture(filepath)
