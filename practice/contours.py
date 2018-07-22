import argparse
import cv2
import numpy as np

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])

grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

thresh = 90
maxValue = 255
retval, t = cv2.threshold(grey, thresh, maxValue, cv2.THRESH_BINARY)

image_c, contours, hierarchy = cv2.findContours(t, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

c = cv2.drawContours(image, contours, -1, (0,255,0), 3)

print contours

cv2.imshow("Kev", np.hstack([grey]))
cv2.waitKey(0)
