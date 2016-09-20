from threeD_Adaboost import learn
from threeD_IntegralImage import threeD_IntegralImage
import os
from  evaluate_sliding import evaluate_pic


def load_images(path, label):
    images = []
    for _file in os.listdir(path):
        if _file.endswith('.npy'):
            images.append(threeD_IntegralImage(os.path.join(path, _file), label=label, imageSrcpath = True))
    return images

def classify(classifiers, image):
    return 1 if sum([c[0].get_vote(image) * c[1] for c in classifiers]) >= 0 else -1



if __name__ == "__main__":

    # TODO: select optimal threshold for each feature
    # TODO: attentional cascading

    print 'Loading spheres..'
    spheres = load_images('/home/rohit/Viola-Jones/threeD_data/train/spheres', 1)
    print '..done. ' + str(len(spheres)) + ' spheres loaded.\n\nLoading non spheres..'
    non_spheres = load_images('/home/rohit/Viola-Jones/threeD_data/train/non_spheres', -1)
    print '..done. ' + str(len(non_spheres)) + ' non spheres loaded.\n'

    T = 20
    classifiers = learn(spheres, non_spheres, T)
    # path = '/home/rohit/dlib/examples/spheres/2008_001009.jpg'
    # evaluate_pic(classifiers,path)
    print 'Loading test spheres..'
    spheres = load_images('/home/rohit/Viola-Jones/threeD_data/test/spheres', 1)
    print '..done. ' + str(len(spheres)) + ' spheres loaded.\n\nLoading test non spheres..'
    non_spheres = load_images('/home/rohit/Viola-Jones/threeD_data/test/non_spheres', -1)
    print '..done. ' + str(len(non_spheres)) + ' non spheres loaded.\n'

    print 'Validating selected classifiers..'
    correct_spheres = 0
    correct_non_spheres = 0
    for image in spheres + non_spheres:
        result = classify(classifiers, image)
        if image.label == 1 and result == 1:
            correct_spheres += 1
        if image.label == -1 and result == -1:
            correct_non_spheres += 1

    print '..done. Result:\n  spheres: ' + str(correct_spheres) + '/' + str(len(spheres)) + '\n  non-spheres: ' + str(correct_non_spheres) + '/' + str(len(non_spheres))
