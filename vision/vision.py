import io

from google.cloud import vision
from google.cloud.vision import types

client = vision.ImageAnnotatorClient()


def get_image_labels(file_path):
    """Use Google Vision API to get the labels for the image at specified file path."""
    with io.open(file_path, 'rb') as image_file:
        content = image_file.read()
    image = types.Image(content=content)
    response = client.label_detection(image=image)

    return response.label_annotations
