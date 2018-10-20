# VegeVision

- Return normalized difference vegetation index (NDVI) for a region.
- Download images of the same region from different times to observe how NDVI changes with seasons.

## Usage

here are all the functions you can use and why they are here


## "SOLID" compliant approach

- connect to camera
   -  have a function "Attach to camera"
        - private functions like list connected camera

- read an image
    - pass in a camera, get back an image
    - get image from camera or get image from file without having to change program logic

- process the image
    - pass in image, return result

- save the file
    - pass in result (directory file structure and stuff hidden)
