# import the necessary packages
import imutils
import numpy as np
import argparse
import cv2

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# if a video path was not supplied, grab the reference
# to the gray
if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, load the video
else:
    camera = cv2.VideoCapture(args["video"])

    # keep looping over the frames in the video
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a
    # frame, then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, convert it to the HSV color space,
    # and determine the HSV pixel intensities that fall into
    # the speicifed upper and lower boundaries
    frame = imutils.resize(frame, width=600)

    # MESS WITH STUFF HERE
    # START

    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    thresh = 90
    maxValue = 255
    retval, t = cv2.threshold(grey, thresh, maxValue, cv2.THRESH_BINARY)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (1, 1))
    t = cv2.erode(t, kernel, iterations=2)
    t = cv2.dilate(t, kernel, iterations=2)
    t = cv2.GaussianBlur(t, (3, 3), 0)

    image_c, contours, hierarchy = cv2.findContours(t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    c = cv2.drawContours(frame, contours, -1, (0, 0, 255), 2)

    if len(contours) != 0:
        cnt = max(contours, key=cv2.contourArea)
        hull = cv2.convexHull(cnt)

        shell = cv2.drawContours(frame, [hull], -1, (0,255,0), 3)

        cv2.imshow("image", np.hstack([shell]))

    # END


    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
