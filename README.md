# TrashSort

We built a hardware device that uses computer vision to sort through recyclable items. Our hope is that it'll help reduce cognitive load on putting stuff in the right recycling bins, encourage people to recycle, and reduce the number of recyclable items that are inadverdently and unfortunately thrown away.

The classifier is best explained through a video:

INSERT_VIDEO

## The Classification Algorithm

Initially, when prototyping the classifier we used the Google Cloud Vision API. This API returned a list of labels for a given image. By searching through the labels, we could pick out keywords that we thought would work. However, this classifier turned out to not be accurate enough.

We decided to try to train our own convolutional neural network to pick the right trash label.

Special thanks to this paper - http://cs229.stanford.edu/proj2016/report/ThungYang-ClassificationOfTrashForRecyclabilityStatus-report.pdf - for the dataset and the overall architecture help.

Specially, I used the image retraining ability within Tensorflow to retrain the final layer of Inception-v3 on our own dataset. This consisted of images we took ourselves of the bottles and other items.

## Hardware

The sorter is prototyped with cardboard. A Raspberry Pi 3 sits at the top. It's connected to a Camera module for the material recognition and a HAT for displaying UI state to the user.

The Raspberry Pi turns two 

PICTURES

## Dashboard

I also built a custom dashboard that displays a few basic stats about 

INSERT_PICTURE_AND_LINK_HERE

## Future Plans

I'd like to build the hardware so it's more solid than the cardboard prototype, and integrate other sensors into the product - for example, looking at the weight to help classify. Initial results from training my own convnet were really promising as well - I think I could develop a fairly reliable recycling sorting algorithm if I spent more time taking training data. I'd also like to integrate the ability to sort into more than two trash bins - especially because the classifier has the ability to distinguish these objects already.

This project was created for Greylock Hackfest 2017.
