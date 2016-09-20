
def enum(**enums):
    return type('Enum', (), enums)

FeatureType = enum(ONE_X = (2,1,1), ONE_Y = (1,2,1), ONE_Z = (1,1,2), TWO_X_Y = (2,2,1), TWO_Y_Z =(1,2,2), TWO_X_Z= (1,2,1), THREE_X_Y_Z = (2,2,2), ALL= (1,1,1,))
threeDFeatureTypes = [FeatureType.ONE_X, FeatureType.ONE_Y, FeatureType.ONE_Z, FeatureType.TWO_X_Y, FeatureType.TWO_Y_Z, FeatureType.TWO_X_Z, FeatureType.THREE_X_Y_Z, FeatureType.ALL]

class threeD_HaarLikeFeature(object):
    '''
    classdocs
    '''


    def __init__(self, feature_type, position, width, breadth, height, threshold, polarity):
        '''
        @param feature_type: see FeatureType enum
        @param position: top left corner where the feature begins (tuple)
        @param width: width of the feature
        @param height: height of the feature
        @param threshold: feature threshold
        @param polarity: polarity of the feature (-1, 1)
        '''
        self.type = feature_type
        self.top_left_above = position
        self.bottom_right_below = (position[0] + width, position[1] + breadth, position[2] + height)
        self.width = width
        self.height = height
        self.breadth = breadth
        self.threshold = threshold
        self.polarity = polarity

    def get_score(self, intImage):
        score = 0
        if self.type == FeatureType.ONE_Z:
            midway_first = (self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth, self.top_left_above[2] + self.height/2)
            first = intImage.get_area_sum(self.top_left_above, midway_first)
            midway_second = (self.top_left_above[0], self.top_left_above[1], self.top_left_above[2] + self.height/2)
            second = intImage.get_area_sum(midway_second, self.bottom_right_below)
            score = first - second
        elif self.type== FeatureType.ONE_Y:
            midway_first = (self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth/2, self.top_left_above[2] + self.height)
            first = intImage.get_area_sum(self.top_left_above, midway_first)
            midway_second = (self.top_left_above[0], self.top_left_above[1] + self.breadth/2,self.top_left_above[2] )
            second = intImage.get_area_sum(midway_second, self.bottom_right_below)
            score = first - second
        elif self.type== FeatureType.ONE_X:
            midway_first = (self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth, self.top_left_above[2] + self.height)
            first = intImage.get_area_sum(self.top_left_above, midway_first)
            midway_second = (self.top_left_above[0]+ self.width/2, self.top_left_above[1],self.top_left_above[2] )
            second = intImage.get_area_sum(midway_second, self.bottom_right_below)
            score = first - second
        elif self.type == FeatureType.TWO_X_Y:
            first = intImage.get_area_sum(self.top_left_above, (self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2,self.top_left_above[2]+self.height ))
            second = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2,self.top_left_above[2]), self.bottom_right_below)
            third = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1] ,self.top_left_above[2]),(self.top_left_above[0] + self.width, self.top_left_above[1]+ breadth/2 ,self.top_left_above[2]+self.height))
            fourth = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1]+ self.breadth/2 ,self.top_left_above[2]),(self.top_left_above[0] + self.width/2, self.top_left_above[1]+ breadth ,self.top_left_above[2]+ self.height))
            score = first + second - third - fourth
        elif self.type == FeatureType.TWO_X_Z:
            first = intImage.get_area_sum(self.top_left_above, (self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth,self.top_left_above[2] + self.height/2 ))
            second = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1],self.top_left_above[2] +self.height/2 ), self.bottom_right_below)
            third = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1] ,self.top_left_above[2]),(self.top_left_above[0] + self.width, self.top_left_above[1]+ breadth ,self.top_left_above[2]+self.height/2))
            fourth = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1] ,self.top_left_above[2] + self.height/2),(self.top_left_above[0] + self.width/2, self.top_left_above[1]+ breadth ,self.top_left_above[2]+self.height))
            score = first + second - third - fourth
        elif self.type == FeatureType.TWO_Y_Z:
            first = intImage.get_area_sum(self.top_left_above, (self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth/2,self.top_left_above[2] + self.height/2 ))
            second = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1] + self.breadth/2,self.top_left_above[2] +self.height/2 ), self.bottom_right_below)
            third = intImage.get_area_sum((self.top_left_above[0] , self.top_left_above[1] + self.breadth/2 ,self.top_left_above[2]),(self.top_left_above[0] + self.width, self.top_left_above[1]+ breadth ,self.top_left_above[2]+ self.height/2))
            fourth = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1] ,self.top_left_above[2] + self.height/2),(self.top_left_above[0] + self.width, self.top_left_above[1]+ breadth/2 ,self.top_left_above[2]+ self.height))
            score = first + second - third - fourth
        elif self.type == FeatureType.THREE_X_Y_Z:
            first = intImage.get_area_sum(self.top_left_above, (self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2,self.top_left_above[2] + self.height/2 ))
            second = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2,self.top_left_above[2]),(self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth, self.top_left_above[2] + self.height/2))
            third = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1] + self.breadth/2,self.top_left_above[2] + self.height/2),(self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth, self.top_left_above[2] + self.height))
            fourth = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1],self.top_left_above[2] + self.height/2),(self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth/2, self.top_left_above[2] + self.height))

            fifth = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2,self.top_left_above[2] +self.height/2 ), self.bottom_right_below)
            sixth = intImage.get_area_sum((self.top_left_above[0] + self.width/2, self.top_left_above[1],self.top_left_above[2]),(self.top_left_above[0] + self.width, self.top_left_above[1] + self.breadth/2 ,self.top_left_above[2] + self.height/2))
            seventh = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1] + self.breadth/2, self.top_left_above[2]),(self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth ,self.top_left_above[2] + self.height/2))
            eighth = intImage.get_area_sum((self.top_left_above[0], self.top_left_above[1],self.top_left_above[2]+self.height/2),(self.top_left_above[0] + self.width/2, self.top_left_above[1] + self.breadth/2 ,self.top_left_above[2] + self.height))
            score = first + second + third + fourth - fifth - sixth - seventh - eighth
        elif self.type == FeatureType.ALL:
            score = intImage.get_area_sum(self.top_left_above, self.bottom_right_below)
        return score

    def get_vote(self, intImage):
        score = self.get_score(intImage)
        return 1 if score < self.polarity*self.threshold else -1
