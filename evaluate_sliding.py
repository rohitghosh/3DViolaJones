from skimage import color
from scipy import misc
from IntegralImage import IntegralImage
from skimage.transform import pyramid_reduce
import numpy as np
import pdb

def classify(classifiers, image):
    return sum([c[0].get_vote(image) * c[1] for c in classifiers])
    #return 1 if sum([c[0].get_vote(image) * c[1] for c in classifiers]) >= 1 else -1

def evaluate_pic(classifier,path):
    stride = (20,20)
    window_size = (100,100)#heuristically chosen for this image


    img = color.rgb2gray(misc.imread(path))
    h,w = img.shape

    delta_x,delta_y = stride

    x_list = range(0,w-window_size[1]+1,delta_x)
    y_list = range(0,h-window_size[0]+1,delta_y)


    lis=[]
    for w in x_list:
        for h in y_list:
            #downscale value also heurestically chosen
            im = img[h:h+window_size[0],w:w+window_size[1]]
            im = pyramid_reduce(img[h:h+window_size[0],w:w+window_size[1]],downscale=5)
            #im = np.array(im[:,:] * 255, dtype = np.uint8)
            im = IntegralImage(image=im, imageSrcpath = False)
            lis.append(im)

    import pickle
    pickle.dump( lis, open( "test-windows.pkl", "wb" ) )
    #lis = pickle.load( open( "test-windows.pkl", "rb" ) )


    ##Finding-windows
    k = len(lis)/10 #no of chunks, jobs
    k=1
    iterator = range(0,len(lis),k)
    print (len(lis))
    from joblib import Parallel, delayed
    # from parr_test import myfunc

    #pdb.set_trace()

    results_lists = Parallel(n_jobs=-1)(delayed(classify)(classifier,lis[i]) for i in iterator)
    results = [+1 if i > 2 else -1 for i in results_lists ]
    print (len(results))
    print (sum(results))
    #print (results_lists)


    # if len(lis[iterator[-1]+k:]) >= 2:
    #     results.append(classify(classifier,lis[iterator[-1]+k:]))

    detects = np.array(results)

    ##Plotting result
    windows=[]
    for w in x_list:
        for h in y_list:
            windows.append((h,w))

    ind = np.where(detects==1)[0]

    ws1=[]
    for i in ind:
        ws1.append(windows[i])

    #http://www.nafisahmad.com/2014/10/how-to-draw-rectangle-with-more-then.html
    from PIL import Image, ImageDraw
    pil_img = Image.open(path)
    dr = ImageDraw.Draw(pil_img)
    for h,w in ws1:
        cor = (w,h,w+window_size[1],h+window_size[0])
        dr.rectangle(cor, outline="red")

    pil_img.save('final.png')
