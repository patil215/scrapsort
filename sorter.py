import servo
import ui
from camera import Camera
import vision
import motiondetector
import time 
import brain

TRASH_POS = 10
RECYCLE_POS = 180
NEUTRAL_POS = 100

def sort_trash(imgpath):
	camera = Camera()	

	statusThread = ui.start_status_shower_thread()

	while True:
		servo.move(NEUTRAL_POS)
		ui.set_status("ready")

		# wait for camera to detect motion, then sleep for a bit to
		# let the object settle down
		print "waiting for motion..."
		motiondetector.waitForMotionDetection(camera.getPiCamera())
		time.sleep(0.5) # Lets object settle down, TODO maybe remove
		
		print "detected motion"

		ui.set_status("classifying")

		# take a photo and classify it
		camera.takePhoto(imgpath)
		labels = vision.get_image_labels(imgpath)
		is_trash = brain.isTrash(labels)

		if is_trash:
			print("It's trash.")
			ui.set_status("trash")
			servo.move(TRASH_POS)
		else:
			print("It's recyclable.")
			ui.set_status("recycling")
			servo.move(RECYCLE_POS)

	statusThread.shutdown()

def main():
	sort_trash('img/classificationImage.jpg')

if __name__ == '__main__':
	main()
