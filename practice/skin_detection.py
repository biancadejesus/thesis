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

# define the upper and lower boundaries of the HSV pixel
# intensities to be considered 'skin'
# lower = np.array([0, 48, 80], dtype = "uint8")
# upper = np.array([20, 255, 255], dtype = "uint8")

# if hue value loops around, need to define two separate boundaries
# keep everything else the same

# lower_1 = np.array([0, 80, 95], dtype="uint8")
# upper_1 = np.array([3, 145, 105], dtype="uint8")

# lower_2 = np.array([220, 135, 95], dtype="uint8")
# upper_2 = np.array([255, 255, 255], dtype="uint8")

lower_1 = np.array([0, 48, 50], dtype="uint8")
upper_1 = np.array([20, 255, 255], dtype="uint8")

lower_2 = np.array([250, 48, 50], dtype="uint8")
upper_2 = np.array([255, 255, 255], dtype="uint8")

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

    converted = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    skinMask_1 = cv2.inRange(converted, lower_1, upper_2)
    skinMask_2 = cv2.inRange(converted, lower_2, upper_2)

    skinMask = skinMask_1 + skinMask_2      # add masks together

    # apply a series of erosions and dilations to the mask
    # using an elliptical kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
    skinMask = cv2.erode(skinMask, kernel, iterations=2)
    skinMask = cv2.dilate(skinMask, kernel, iterations=2)

    # blur the mask to help remove noise, then apply the
    # mask to the frame
    skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
    skin = cv2.bitwise_and(frame, frame, mask=skinMask)

    # create binary mask
    grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    grey = imutils.resize(grey, width=600)
    thresh = 90
    maxValue = 255

    retval, binary = cv2.threshold(grey, thresh, maxValue, cv2.THRESH_BINARY)

    masked = cv2.bitwise_and(frame, frame, mask=binary)

    # hand contours
    image, contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # show the skin in the image along with the mask
    c = cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
    cv2.imshow("Image", binary)


    # cv2.imshow("images", np.hstack([c]))

    # if the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
