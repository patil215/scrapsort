import servo
import ui
import camera
import vision

def classify(imgpath):
	labels = vision.get_image_labels(imgpath)
	
	#servo.move(20)
	if 'plastic' in str(labels):
		print "a bottle"
		servo.move(200)
		servo.move(110)
	else:
		print "not a bottle"
		servo.move(40)
		servo.move(110)

def main():
	camera.takePhoto('img/classificationImage.jpg')
	classify('img/classificationImage.jpg')

if __name__ == '__main__':
	main()
