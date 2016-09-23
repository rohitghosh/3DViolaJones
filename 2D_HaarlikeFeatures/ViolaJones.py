from AdaBoost import learn
from IntegralImage import IntegralImage
import os
from  evaluate_sliding import evaluate_pic


def load_images(path, label):
    images = []
    for _file in os.listdir(path):
        if _file.endswith('.pgm'):
            images.append(IntegralImage(os.path.join(path, _file), label=label, imageSrcpath = True))
    return images

def classify(classifiers, image, threshold):
    return 1 if sum([c[0].get_vote(image) * c[1] for c in classifiers]) >= threshold else -1



if __name__ == "__main__":

    # TODO: attentional cascading

    best_accuracy= 0
    T = 20


    for threshold in [-1, 0, 1]:
        print ("======================================================================")
        print ("Checking for threshold {}\n\n".format(threshold))


        print ('Loading faces..')
        faces = load_images('faces_data/faces_train/train/face', 1)
        print ('..done. {} faces loaded.\n\nLoading non faces..'.format(len(faces)))
        non_faces = load_images('faces_data/faces_train/train/non-face', -1)
        print ('..done. {} non faces loaded.\n'.format(len(non_faces)))

        classifiers = learn(faces, non_faces, T, threshold)

        print ('Loading test faces..')
        faces = load_images('faces_data/faces_test/test/face', 1)
        print ('..done. {} faces loaded.\n\nLoading test non faces..'.format(len(faces)))
        non_faces = load_images('faces_data/faces_test/test/non-face', -1)
        print ('..done. {} non faces loaded.\n'.format(len(non_faces)))

        print ('Validating selected classifiers..')
        correct_faces = 0
        correct_non_faces = 0
        for image in faces + non_faces:
            result = classify(classifiers, image, threshold)
            if image.label == 1 and result == 1:
                correct_faces += 1
            if image.label == -1 and result == -1:
                correct_non_faces += 1
        accuracy = (correct_faces + correct_non_faces)/(len(faces)+len(non_faces))
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_correct_faces = correct_faces
            best_correct_non_faces = correct_non_faces
            best_threshold = threshold
            best_classifiers = classifiers
    print ('..done. Best Result for threshold of {}:\n  Faces: {}/{}\n  non-Faces: {}/{}\n '.format(best_threshold,best_correct_faces,len(faces),best_correct_non_faces,len(non_faces)))

    print ('Evaluating best classifier on demo pic')
    path = 'images/demo.jpg'
    evaluate_pic(best_classifiers,path, best_threshold, stride_size = 20, window_length = 100)
