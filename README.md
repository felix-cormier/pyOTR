# Python Module for Simulating OTR Light

## Set-up

Once you've cloned the directory, there is some setup to do.

You want to use anaconda to install some packages. Make a folder in your home directory (e.g. miniconda), navigate to it,  and run

```
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh 
```

This will download and install miniconda, with prompts to decide where to install. To load the conda environment used here, simply navigate to the top directory of the repo and run

```
conda env create --file=opencv.yml
conda activate opencv
```

This conda environment should give you access to most libraries needed in this repo. If running things locally, when in the main repo directory, one should run this every new shell, except when running WCSim:

```
conda activate opencv
```

## How the code is arranged

The main steering file is called _otr\_sim\_runner.py_. Various functions are called from there.

### Generation and Propagation

Typically you can call the options

```
--doGeneration --doPropagation
```

when running _otr\_sim\_runner.py_. Generation generates light from your choice of source, while propagation propagates the light after generation is run. Code is under construction to run these and save/load the files separately. 

### Light Generation

There is a class, called _generatorConfig_ defined in _Beam/Modules/Config.py_ which sets the options for what light to generate. 

The _generate\_OTR_ function in _Beam/generate\_OTR.py_ file is called from the steering file, and the options for _generatorConfig_ (caled _generator\_options_) are defined in _generate\_OTR_. You can see a description of the options in _Beam/Modules/Config.py_. Also in the _generatorConfig_ class are definitions for reflector, foil and filament settings. Most important is the source (Laser, filament, protons), the number of rays, and the output path of image files.

### Geometry set-up

To place optical components _Geometry.py_ is used. For generation, this will be in _Beam/Modules/Geometry.py_, and for propagation in _OTR/Modules/Geometry.py_. In this file, first define the object you want to place by initializing an object of that class. All the arguments needed should be in the definition of the object in _Config.py_. Then, place the object in space, again using the X positions and angle from _Config.py_. Then, add to the system by calling AddComponent. Examples of this will already be in both _Geometry.py_ files.

When going to a new OpticalComponent, to transport photons, typically the code will transform from global to local coordinates, calculate when they intersect the component, reflect them if need be, then transform back to global. Global coordinates are right handed, with

x: left/right
y: up/down
z: in/out of page

where these directions are defined from [this image of the typical OTR arrangement](https://t2k-experiment.org/wp-content/uploads/otr_sys_rays.png).

### Light propagation

Once light has been generated, X (positions), V (direction) and general settings are passed to _pyOTR_ in _OTR/pyOTR.py_. This propagates the photons through the rest of the optical system, as defined in _OTR/Geometry.py_. Settings for the additional components, defined in _OTR/Modules/Config.py_ are added to the _generator_options_ class object through the _options_for_propagation_ function (called in _pyOTR). This ensures your changes to _OTR/Modules/Config.py_ are included in the _generator_options_ being used in the code. Typically, propagation will end in an image file. The imagePlane class stays in local coordinates after passing through it, as it is typically the last component. 

### Diagnostic images

In the _generatorConfig_ class there is a _diagnosticImage_ function which is called for every component. This will make images of the photons at every component. This should work with both parallel and not parallel photon generation. It will save them in the _output\_path_ folder. They should also be separated into transmitted and reflected photons for each surface, but this doesn't quite work. Coordinates have been hard-coded, but not all are correct. If you add a new component, you will have to add some definitions, see _Config.py_ for examples.



## To Do:
- (Done!)   Vectorize the calculations
- (Done!)   Parallelize
- (Partial) Implement all Foils
- (Done!)   Implement Mirrors
- (Done!)   Implement Image Plane
-           Implement Camera

## Updates:
Jan 22nd:
Now, pyOTR is written in a "vectorized" way and it uses parallel computing.
Instead of computing the path of each ray of light individually, it now
uses Linear Algebra to compute the path of many rays at once and it
divided the total number of rays into chuncks of data that are ran in parallel.

The gain in speed is very substantial:
In the original version, it took ~20 s to generate and trace the path of 100,000 rays.
Now, it only takes less than 2 s and 20 s can not trace 1,000,000 rays!!

## Usage:
python pyOTR.py

Note that the code is only compatible with python3.

The jupyter notebook "Examples" shows a few plots of the distribution of photons before and after passing by the Calibration Foil.

## Configuration:
The definitions of all necessary parameters to set up the simulation are in the Config.py Module.

The main ones to change right now are:

### VERBOSE (default: 0):
Set it to 1 to include debugging info.

### nrays:
Number of photons to be simulated.

### xmax:
Size of initial square side to randomly generate the photons.
