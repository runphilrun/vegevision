import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import csv
import utils


def load_cmap(csv_file, name='custom_cmap'):
    '''Generate a custom colormap from a comma separated list of colors.
    The contents of the file shall contain:
        three columns (red, green, blue)
        no headers
        values between 0 and 255

    In the future this function will be updated to handle files
    containing headers and floats or hex as values.
    '''
    # read in rows as color indices
    colors = []
    with open(csv_file) as f:
        reader = csv.reader(f)
        for row in reader:
            rgb = tuple(float(c) / 255 for c in row)
            colors.append(rgb)

    # create a colorbar from list of colors
    cm = matplotlib.colors.ListedColormap(colors, name=name)
    return cm


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
    plot_ndvi(ndvi, cm=load_cmap('NDVI_VGYRM-lut.csv', name='ndvi'))

    plt.show()


def get_ndvi(red, nir):
    ''' Compute normalized difference vegetation index.
    '''
    np.seterr(divide='ignore', invalid='ignore')  # allow division by zero
    ndvi = (nir - red) / (nir + red)
    return ndvi
