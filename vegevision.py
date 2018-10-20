import numpy
import rasterio
from xml.dom import minidom
from matplotlib import pyplot as plt


def show_image(image):
    '''Display image with colormap.
    '''
    plt.imshow(image, cmap='summer')
    plt.show()


def ndvi(red,nir):
    ''' Compute normalized difference vegetation index.
    '''
    numpy.seterr(divide='ignore', invalid='ignore') # allow division by zero
    return (nir-red)/(nir+red)


def planet_ndvi(image_id):
    image_name=image_id + "_3B_AnalyticMS.tif"
    with rasterio.open(image_name) as src:
        blue, green, red, nir = src.read()

    show_image(ndvi(red,nir))


def main():
    planet_ndvi(
        "images/20170928_181142_1032/20170928_181142_1032")


if __name__ == '__main__':
    main()