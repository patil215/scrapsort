# TrashSort

We built a hardware device that uses computer vision to sort through recyclable items.

## Training the Classifier

Initially, when prototyping the classifier we used the Google Cloud Vision API. This API returned a list of labels for a given image. By searching through the labels, we could pick out keywords that we thought would work. However, this classifier turned out to not be accurate enough.

We decided to try to train our own convolutional neural network to pick the right trash label.

Specially, I used the image retraining ability within Tensorflow to retrain the final layer of Inception-v3 on our own dataset. This consisted of images we took ourselves of the bottles and other items.

## Hardware

The sorter is prototyped with cardboard. A Raspberry Pi 3 sits at the top. It's connected to a Camera module for the material recognition and a HAT for displaying UI state to the user.

Special thanks to this paper - http://cs229.stanford.edu/proj2016/report/ThungYang-ClassificationOfTrashForRecyclabilityStatus-report.pdf - for the dataset and the overall architecture help.

This project was created for Greylock Hackfest 2017.

Too often we head over to throw away our trash and are presented with rows and rows of recycling bins. If only there was a smart thing to sort those for us...

