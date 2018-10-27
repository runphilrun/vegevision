import vegevision
from pivideostream import PiVideoStream
import cv2
import time
import os


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


def picamera_ndvi(resolution=(640, 480), framerate=60):
    stream = PiVideoStream(resolution=resolution, framerate=framerate).start()
    directory = 'capture_' + str(get_time_ms)
    # loop over the frames from the video stream indefinitely
    while True:
        # grab the frame from the threaded video stream
        frame = stream.read()
        b, _, r = cv2.split(frame)

        # get NDVI from RGB image
        ndvi = vegevision.get_ndvi(b, r)

        # show the frame
        cv2.imshow("Video Input with NDVI", ndvi)
        save_image(ndvi)

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
