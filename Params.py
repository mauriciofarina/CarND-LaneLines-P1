import json

class Params(object):

    def __init__(self, paramsPath):

        # Loads Params From File
        try:
            with open(paramsPath) as jsonFile:
                data = json.load(jsonFile)
            self.__dict__ = json.loads(data)

        # If Params File Do Not Exists
        except:
            print("Loading default Params")
            # Region Points
            self.x1 = 47
            self.y1 = 60
            self.x2 = 13
            self.y2 = 100
            self.x3 = 93
            self.y3 = 100
            self.x4 = 53
            self.y4 = 60

            # Gaussian Filter Params
            self.gaussianKernel = 5

            # Canny Transform Params
            self.cannyLowThreshold = 50
            self.cannyHighThreshold = 150

            # Hough Transform Params
            self.houghRho = 2
            self.houghTheta = 180
            self.houghThreshold = 15
            self.houghMinLineLen = 40
            self.houghMaxLineGap = 20
            self.houghAngleIgnore = 0

        self.validator()

            
    # Fix Bad Values
    def validator(self):
        
        # Gaussian Blur
        if (self.gaussianKernel <= 0):
            self.gaussianKernel = 1
        if (self.gaussianKernel%2==0):
            self.gaussianKernel -= 1
        
        # Hough Transform
        if self.houghRho < 1:
            self.houghRho = 1

        if self.houghTheta == 0:
            self.houghTheta = 1


    # Save Params to JSON File
    def save(self, fileName):
        s = json.dumps(self.__dict__)
        with open(fileName, 'w') as outfile:  
            json.dump(s, outfile)
        print("Params Saved")
