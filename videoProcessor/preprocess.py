import cv2
import PIL
import numpy
from PIL import Image

class Preprocessor:
    def __init__(self, width, height, frames):
        self.width = width
        self.height = height
        self.frames = frames

    def resize(self, img):
        return cv2.resize(img, (self.width, self.height))

    def detectOutline(self, img):
        width, height = img.size
        array = numpy.array(img)
        out = numpy.zeros((height, width, 3), numpy.uint8)
        def isValid(x, y):
            return not (x<0 or x>=width or y<0 or y>=height)

        def findDist(r1, g1, b1, r2, g2, b2):
            r1 = int(r1)
            g1 = int(g1)
            b1 = int(b1)
            r2 = int(r2)
            g2 = int(g2)
            b2 = int(b2)
            rDiff = r1-r2
            gDiff = g1-g2
            bDiff = b1-b2
            return (rDiff**2 + gDiff**2 + bDiff**2)**(1/2)

        diffSum = 0
        diffs = numpy.zeros((height, width), numpy.uint16)
        for y in range(height):
            for x in range(width):
                thisDiff = 0
                if (isValid(x-1, y) and isValid(x+1, y)):
                    dist = findDist(array[y, x-1, 0], array[y, x-1, 1], array[y, x-1, 2],
                                 array[y, x+1, 0], array[y, x+1, 1], array[y, x+1, 2])
                    if (dist > thisDiff):
                        thisDiff = dist

                if (isValid(x, y-1) and isValid(x, y+1)):
                    dist = findDist(array[y-1, x, 0], array[y-1, x, 1], array[y-1, x, 2],
                                 array[y+1, x, 0], array[y+1, x, 1], array[y+1, x, 2])
                    if (dist > thisDiff):
                        thisDiff = dist

                diffSum += thisDiff
                diffs[y, x] = thisDiff

        diffThreshold = diffSum / (height * width)
        diffOver = 0
        for y in range(height):
            for x in range(width):
                if int(diffs[y, x]) > diffThreshold:
                    diffOver += int(diffs[y, x]) - diffThreshold


        diffAbove = diffOver / (height * width)


        for y in range(height):
            for x in range(width):
                if int(diffs[y, x]) > diffThreshold + diffAbove:
                    out[y, x, 0] = 0
                    out[y, x, 1] = 0
                    out[y, x, 2] = 0

                else:
                    out[y, x, 0] = 255
                    out[y, x, 1] = 255
                    out[y, x, 2] = 255

        return Image.fromarray(out.squeeze())


    def convertToOpenCV(self, img):
        return numpy.array(img)[:,:,::-1].copy()

