# skin_detection_dynamic.py
# creates a mask based on a given sample that filters out the background
# take a sample of 

hsv = cv2.cvtColor(frame, cv2.COLOUR_BGR2HSV)
dst = cv2.calcBackProject([hsv], [0,1], hist, [0, 180, 0 ,256], 1)

ret, skinMask = cv2.threshold(dst, 100, 255, 0)

# apply a series of erosions and dilations to the mask sing an elliptical
# kernel
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
skinMask = cv2.erode(skinMask, kernel, iterations=2)
skinMask = cv2.dilate(skinMask, kernel, iterations=2)

# blur the mask to help remove noise, then apply the mask to the frame
skinMask = cv2.GaussianBlur(skinMask, (3, 3), 0)
skin = cv2.bitwise_and(frame, frame, mask=skinMask)