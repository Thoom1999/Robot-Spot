# import the necessary packages
import numpy as np
import cv2


# load the image, clone it for output, and then convert it to grayscale
image = cv2.imread('../images/image.jpg')
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# detect circles in the image
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 10)
# ensure at least some circles were found
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
        x_center, y_center = x, y
        print((320-x_center)*(45/640)/100, (240-y_center)*(45/640)/100) # en mètre
        print("ca marche")

else :
    print("ca marhce pas")
    print(0, 0)
