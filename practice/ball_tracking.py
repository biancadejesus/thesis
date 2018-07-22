from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# construct argument parse and parse arguments

ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
                help="max buffer size")
args = vars(ap.parse_args())

# define lower and upper boundaries of [colour] object in HSV colour space and
# initialise list of tracked points

# green
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if no video path is supplied, grab webcam reference, otherwise, grab
# reference to video file

if not args.get("video", False):
    camera = cv2.VideoCapture(0)
else:
    camera = cv2.VideoCapture(args["video"])

# LOOP

while True:
    # grab current frame
    (grabbed, frame) = camera.read()

    # if viewing video and no frame grabbed, the end was reached
    if args.get("video") and not grabbed:
        break

    # resize frame, blur, and convert to HSV colour space
    frame = imutils.resize(frame, width=600)
    frame = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # construct mask for each colour
    mask_green = cv2.inRange(hsv, greenLower, greenUpper)
    mask_green = cv2.erode(mask_green, None, iterations=2)
    mask_green = cv2.dilate(mask_green, None, iterations=2)

    # find contours in mask and initialise current centre of ball (x, y)
    cnts = cv2.findContours(mask_green.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    centre = None

    # only proceed if at least one contour found
    if len(cnts) > 0:
        # find longest contour in mask, use to compute min enclosing circle
        # and centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        centre = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if radius meets min size
        if radius > 10:
            # draw circle and centroid on frame, then update list of tracked
            # points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                       (0, 255, 255), 2)

    # updates the points queue
    pts.appendleft(centre)

    # loop over set of tracked points
    for i in range(1, len(pts)):
        # if either tracked point is None, ignore them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise compute the thickness of the line and draw connecting lines
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

    # show frame on screen
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# clean up camera and close any open windows
camera.release()
cv2.destroyAllWindows()
