# Gaze-Analyser
## This script was built to implement the algorithm outlined in "A Study of Non-Invasive Gaze Detection Methods" by George Markham
### Written for an undergraduate dissertation project at the University of Lincoln investigating non-invasive gaze detection

To run with default system webcam:

```
python CMP3060M_project_implementation.py c 0
```

To run with image:

```
python CMP3060M_project_implementation.py i ./path/to/image.jpg
```

To specify distance (z is distance from camera in meters):

```
python CMP3060M_project_implementation.py c 0 z 1
```

** DISCLAIMER: USE YOUR OWN MICROSOFT AZURE API KEY **

** DISCLAIMER: CALIBRATION MATRIX SHOULD BE PROVIDED AS A NPZ FILE **