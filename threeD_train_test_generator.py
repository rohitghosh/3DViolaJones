from __future__ import division, print_function
import numpy as np
import math

def cmask(index,radius,array):
  a,b = index
  nx,ny = array.shape
  y,x = np.ogrid[-a:nx-a,-b:ny-b]
  mask = x*x + y*y <= radius*radius
  array[mask]=1
  return array

def get_spheres(image_shape = (15,15,15),image_origin=(7,7,7), radius = 5):
    """
    Returns a patch of 3x64x64 patch centred around the nodule, with 3mm displacement in z-axis
    """

    labels = np.zeros(image_shape)

    centre = image_origin[0], image_origin[1]

    big_radius = radius
    small_radius = big_radius
    height = 0

    for height in range(int(-big_radius),int(big_radius+1)):
        small_radius = math.sqrt(big_radius**2 - height**2)
        labels[image_origin[2]+height] = cmask(centre,small_radius,labels[image_origin[2]+height])

    return labels

def get_cubes(image_shape = (15,15,15),image_origin=(7,7,7), side = 5):
    """
    Returns a patch of 3x64x64 patch centred around the nodule, with 3mm displacement in z-axis
    """

    labels = np.zeros(image_shape)

    centre = image_origin[0], image_origin[1], image_origin[2]

    labels[centre[0]-side/2:centre[0]+side/2,centre[1]-side/2:centre[1]+side/2, centre[2]-side/2:centre[2]+side/2 ] = 1

    return labels

def get_cylinders(image_shape = (15,15,15),image_origin=(7,7,7), radius = 5, height = 5):
    """
    Returns a patch of 3x64x64 patch centred around the nodule, with 3mm displacement in z-axis
    """

    labels = np.zeros(image_shape)

    centre = image_origin[0], image_origin[1]

    height_diff = height/2

    for height in range(int(-height_diff),int(height_diff+1)):
        labels[image_origin[2]+height] = cmask(centre, radius,labels[image_origin[2]+height])

    return labels

train_test_seq = np.random.randint(2, size=20)

for i in range(train_test_seq.shape[0]):
    radius = np.random.randint(low = 3, high = 15, size = 1)[0]
    radius = radius/3
    labels = get_spheres(radius = radius)
    if train_test_seq[i]==0:
        np.save('threeD_data/train/spheres/sphere_{}.npy'.format(i), labels)
    else:
        np.save('threeD_data/test/spheres/sphere_{}.npy'.format(i), labels)

shape_seq = np.random.randint(2, size=20)
for i in range(train_test_seq.shape[0]):
    a = np.random.randint(low = 3, high = 15, size = 1)[0]
    b = np.random.randint(low = 3, high = 15, size = 1)[0]
    a = a/3
    b = b/3
    if shape_seq[i]==0:
        labels = get_cubes(side = a)
        shape = 'cube'
    else:
        labels = get_cylinders(radius = a, height =b)
        shape = 'cylinder'
    if train_test_seq[i]==0:
        np.save('threeD_data/train/non_spheres/{}_{}.npy'.format(shape,i),labels)
    else:
        np.save('threeD_data/test/non_spheres/{}_{}.npy'.format(shape,i), labels)
