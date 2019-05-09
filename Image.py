import numpy as np
import cv2
import math


class Image:

    def __init__(self, name, image):
        self.original = image
        self.name = name
        self.ysize = image.shape[0]
        self.xsize = image.shape[1]


    # Convert image to Grayscale
    def toGrayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)


    # Convert image to Gaussian Blur
    def toGaussianBlur(self, image, params):
        return cv2.GaussianBlur(image, (params.gaussianKernel, params.gaussianKernel), 0)


    # Convert image to Canny Transform
    def toCanny(self, image, params):
        return cv2.Canny(image, params.cannyLowThreshold, params.cannyHighThreshold)


    # Convert image to image of Region of Interest
    def toRegion(self, image, params):

        # Convert Percentage to Pixels
        pixX1 = int(params.x1 * self.xsize / 100)
        pixX2 = int(params.x2 * self.xsize / 100)
        pixX3 = int(params.x3 * self.xsize / 100)
        pixX4 = int(params.x4 * self.xsize / 100)
        pixY1 = int(params.y1 * self.ysize / 100)
        pixY2 = int(params.y2 * self.ysize / 100)
        pixY3 = int(params.y3 * self.ysize / 100)
        pixY4 = int(params.y4 * self.ysize / 100)

        vertices = np.array([[(pixX1, pixY1),
                                (pixX2, pixY2),
                                (pixX3, pixY3),
                                (pixX4, pixY4)]],
                                dtype=np.int32)


        mask = np.zeros_like(image)

        # defining a 3 channel or 1 channel color to fill the mask with depending on the input image
        if len(image.shape) > 2:
            channel_count = image.shape[2]  # i.e. 3 or 4 depending on your image
            ignore_mask_color = (255,) * channel_count
        else:
            ignore_mask_color = 255

        # filling pixels inside the polygon defined by "vertices" with the fill color
        cv2.fillPoly(mask, vertices, ignore_mask_color)

        # returning the image only where mask pixels are nonzero
        return cv2.bitwise_and(image, mask)


    # Convert image to Hough Transform
    def toHough(self, image, params):

        # Convert Deg to Rad
        theta = np.pi/params.houghTheta

        lines = cv2.HoughLinesP(image,
                                params.houghRho,
                                theta,
                                params.houghThreshold,
                                np.array([]),
                                minLineLength=params.houghMinLineLen,
                                maxLineGap=params.houghMaxLineGap)


        outputImage = np.zeros((image.shape[0], image.shape[1], 3), dtype=np.uint8)

        if (lines is not None):
            # Draw Lines
            for x1, y1, x2, y2 in lines[:,0]:
                # Calculate Line Angle
                angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                # Ignore Horizontal Angles
                if not (-params.houghAngleIgnore < angle < params.houghAngleIgnore):
                    cv2.line(outputImage, (x1, y1), (x2, y2), [255, 0, 0], 2)

        return outputImage


    # Convert image to Hough Transform Lines Array
    def toHoughLines(self, image, params):

        # Convert Deg to Rad
        theta = np.pi/params.houghTheta

        lines = cv2.HoughLinesP(image,
                                params.houghRho,
                                theta,
                                params.houghThreshold,
                                np.array([]),
                                minLineLength=params.houghMinLineLen,
                                maxLineGap=params.houghMaxLineGap)


        filteredLines = []

        if (lines is not None):
            for x1, y1, x2, y2 in lines[:,0]:
                # Calculate Line Angle
                angle = math.atan2(y2 - y1, x2 - x1) * 180.0 / np.pi
                # Ignore Horizontal Angles
                if not (-params.houghAngleIgnore < angle < params.houghAngleIgnore):
                    filteredLines.append([x1,y1,x2,y2])

        return filteredLines


    # Join Two Images
    def toWeighted(self, initialImage, image):
        return cv2.addWeighted(initialImage, 0.8, image, 1., 0.) 


    # Process Hough Lines to Find Lane Lines
    def toLaneLines(self, lines, params):
        
        linesLeft = []
        linesRight = []

        for l in lines:
            x1,y1,x2,y2 = l

            # Calculate Slope
            if x2 - x1 == 0.:
                slope = 999.
            else:
                slope = (y2 - y1) / (x2 - x1)
    
            # Separate Lines into Left and Right Lines
            if slope > 0:
                linesRight.append([x1,y1,x2,y2,slope])
            elif slope < 0:
                linesLeft.append([x1,y1,x2,y2,slope])

        # Slope
        slopeSumLeft = 0
        slopeSumRight = 0
        # Line MidPoint
        xSumLeft = 0
        ySumLeft = 0
        xSumRight = 0
        ySumRight = 0

        # Verify found Lines
        foundLeftLine = False
        foundRightLine = False
        
        if len(linesLeft) :
            foundLeftLine = True
        if len(linesRight) :
            foundRightLine = True


        # Avarege Lines
        for l in linesLeft:
            xSumLeft += (l[2]+l[0])/2
            ySumLeft += (l[3]+l[1])/2
            slopeSumLeft += l[4]

        for l in linesRight:
            xSumRight += (l[2]+l[0])/2
            ySumRight += (l[3]+l[1])/2
            slopeSumRight += l[4]

        outputLines = []
        
        if(foundLeftLine):
            slopeAvgLeft = slopeSumLeft / len(linesLeft)
            xAvgLeft = xSumLeft / len(linesLeft)
            yAvgLeft = ySumLeft / len(linesLeft)
            
            # Calculate b in y = m*x + b
            bLeft = yAvgLeft - (slopeAvgLeft*xAvgLeft)

            # Calculate x1,y1,x2,y2 Coordinates
            y1Left = self.ysize
            x1Left = (self.ysize -bLeft)/slopeAvgLeft

            # Define Upper Limit for Lines
            yLimit = max(params.y1,params.y4)*self.ysize/100

            y2Left = yLimit
            x2Left = (y2Left -bLeft)/slopeAvgLeft

            outputLines.append([x1Left, y1Left, x2Left, y2Left])

        if(foundRightLine):
            slopeAvgRight = slopeSumRight / len(linesRight)
            xAvgRight = xSumRight / len(linesRight)
            yAvgRight = ySumRight / len(linesRight)
            
            # Calculate b in y = m*x + b
            bRight = yAvgRight - (slopeAvgRight*xAvgRight)

            # Calculate x1,y1,x2,y2 Coordinates
            y1Right = self.ysize
            x1Right = (self.ysize -bRight)/slopeAvgRight

            # Define Upper Limit for Lines
            yLimit = max(params.y1,params.y4)*self.ysize/100

            y2Right = yLimit
            x2Right = (y2Right -bRight)/slopeAvgRight

            outputLines.append([x1Right, y1Right, x2Right, y2Right])


        return outputLines






    # Save Image to File
    def save(self, outputPath, params):
        cv2.imwrite(outputPath, self.getLaneLines(params))
        print("Image " + self.name + " Saved!")




    # Methods for Image Tuner GUI

    # Step 1
    # Return Original Image
    def getOriginal(self):
        return self.original

    # Step 2
    # Return Grayscale Image
    def getGrayscale(self):
        return self.toGrayscale(self.getOriginal())


    # Step 3
    # Return Canny Transform Image
    def getCanny(self, params):
        return self.toCanny(self.toGaussianBlur(self.getGrayscale(),params), params)


    # Step 4
    # Return Region of Interest Image
    def getRegion(self, params):
        return self.toRegion(self.getOriginal(), params)


    # Step 5
    # Return Hough Transform Image
    def getHough(self, params):
        return self.toHough(self.toRegion(self.getCanny(params), params),params)

    # Step 6
    # Return Final Image
    def getDone(self, params):
        return self.toWeighted(self.getOriginal(), self.getHough(params))

    # Step 7
    # Return Original Image with Lane Lines Finded
    def getLaneLines(self, params):

        houghLines = self.toHoughLines(self.toRegion(self.getCanny(params), params), params)
        lines = self.toLaneLines(houghLines,params)

        linesImage = np.zeros((self.ysize, self.xsize, 3), dtype=np.uint8)

        for l in lines:
            x1, y1, x2, y2 = l
            cv2.line(linesImage, (int(x1), int(y1)), (int(x2), int(y2)), [255, 0, 0], 20)


        return self.toWeighted(self.getOriginal(),linesImage)

    
    
