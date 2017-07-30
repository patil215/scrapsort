import servo
import ui
from camera import Camera
from vision import Classifier
import motiondetector
import time 
import brain
from databasehelper import Database
import os

TRASH_POS = 10
RECYCLE_POS = 160
NEUTRAL_POS = 100

def sort_trash(imgpath):
	camera = Camera()
	database = Database()
	classifier = Classifier(os.path.abspath('classifier/trained_graph.pb'), os.path.abspath('classifier/output_labels.txt'))

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
		labels = classifier.get_image_labels(imgpath)
		print labels
		selectedLabel = brain.getRecyclingLabel(labels)
		is_trash = selectedLabel == None

		database.write_result(imgpath, labels, is_trash, selectedLabel)
		print "Wrote result to database."

		if is_trash:
			print("It's trash.")
			ui.set_status("trash")
			servo.move(TRASH_POS)
		else:
			print("It's recyclable.")
			ui.set_status("recycling")
			servo.move(RECYCLE_POS)


def main():
	sort_trash('img/classificationImage.jpg')

if __name__ == '__main__':
	main()
