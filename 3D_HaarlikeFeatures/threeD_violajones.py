from threeD_Adaboost import learn
from threeD_IntegralImage import threeD_IntegralImage
import os


def load_images(path, label):
    images = []
    for _file in os.listdir(path):
        if _file.endswith('.npy'):
            images.append(threeD_IntegralImage(os.path.join(path, _file), label=label, imageSrcpath = True))
    return images

def classify(classifiers, image, threshold = 0):
    return 1 if sum([c[0].get_vote(image) * c[1] for c in classifiers]) >= threshold else -1



if __name__ == "__main__":

    # TODO: attentional cascading

    best_accuracy= 0
    T = 90

    for threshold in [-1, 0, 1]:
        print ("======================================================================")
        print ("Checking for threshold {}\n\n".format(threshold))

        print ('Loading spheres..')
        spheres = load_images('/home/users/rohitg/Viola-Jones/threeD_data/train/spheres', 1)
        print ('..done. {} spheres loaded.\n\nLoading non spheres..'.format(len(spheres)))
        non_spheres = load_images('/home/users/rohitg/Viola-Jones/threeD_data/train/non_spheres', -1)
        print ('..done. {} non spheres loaded.\n'.format(len(non_spheres)))


        classifiers = learn(spheres, non_spheres, T, threshold)


        print ('Loading test spheres..')
        spheres = load_images('/home/users/rohitg/Viola-Jones/threeD_data/test/spheres', 1)
        print ('..done. {} spheres loaded.\n\nLoading test non spheres..',format(len(spheres)))
        non_spheres = load_images('/home/users/rohitg/Viola-Jones/threeD_data/test/non_spheres', -1)
        print ('..done. {} non spheres loaded.\n',format(len(non_spheres)))

        print ('Validating selected classifiers..')
        correct_spheres = 0
        correct_non_spheres = 0
        for image in spheres + non_spheres:
            result = classify(classifiers, image, threshold = threshold)
            if image.label == 1 and result == 1:
                correct_spheres += 1
            if image.label == -1 and result == -1:
                correct_non_spheres += 1
        accuracy = (correct_spheres + correct_non_spheres)/(len(spheres)+len(non_spheres))
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_correct_spheres = correct_spheres
            best_correct_non_spheres = correct_non_spheres
            best_threshold = threshold


    print ('..done. Best Result for threshold {}:\n  spheres: {}/{}\n  non-spheres: {}/{}'.format(best_threshold,best_correct_spheres,len(spheres), best_correct_non_spheres,len(non_spheres)))
