import numpy as np
import os
import planet_api
import vegevision


def planet_ndvi(image_id):
    if not os.path.isdir('images/' + image_id):
        planet_api.download_image(image_id)
    blue, green, red, nir = planet_api.get_bands(image_id)
    rgb = np.dstack((red, green, blue))
    ndvi = vegevision.get_ndvi(red, nir)
    vegevision.show_ndvi_vs_rgb(rgb, ndvi)


def main():
    planet_ndvi('20170928_181142_1032')


if __name__ == '__main__':
    main()
