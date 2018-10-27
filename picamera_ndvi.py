import vegevision
from pivideostream import PiVideoStream
import cv2


def picamera_ndvi(resolution=(640, 480), framerate=60):
    stream = PiVideoStream(resolution=resolution, framerate=framerate).start()

    # loop over the frames from the video stream indefinitely
    while True:
        # grab the frame from the threaded video stream
        frame = stream.read()
        b, _, r = cv2.split(frame)

        # get NDVI from RGB image
        ndvi = vegevision.get_ndvi(b, r)

        # show the frame
        cv2.imshow("Video Input with NDVI", ndvi)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

        # do a bit of cleanup
        cv2.destroyAllWindows()
        stream.stop()


def main():
    picamera_ndvi()


if __name__ == '__main__':
    main()
