# USAGE
# python detect-low-contrast-images.py

from skimage.exposure import is_low_contrast
from imutils.paths import list_images
import argparse
import imutils
import cv2

# construct the argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
                help="path to the input directory")
# https://scikit-image.org/docs/dev/api/skimage.exposure.html#skimage.exposure.is_low_contrast
# images in opencv are unsigned 8-bit integers array
# if less than 35% fail to span the entire 0 to 255 range, it is a low contrast image b/c not enough pixels
# span the entire range
ap.add_argument("-t", "--thresh", type=float, default=0.35,
                help="threshold for low contrast images")
args = vars(ap.parse_args())

# get the paths to images
imagePaths = sorted(list(list_images(args["input"])))

# loop over the image paths
for (i, imagePaths) in enumerate(imagePaths):
    # load image from disk
    print("[INFO] processing image {}/{}".format(i + 1,
                                 len(imagePaths)))
    image = cv2.imread(imagePaths)
    # resize to 450 pixels wide
    image = imutils.resize(image, width=450)
    # convert from RGB to GRAY
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # prepare for edge detection
    # smooth 5x5 gaussian kernel
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # apply edge detection to the blur
    edged = cv2.Canny(blurred, 30, 150)

    # initialize two variables green text
    test = "Low contrast: No"
    color = (0, 255, 0)

    # is the image low contrast
    if is_low_contrast(gray, fraction_threshold=args["thresh"]):
        # update the color to red and text
        text = "Low contrast: Yes"
        color = (0, 0, 255)

    # perform edge detection
    else:
        # find contours in the edge map and the largest one
        # which we'll assume is the outline of the image
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # draw the largest contour on the image
        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

    cv2.putText(image, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                color, 2)

    # show the output image and edge map
    cv2.imshow("Image", image)
    cv2.imshow("edged", edged)
    cv2.waitKey(0)