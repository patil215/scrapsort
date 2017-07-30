import time
from datetime import datetime
import picamera
from picamera import PiCamera
from io import BytesIO
from PIL import Image

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many pixels need to have changed before we mark motion as having occurred)
threshold = 10
sensitivity = 500

# Capture a small test image for motion detection
def captureTestImage(camera):
    stream = BytesIO()
    camera.capture(stream, format='jpeg', resize=(100, 75))
    stream.seek(0)
    image = Image.open(stream)
    buffer = im.load()
    stream.close()
    return im, buffer

""" Blocks until motion detection has occurred. Once motion passes the threshold, returns."""
def waitForMotionDetection():
    camera = PiCamera()

    # Get first image
    image1, buffer1 = captureTestImage(camera)

    while (True):
        # Get comparison image
        image2, buffer2 = captureTestImage(camera)

        # Count changed pixels
        changedPixels = 0
        for x in xrange(0, 100):
            for y in xrange(0, 75):
                # Just check green channel - it's highest quality
                pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
                if pixdiff > threshold:
                    changedPixels += 1
                    
        # Break out of the loop if the pixels have changed
        if changedPixels > sensitivity:
            break

        # Swap comparison buffers
        image1 = image2
        buffer1 = buffer2

        # Wait for half a second before taking another picture
        time.sleep(0.5)
