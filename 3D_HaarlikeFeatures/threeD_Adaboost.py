import numpy as np
from threeD_HaarLikeFeature import FeatureType
from threeD_HaarLikeFeature import threeD_HaarLikeFeature
from threeD_HaarLikeFeature import threeDFeatureTypes
import sys

class AdaBoost(object):
    '''
    classdocs
    '''


    def __init__(self, params):
        '''
        Constructor
        '''

def learn(positives, negatives, T , threshold):

    # construct initial weights
    pos_weight = 1. / (2 * len(positives))
    neg_weight = 1. / (2 * len(negatives))
    for p in positives:
        p.set_weight(pos_weight)
    for n in negatives:
        n.set_weight(neg_weight)

    # create column vector
    images = np.hstack((positives, negatives))

    print ('Creating haar like features..')
    features = []
    for f in threeDFeatureTypes:
        for width in range(f[0],15,f[0]):
            for breadth in range(f[1],15,f[1]):
                for height in range(f[2],15,f[2]):
                    for x in range(15-width):
                        for y in range(15-breadth):
                            for z in range(15-height):
                                features.append(threeD_HaarLikeFeature(f, (x,y,z), width, breadth, height, threshold , 1))
    print ('..done.\n. {} features created.\n'.format(len(features)))

    print ('Calculating scores for features..')
    # dictionary of feature -> list of vote for each image: matrix[image, weight, vote])
    votes = dict()
    i = 0
    for feature in features:
        # calculate score for each image, also associate the image
        feature_votes = np.array(list(map(lambda im: [im, feature.get_vote(im)], images)))
        votes[feature] = feature_votes
        i += 1
        if i % 1000 == 0:
            break   #@todo: remove
            print (' {} features of {} done'.format(i,len(features)))
    print ('..done.\n')


    # select classifiers

    classifiers = []
    used = []

    print ('Selecting classifiers..')
    sys.stdout.write('[' + ' '*20 + ']\r')
    sys.stdout.flush()
    for i in range(T):

        classification_errors = dict()

        # normalize weights
        norm_factor = 1. / sum(list(map(lambda im: im.weight, images)))
        for image in images:
            image.set_weight(image.weight * norm_factor)

        # select best weak classifier
        for feature, feature_votes in votes.items():

            if feature in used:
                continue

            # calculate error
            error = sum(list(map(lambda im, vote: im.weight if im.label != vote else 0, feature_votes[:,0], feature_votes[:,1])))
            # map error -> feature, use error as key to select feature with
            # smallest error later
            classification_errors[error] = feature

        # get best feature, i.e. with smallest error
        errors = list(classification_errors.keys())
        best_error = errors[np.argmin(errors)]
        feature = classification_errors[best_error]
        used.append(feature)
        feature_weight = 0.5 * np.log((1-best_error)/best_error)

        classifiers.append((feature, feature_weight))

        # update image weights
        best_feature_votes = votes[feature]
        for feature_vote in best_feature_votes:
            im = feature_vote[0]
            vote = feature_vote[1]
            if im.label != vote:
                im.set_weight(im.weight * np.sqrt((1-best_error)/best_error))
            else:
                im.set_weight(im.weight * np.sqrt(best_error/(1-best_error)))

        sys.stdout.write('[' + '='*int(((i+1)*20)/T) + ' '*int(20-(((i+1)*20)/T)) + ']\r')
        sys.stdout.flush()
    print ('..done.\n')

    return classifiers
