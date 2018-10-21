# Computing NDVI with Python

Return [normalized difference vegetation index (NDVI)](https://developers.planet.com/tutorials/calculate-ndvi/) for an image.

## Vegevision

`vegevision.py` is a set of tools for calculating and displaying NDVI from two images. The functions assume that a "red" image is a grayscale image of the response to light between 0.4 to 0.7 micron, and "near-infrared" is a grayscale image of the response to light between 0.7 to 1.1 micron. Images are assumed to be in `float32` format (values between 0 and 1).

### Using Vegevision

```python
import numpy as np
import vegevision

blue, green, red, nir = np.split(imageWith4Bands)
ndvi = vegevision.get_ndvi(red,nir)
```

### Future plans for Vegevision

- Add examples for camera inputs (webcams or Raspberry Pi cameras)
- File saving with colormap
- Custom colormaps for NDVI (see: [NDVI_VGYRM-lut.csv](NDVI_VGYRM-lut.csv) as developed by [cfastie](https://publiclab.org/notes/cfastie/08-26-2014/new-ndvi-colormap))

The idea behind this repository is to build a set of tools with `vegevision.py` which can be run with different image sources and produce consistent results. In the following example, Vegevision is applied to images from Planet's constellation.


## Planet NDVI

PlanetScope data collected by Dove satellites can be requested through the Planet API as `.tif` images. The images have 4 bands: blue, green, red, and near-infrared, and also come with coefficients to normalize "top of atmosphere reflectance" so that images from two different times can be compared.

### Using Planet NDVI

Download assets of the type `analytic` and `analytic_xml` from `PSScene4Band`. Save the assets in a folder called `images/`. 

This example uses the image id `20170928_181142_1032`.

```python
planet_ndvi.py
```

This returns the following plot.

![NDVI for item id 20170928_181142_1032](NDVI.png)

### Future plans for Planet NDVI

- Automatically download images from Planet API if they are not found locally.
- Plot images of the same region from different times to observe how NDVI changes with seasons.
- Save NDVI plots as an animation.
