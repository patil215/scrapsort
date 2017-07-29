import picamera

""" Takes a photo and saves it to the /img directory. """
def takephoto(filepath):
	camera = picamera.PiCamera()
	camera.capture('img/' + filepath)

takephoto('image.jpg')
