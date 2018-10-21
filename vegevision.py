import numpy as np
import planet_api
from matplotlib import pyplot as plt
from matplotlib import colors
import csv


def plot_ndvi(ndvi,cm='RdYlGn'):
    '''Display ndvi image with colormap.
    '''
    plt.imshow(ndvi, cmap=cm)
    plt.colorbar()


def show_ndvi_vs_rgb(rgb, ndvi):
    plt.subplot(2,1,1)
    plt.title('RGB (normalized reflectance)')
    plt.imshow(rgb)

    plt.subplot(2,1,2)
    plt.title('NDVI')
    plot_ndvi(ndvi)

    plt.show()


def get_ndvi(red,nir):
    ''' Compute normalized difference vegetation index.
    '''
    np.seterr(divide='ignore', invalid='ignore') # allow division by zero
    return (nir-red)/(nir+red)


def planet_ndvi(image_id):
    blue, green, red, nir = planet_api.get_image(image_id)

    rgb = np.dstack((red,green,blue))
    ndvi = get_ndvi(red, nir)

    show_ndvi_vs_rgb(rgb,ndvi)


def main():
    planet_ndvi('20170928_181142_1032')


if __name__ == '__main__':
    main()