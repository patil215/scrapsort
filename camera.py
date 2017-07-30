import picamera

initialized = False

class Camera:
	camera = None
	def __init__(self):
		self.camera = picamera.PiCamera()
	
	def takePhoto(self, filepath):
		""" Takes a photo and saves it to the /img directory. """
		self.camera.capture(filepath)

	def getPiCamera(self):
		return self.camera
