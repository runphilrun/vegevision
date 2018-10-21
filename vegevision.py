import numpy as np
from matplotlib import pyplot as plt


def plot_ndvi(ndvi, cm='RdYlGn'):
    '''Display image with preset plot configurations tailored for NDVI.
    '''
    plt.imshow(ndvi, cmap=cm)
    plt.colorbar()
    plt.clim(vmin=-1, vmax=1)


def show_ndvi_vs_rgb(rgb, ndvi, rgb_title='RGB', ndvi_title='NDVI'):
    '''Show RGB image and NDVI image side-by-side.
    '''
    # plot RGB image on top
    plt.subplot(2, 1, 1)
    plt.title(rgb_title)
    plt.imshow(rgb)

    # plot NDVI image below
    plt.subplot(2, 1, 2)
    plt.title(ndvi_title)
    plot_ndvi(ndvi)

    plt.show()


def show_ndvi_vs_nir(nir, ndvi, nir_title='Near-infrared', ndvi_title='NDVI'):
    '''Show RGB image and NDVI image side-by-side.
    '''
    # plot RGB image on top
    plt.subplot(2, 1, 1)
    plt.title(nir_title)
    plt.imshow(nir, cmap='grayscale')
    plt.colorbar()

    # plot NDVI image below
    plt.subplot(2, 1, 2)
    plt.title(ndvi_title)
    plot_ndvi(ndvi)

    plt.show()


def get_ndvi(red, nir):
    ''' Compute normalized difference vegetation index.
    '''
    np.seterr(divide='ignore', invalid='ignore')  # allow division by zero
    ndvi = (nir - red) / (nir + red)
    return ndvi
