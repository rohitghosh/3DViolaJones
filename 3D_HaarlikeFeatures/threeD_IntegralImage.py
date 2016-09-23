from PIL import Image
import numpy as np

'''
In an integral image each pixel is the sum of all pixels in the original image
that are 'left and above' the pixel.

Original    Integral
+--------   +------------
| 1 2 3 .   | 0  0  0  0 .
| 4 5 6 .   | 0  1  3  6 .
| . . . .   | 0  5 12 21 .
            | . . . . . .

'''
class threeD_IntegralImage:

    def __init__(self, imageSrc = '/path', label=1, imageSrcpath = True, image = 'random'):
        if imageSrcpath:
            self.original = np.load(imageSrc)
        else:
            self.original = image
        self.sum = 0
        self.label = label
        self.calculate_integral()
        self.weight = 0

    def calculate_integral(self):
        # an index of -1 refers to the last row/column
        # since rowSum is calculated starting from (0,0),
        # rowSum(x, -1) == 0 holds for all x
        rowSum = np.zeros(self.original.shape)
        # we need an additional column and row
        self.integral = np.zeros((self.original.shape[0]+1, self.original.shape[1]+1,self.original.shape[2]+1 ))
        self.integral[1:,1:,1:] = self.original.cumsum(0).cumsum(1).cumsum(2)
        self.integral[1:,1:,0] = self.original[:,:,0].cumsum(0).cumsum(1)


    def get_area_sum(self, topLeftAbove, bottomRightBelow):
        '''
        Calculates the sum in the rectangle specified by the given tuples.
        @param topLeft: (x,y) of the rectangle's top left corner
        @param bottomRight: (x,y) of the rectangle's bottom right corner
        '''

        topLeftAbove = (int(topLeftAbove[0]), int(topLeftAbove[1]),int(topLeftAbove[2]))
        bottomRightBelow = (int(bottomRightBelow[0]), int(bottomRightBelow[1]), int(bottomRightBelow[2]))
        topLeftBelow = (topLeftAbove[0], topLeftAbove[1], bottomRightBelow[2] )
        bottomRightAbove= (bottomRightBelow[1], bottomRightBelow[0], topLeftAbove[2])

        if topLeftAbove == bottomRightBelow:
            return self.integral[topLeftAbove]
        topRightAbove = (bottomRightBelow[0], topLeftAbove[1],topLeftAbove[2])
        topRightBelow = (bottomRightBelow[0], topLeftAbove[1],bottomRightBelow[2])
        bottomLeftAbove = (topLeftAbove[0], bottomRightBelow[1],topLeftAbove[2])
        bottomLeftBelow = (topLeftAbove[0], bottomRightBelow[1],bottomRightBelow[2])

        sum_above = self.integral[bottomRightAbove] - self.integral[topRightAbove] - self.integral[bottomLeftAbove] + self.integral[topLeftAbove]
        sum_below = self.integral[bottomRightBelow] - self.integral[topRightBelow] - self.integral[bottomLeftBelow] + self.integral[topLeftBelow]

        return sum_below - sum_above

    def set_label(self, label):
        self.label = label

    def set_weight(self, weight):
        self.weight = weight
