import os
from moviepy.editor import VideoFileClip
from Image import Image
from Params import Params

params = Params("params.json")

VIDEOS_PATH = 'test_videos/'
VIDEOS_OUTPUT_PATH = 'test_videos_output/'


def processImage(image):
    img = Image("frame", image)
    return img.getLaneLines(params)


for v in os.listdir(VIDEOS_PATH):
    whiteOutput = VIDEOS_OUTPUT_PATH + v
    clip1 = VideoFileClip(VIDEOS_PATH+ v)
    whiteClip = clip1.fl_image(processImage)
    whiteClip.write_videofile(whiteOutput)






