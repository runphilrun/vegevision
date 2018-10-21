import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
import csv


def plot_ndvi(ndvi, cm='RdYlGn'):
    '''Display ndvi image with colormap.
    '''
    plt.imshow(ndvi, cmap=cm)
    plt.colorbar()


def show_ndvi_vs_rgb(rgb, ndvi, rgb_title='RGB', ndvi_title='NDVI'):
    '''Show RGB image and NDVI image side-by-side.
    '''
    plt.subplot(2, 1, 1)
    plt.title(rgb_title)
    plt.imshow(rgb)

    plt.subplot(2, 1, 2)
    plt.title(ndvi_title)
    plot_ndvi(ndvi)

    plt.show()


def get_ndvi(red, nir):
    ''' Compute normalized difference vegetation index.
    '''
    np.seterr(divide='ignore', invalid='ignore')  # allow division by zero
    return (nir - red) / (nir + red)
