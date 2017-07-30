import servo
import ui
import camera
import vision

import time 

TRASH_POS = 40
RECYCLE_POS = 200
NEUTRAL_POS = 105

def classify(imgpath):
	labels = vision.get_image_labels(imgpath)
	print labels
	return 'plastic' in str(labels)
	
	#servo.move(20)
	# if 'plastic' in str(labels):
	# 	print "a bottle"
	# 	servo.move(200)
	# else:
	# 	print "not a bottle"
	# 	servo.move(40)
	# servo.move(105)




def sort_trash(imgpath):
	ui.start_status_shower_thread()

	while True:
		servo.move(NEUTRAL_POS)
		set_status("ready")

		# wait for camera to detect motion, then sleep for a bit to
		# let the object settle down
		waitForMotionDetection()
		time.sleep(2) # TODO maybe remove

		set_status("classifying")

		# take a photo and classify it
		camera.takePhoto(imgpath)
		is_trash = classify(imgpath)

		if is_trash:
			print("It's trash.")
			set_status("trash")
			servo.move(TRASH_POS)
		else:
			print("It's recyclable.")
			set_status("recycling")
			servo.move(RECYCLE_POS)




def main():
	sort_trash('img/classificationImage.jpg')

if __name__ == '__main__':
	main()
