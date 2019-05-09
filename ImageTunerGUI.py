import cv2
import os
from Image import Image
from Params import Params


# Defines
NAME = 'Lane Line Finder Tuner'
IMAGES_PATH = 'test_images/'

STEP_ORIGINAL = 0
STEP_REGION = 1
STEP_GRAYSCALE = 2
STEP_CANNY = 3
STEP_HOUGH = 4
STEP_DONE = 5
STEP_LANE_LINES = 6


# Init Global Variables
windowIndex = 0
imgIndex = 0
stepIndex = 0
images = []
displayImage = 0

# Load Params
params = Params("params.json")


# Load Images
def loadImages():
    for i in os.listdir(IMAGES_PATH):
        image = cv2.imread((IMAGES_PATH + i))
        images.append(Image(i, image))


# Display Image
def display():
    global displayImage
    global images
    images[imgIndex].params = params

    if stepIndex == STEP_ORIGINAL:
        displayImage = images[imgIndex].getOriginal()
    elif stepIndex == STEP_REGION:
        displayImage = images[imgIndex].getRegion(params)
    elif stepIndex == STEP_GRAYSCALE:
        displayImage = images[imgIndex].getGrayscale()
    elif stepIndex == STEP_CANNY:
        displayImage = images[imgIndex].getCanny(params)
    elif stepIndex == STEP_HOUGH:
        displayImage = images[imgIndex].getHough(params)
    elif stepIndex == STEP_DONE:
        displayImage = images[imgIndex].getDone(params)
    elif stepIndex == STEP_LANE_LINES:
        displayImage = images[imgIndex].getLaneLines(params)

    cv2.imshow(NAME, displayImage)


# Image Select Callback
def imageSelect(value):
    global imgIndex
    imgIndex = value
    display()


# Step Select Callback
def stepSelect(value):
    global stepIndex
    stepIndex = value


# Region Step Callback
def regionStep(value):
    global params
    params.x1 = cv2.getTrackbarPos('X1', NAME)
    params.y1 = cv2.getTrackbarPos('Y1', NAME)
    params.x2 = cv2.getTrackbarPos('X2', NAME)
    params.y2 = cv2.getTrackbarPos('Y2', NAME)
    params.x3 = cv2.getTrackbarPos('X3', NAME)
    params.y3 = cv2.getTrackbarPos('Y3', NAME)
    params.x4 = cv2.getTrackbarPos('X4', NAME)
    params.y4 = cv2.getTrackbarPos('Y4', NAME)
    params.validator()
    display()


# Canny Step Callback
def cannyStep(value):
    global params
    params.gaussianKernel = cv2.getTrackbarPos(
        'Gaussian Kernel\n(Even Numbers are Ignored)', NAME)
    params.cannyLowThreshold = cv2.getTrackbarPos('Canny Low Threshold', NAME)
    params.cannyHighThreshold = cv2.getTrackbarPos(
        'Canny High Threshold', NAME)
    params.validator()
    display()


# Hough Step Callback
def houghStep(value):
    global params
    params.houghRho = cv2.getTrackbarPos('Rho', NAME)
    params.houghTheta = cv2.getTrackbarPos('Theta\n(Pi/Theta)', NAME)
    params.houghThreshold = cv2.getTrackbarPos('Threshold', NAME)
    params.houghMinLineLen = cv2.getTrackbarPos('Min Line Length', NAME)
    params.houghMaxLineGap = cv2.getTrackbarPos('Max Line Gap', NAME)
    params.houghAngleIgnore = cv2.getTrackbarPos('Max Line Angle', NAME)
    params.validator()
    display()


# Window Initialization
def windowInit(name, imgSize, index):
    cv2.destroyAllWindows()
    cv2.namedWindow(name, cv2.WINDOW_NORMAL)
    cv2.moveWindow(name, 40, 30)
    cv2.resizeWindow(name, 600, 600)
    cv2.createTrackbar('IMG', name, index, (imgSize-1), imageSelect)
    imageSelect(index)
    cv2.imshow(name, displayImage)


# Display Original Image Window
def originalWindow():
    stepSelect(STEP_ORIGINAL)
    windowInit(NAME, len(images), imgIndex)

# Display Region Image Window
def regionWindow():
    stepSelect(STEP_REGION)
    windowInit(NAME, len(images), imgIndex)

    cv2.createTrackbar('X1', NAME, params.x1, 100, regionStep)
    cv2.createTrackbar('Y1', NAME, params.y1, 100, regionStep)
    cv2.createTrackbar('X2', NAME, params.x2, 100, regionStep)
    cv2.createTrackbar('Y2', NAME, params.y2, 100, regionStep)
    cv2.createTrackbar('X3', NAME, params.x3, 100, regionStep)
    cv2.createTrackbar('Y3', NAME, params.y3, 100, regionStep)
    cv2.createTrackbar('X4', NAME, params.x4, 100, regionStep)
    cv2.createTrackbar('Y4', NAME, params.y4, 100, regionStep)

# Display Grayscale Image Window
def grayscaleWindow():
    stepSelect(STEP_GRAYSCALE)
    windowInit(NAME, len(images), imgIndex)

# Display Canny Image Window
def cannyWindow():
    stepSelect(STEP_CANNY)
    windowInit(NAME, len(images), imgIndex)

    cv2.createTrackbar('Gaussian Kernel\n(Even Numbers are Ignored)',
                       NAME, params.gaussianKernel, 20, cannyStep)
    cv2.createTrackbar('Canny Low Threshold', NAME,
                       params.cannyLowThreshold, 300, cannyStep)
    cv2.createTrackbar('Canny High Threshold', NAME,
                       params.cannyHighThreshold, 600, cannyStep)

# Display Hough Image Window
def houghWindow():
    stepSelect(STEP_HOUGH)
    windowInit(NAME, len(images), imgIndex)

    cv2.createTrackbar('Rho', NAME, params.houghRho, 20, houghStep)
    cv2.createTrackbar('Theta\n(Pi/Theta)', NAME,
                       params.houghTheta, 1000, houghStep)
    cv2.createTrackbar('Threshold', NAME,
                       params.houghThreshold, 600, houghStep)
    cv2.createTrackbar('Min Line Length', NAME,
                       params.houghMinLineLen, 600, houghStep)
    cv2.createTrackbar('Max Line Gap', NAME,
                       params.houghMaxLineGap, 600, houghStep)
    cv2.createTrackbar('Max Line Angle', NAME,
                       params.houghAngleIgnore, 90, houghStep)

# Display Done Image Window
def doneWindow():
    stepSelect(STEP_DONE)
    windowInit(NAME, len(images), imgIndex)

# Display Lane Lines Image Window
def laneLinesWindow():
    stepSelect(STEP_LANE_LINES)
    windowInit(NAME, len(images), imgIndex)


# Main
loadImages()
windowInit(NAME, len(images), 0)

while(1):
    k = cv2.waitKey(300)

    if k == 49: # Step 1
        originalWindow()
    elif k == 50: # Step 2
        grayscaleWindow()
    elif k == 51: # Step 3
        cannyWindow()
    elif k == 52: # Step 4
        regionWindow()
    elif k == 53: # Step 5
        houghWindow()
    elif k == 54: # Step 6
        doneWindow()
    elif k == 55: # Step 7
        laneLinesWindow()
    elif k == 115: # Save Params
        params.save("params.json")
    elif k == 27:
        break
    elif cv2.getWindowProperty(NAME, cv2.WND_PROP_VISIBLE) < 1:
        break


cv2.destroyAllWindows()
