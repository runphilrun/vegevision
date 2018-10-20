import numpy as np
import rasterio
from xml.dom import minidom
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


def get_TOAreflectance(image_id):
    filename='images/' + image_id  + '/' + image_id + '_3B_AnalyticMS_metadata.xml'
    xmldoc = minidom.parse(filename)
    nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")
    coeffs = {}
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ['1', '2', '3', '4']:
            i = int(bn)
            value = node.getElementsByTagName("ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)
    return coeffs


def get_bands(image_id):
    filename = 'images/' + image_id + '/' + image_id + '_3B_AnalyticMS.tif'
    with rasterio.open(filename) as src:
        blue, green, red, nir = src.read()

    TOAreflectance = get_TOAreflectance(image_id)

    blue = blue * TOAreflectance[1]
    green = green * TOAreflectance[2] 
    red = red * TOAreflectance[3] 
    nir = nir * TOAreflectance[4] 
    return blue, green, red, nir


def planet_ndvi(image_id):
    blue, green, red, nir = get_bands(image_id)

    rgb = np.dstack((red,green,blue))
    ndvi = get_ndvi(red, nir)

    show_ndvi_vs_rgb(rgb,ndvi)


def main():
    planet_ndvi('20170928_181142_1032')


if __name__ == '__main__':
    main()