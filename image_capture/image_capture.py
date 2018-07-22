# image_capture.py
# capture image from webcam feed

# RAW VIDEO RETURN

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

# SETUP CAPTURE SESSION
set_name = raw_input("Enter set (varied condition): ")
print set_name
input_name = raw_input("Input name (sign or gesture): ")
print input_name
number = raw_input("Input number: ")
print number
file_name = set_name + "_" + input_name + "_" + number
print file_name

path = 'C:/Users/bianc/Documents/University/Thesis/Images/Test'

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
    frame = imutils.resize(frame, width=1000)

    # DISPLAY
    cv2.putText(frame,
                "Space - Capture, Esc - Quit",
                (50, 700),  # position - bottom left corner of text
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,                # font size
                (255, 255, 255),    # font colour
                1,                  # line thicknes
                cv2.LINE_AA)        # line type - stick with cv2.LINE_AA

    cv2.imshow("frame", frame)



    # INPUT HANDLING #
    k = cv2.waitKey(5)

    # IMAGE CAPTURE - Space
    if k == 32:
        file_name = set_name + "_" + input_name + "_" + number
        write_to = path + '/' + file_name + '.jpg'
        cv2.imwrite(write_to, frame)
        print 'captured!'
        print 'File name: ' + file_name + '.jpg'
        number = str(int(number) + 1)

    # Quit - esc
    elif k == 27:
        camera.release()
        cv2.destroyAllWindows()
        break
