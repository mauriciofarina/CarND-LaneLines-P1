# **Finding Lane Lines on the Road** 

---

**Finding Lane Lines on the Road**

The steps of this project are the following:
1. Develop a Lane Lines Finder Pipeline
1. Develop a Parameters Tuner Aplication
1. Develop a Aplication that runs the Algorithm on Images
1. Develop a Aplication that runs the Algorithm on Videos


[//]: # (Image References)
[image1]: ./test_images_output/solidWhiteCurve.jpg "Result"

---


## **Development**


### **Development Files**

| File | Description |
| ------ | ------ |
| Params.py | Parameters Class |
| Image.py | Image Processing Class | 
| params.json | Saved Parameters Values | 
| ImageTunerGUI.py | Pipeline Parameters Tuner App |
| LaneLinesFinderImage.py | Runs Pipeline on Images | 
| LaneLinesFinderVideo.py | Runs Pipeline on Videos |


### **Lane Lines Finder Pipeline**

In order to develop the pipeline, two classes were created:

- Params
- Image

The `Params` class contains all parameters for the pipeline and necessary validation. The `Image` class contains all the necessary methods for processing an image/frame and a pipeline implementation.

#### **Implementation**

Most of `Image` methods are straightforward implementations of `OpenCV` library, however, some parts deserve attention:

On the method `toRegion` the four vertices of a polygon are defined in a **percentage** scale. The reason for that was to resolve problems with videos of different resolutions. In this format, one can use the same parameters on different types of videos, as long as the camera is positioned in the same location.

On the methods `toHough` and `toHoughLines` an extra parameter was added in order to filter horizontal lines. The parameter `houghAngleIgnore` defines the line's minimum angle threshold. Lines below that angle are ignored.

In order to extrapolate the found lines the method `toLaneLines` was created. In order to obtain the desired results, the method execute the following steps:

1. Separate Hough Transform Lines in two groups: Right Lane Lines (Positive Slope Angles) and Left Lane Lines (Negative Slope Angles)
1. Check if Left and Right lanes were found
1. For each side, Average the lines Slope and Midpoint values
1. For each side, Calculate the `[x1,y1,x2,y2]` coordinates
1. Return the Output lines


The `Params` class is holds all parameters necessary for the pipeline. When defined, it tries to load the `params.json` file in order to obtain user defined parameters. If the file does not exists, a generic set of params is defined.

The method `validator` is responsible to check and fix bad parameter values. By running it, an invalid Gaussian Kernel even value would be changed to the closest lower odd value, for example.

Also, a `save` method was implemented in order to export parameters to a JSON file.


### **Lane Lines Finder Parameters Tuner Application**

In order to easily tune the pipeline parameters, a simple application was developed. This application is composed of 7 screens:

1. Original
1. Grayscale
1. Canny Transform
1. Region of Interest
1. Hough Transform
1. Highlighted Lane Lines
1. Extrapolated Lane Lines

#### **How to Use It:**

When started, the application loads all files inside of the `\test_images` folder. 

---
**NOTE**

Make sure you have only image files inside of `\test_images` folder. Other files may cause the application to get errors and/or crash.

---

Screens can be selected by pressing the keyboard keys `1 - 7`.

Pressing the keyboard key `s` saves the current parameters state to `params.json`.


### **Lane Lines Finder Image/Video Applications**

The `LaneLinesFinderImage` and `LaneLinesFinderImage` work virtually in the same way. Both of them load image/video files inside `\test_images` and `\test_videos` respectively, run the pipeline and save the results to `\test_images_output` and `\test_videos_output` respectively.

---
**NOTE**

Make sure you have only image files inside of `\test_images` folder and only video files inside of `\test_videos` folder. Other files may cause the application to get errors and/or crash.

---

### **Result**

The pipeline algorithm worked proficiently on the test images and videos. The output results can be found on the folders `\test_images_output` and `\test_videos_output` and a similar to the image below:

![alt text][image1]

On the Challenge video, four problems were identified:

- Different Resolution Video
- Car Hood
- Light Color Lane
- Light Shadows and Lane Color Changes

The first two problems where addressed by:

- Changing the vertices parameters to a percentage instead of pixel coordinates, fixing the resolution problem.
- Ignoring horizontal Hough Transform lines, by removing small slope angle lines, fixing the car hood problem.

The light color lane issue caused yellow lines not to be found. This problem could be solved by converting the color yellow to white in the region of interest. Also, black lines on this lanes were found, adding more noise to the results. Also, light shadows and lane color changes were the biggest cause of noise in the results. A shadow remover filter could address some of this issues.
