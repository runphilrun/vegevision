import rasterio
from xml.dom import minidom
import os
import json
import requests


def download_image(image_id):
    '''Download image from Planet API.
    This function requires the user to have a valid API key as
    an environment variable.

    References:
        https://github.com/planetlabs/notebooks/blob/master/jupyter-notebooks/data-api-tutorials/planet_data_api_introduction.ipynb

        https://developers.planet.com/docs/quickstart/downloading-imagery/
    '''
    # get api key
    PLANET_API_KEY = os.getenv('PL_API_KEY')

    # Setup Planet Data API base URL
    base_url = 'https://api.planet.com/data/v1'
    item_type = 'PSScene4Band'
    asset_types = ['analytic', 'analytic_xml']

    # Setup the session
    session = requests.Session()

    # Authenticate
    session.auth = (PLANET_API_KEY, '')

    # Make a GET request to the Planet Data API
    item = session.get((base_url + '{}/items/{}/assets/').format(
        item_type, image_id))

    # extract the activation url from the item for the desired asset
    for asset_type in asset_types:
        item_activation_url = item.json()[asset_type]["_links"]["activate"]

        # request activation
        response = session.post(item_activation_url)
        print('Asset {0} for image id {1} completed with status: {2}'.format(
            asset_type, image_id, response.status_code))
        if not ((response.status_code == 200) or
                (response.status_code == 204)):
            raise Exception(
                'Request failed with status code %s' % response.status_code)


def get_TOAreflectance(image_id):
    '''Load top of atmosphere reflectance coefficients from image metadata.
    '''
    # read data from file
    filename = 'images/{0}/{0}_3B_AnalyticMS_metadata.xml'.format(image_id)
    if not os.path.isfile(filename):
        raise Exception('File %s does not exist.' % filename)

    # parse reflectance coefficients from xml data
    xmldoc = minidom.parse(filename)
    nodes = xmldoc.getElementsByTagName("ps:bandSpecificMetadata")
    coeffs = {}
    for node in nodes:
        bn = node.getElementsByTagName("ps:bandNumber")[0].firstChild.data
        if bn in ['1', '2', '3', '4']:
            i = int(bn)
            value = node.getElementsByTagName(
                "ps:reflectanceCoefficient")[0].firstChild.data
            coeffs[i] = float(value)
    return coeffs


def get_bands(image_id):
    ''' Get individual color bands (Blue, Green, Red, Near-infrared) from
    PlanetScope4Band assets normalized by top-of-atmosphere reflectance.
    '''
    # check if the image file exists
    filename = 'images/' + image_id + '/' + image_id + '_3B_AnalyticMS.tif'
    if not os.path.isfile(filename):
        raise Exception('File %s does not exist.' % filename)

    # read color channels from image file
    with rasterio.open(filename) as src:
        blue, green, red, nir = src.read()

    # normalize image by top of atmosphere reflectance
    TOAreflectance = get_TOAreflectance(image_id)
    blue = blue * TOAreflectance[1]
    green = green * TOAreflectance[2]
    red = red * TOAreflectance[3]
    nir = nir * TOAreflectance[4]

    return blue, green, red, nir
