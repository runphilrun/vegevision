import vegevision
from pivideostream import PiVideoStream
import cv2
import time
import os
import matplotlib.pyplot as plt
import numpy as np


def apply_custom_colormap(image_gray, cmap=plt.get_cmap('seismic')):
    '''Apply a custom colormap to a grayscale image and output the
    result as a BGR image.

    Credit: https://stackoverflow.com/a/52498778
    '''
    assert image_gray.dtype == np.uint8, 'must be np.uint8 image'
    if image_gray.ndim == 3:
        image_gray = image_gray.squeeze(-1)

    # Initialize the matplotlib color map
    sm = plt.cm.ScalarMappable(cmap=cmap)

    # Obtain linear color range
    color_range = sm.to_rgba(np.linspace(
        0, 1, 256))[:, 0:3]  # color range RGBA => RGB
    color_range = (color_range * 255.0).astype(np.uint8)  # [0,1] => [0,255]
    color_range = np.squeeze(
        np.dstack([color_range[:, 2], color_range[:, 1], color_range[:, 0]]),
        0)  # RGB => BGR

    # Apply colormap for each channel individually
    channels = [cv2.LUT(image_gray, color_range[:, i]) for i in range(3)]
    return np.dstack(channels)


def get_time_ms():
    '''Return time since epoch in milliseconds.'''
    return lambda: int(round(time.time() * 1000))


def make_dir(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def save_image(image, directory='capture/'):
    make_dir(directory)
    filename = str(get_time_ms) + '.jpg'
    cv2.imwrite(filename, image)
    print('saved {0}{1}'.format(directory, filename))


def picamera_ndvi(resolution=(640, 480), framerate=60):
    stream = PiVideoStream(resolution=resolution, framerate=framerate).start()
    print('Video stream started.')

    directory = 'capture_' + str(get_time_ms)

    # loop over the frames from the video stream indefinitely
    while True:
        # grab the frame from the threaded video stream
        frame = stream.read()
        b, _, r = cv2.split(frame)

        # get NDVI from RGB image
        ndvi = vegevision.get_ndvi(b, r)
        ndvi_colorized = apply_custom_colormap(
            ndvi, cmap=vegevision.load_cmap('NDVI_VGYRM-lut.csv'))

        # show the frame
        cv2.imshow("Video Input with NDVI", ndvi_colorized)
        print('Displaying NDVI...')
        save_image(ndvi, directory=directory)

        # if the `q` key was pressed, break from the loop
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        stream.stop()


def main():
    picamera_ndvi()


if __name__ == '__main__':
    main()
