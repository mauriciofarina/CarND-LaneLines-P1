import cv2
import os
from Image import Image
from Params import Params

IMAGES_PATH = 'test_images/'
IMAGES_OUTPUT_PATH = 'test_images_output/'

params = Params("params.json")

for i in os.listdir(IMAGES_PATH):
    image = cv2.imread((IMAGES_PATH + i))
    imgObj = Image(i, image)
    imgObj.save(IMAGES_OUTPUT_PATH+i, params)
