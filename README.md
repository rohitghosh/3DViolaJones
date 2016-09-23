# 2D & 3D HaarlikeFeatures for Object Detection

This software uses a single Adaboost classifier for trainig purposes. The cascade-classifieris yet to be implemented.

#### Dependencies

* numpy
* scipy
* Pillow (for drawing boxes)
* joblib

#### Datasets

* For 2D object detection, [face data from MIT](http://cbcl.mit.edu/software-datasets/FaceData2.html) was used.The data is stored as it is faces_data/ . Images are in .pgm & other formats - only .pgm files are read.

* For 3D object detection, a synthetic dataset was composed of spheres & non-spheres( cubes + cylinders). Both train & test contain 10 spheres & 10 non-spheres respectively. Each file consists of 15*15*15 voxels, with cubes/spheres/cylinders being centred at (7,7,7) but with parameters for each shape being chosen at random.It was generated using this [script](threeD_train_test_generator.py)

#### Methodology

2D Object detection was based on the famous Viola-Jones [paper](/resources/2d_haar_facedetection.pdf).

3D object detection based on Haarlike features was used by Wesrag et al for organ detection, as part of the MICCAI Grand Challenge: Prostate MR Image Segmentation 2012. The Haarfeatures include the same fetures mentioned in the [paper](/resources/A Generic Approach to Organ Detection Using 3D Haar-Like Features .pdf)

#### Object Detection

The object detection scripts can be executed from root of the repository
<code>
//For running 2D object detection
$: python 2D_HaarlikeFeatures/ViolaJones.py

// For running 3D object detection
$:python 3D_HaarlikeFeatures/threeD_violajones.py
</code>

#### Results

For 3D object detection, the best results that could be attained
<div class="message">
  Spheres detected : 4/10
  Non-spheres detected : 9/10
</div>

For 2D object detection the faces could only be detected to a certain extent. More optimisation needs to be done.
![placeholder](/images/demo.jpg)
<em>original image</em>

![placeholder](/images/final.png)
<em>detected image</em>
