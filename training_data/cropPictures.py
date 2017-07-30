""" Crops pictures that come from the Raspberry Pi camera to match the size of the other pictures in the dataset. """


import os, sys
from PIL import Image

size = 683, 384

index = 483
for infile in os.listdir("bottles"):
    im = Image.open("bottles/" + infile)
    outfile = "out/plastic" + str(index) + ".jpg"
    im = im.resize((size[0], size[1]), Image.ANTIALIAS)

    width, height = im.size   # Get dimensions

    new_width = 512
    new_height = 384
    left = (width - new_width)/2
    top = (height - new_height)/2
    right = (width + new_width)/2
    bottom = (height + new_height)/2

    im = im.crop((left, top, right, bottom))

    im.save(outfile, "JPEG")
    index += 1
