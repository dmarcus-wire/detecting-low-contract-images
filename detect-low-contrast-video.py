# USAGE
# python detect-low-contrast-video.py

# import necessary packages
from skimage.exposure import is_low_contrast
import numpy as np
import argparse
import imutils
import cv2

# construct argument parser
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", type=str, default="",
                help="optional path to video file")
ap.add_argument("-t", "--thresh", type=float, default=0.35,
                help="threshold for low contrast")
args = vars(ap.parse_args())

# grab pointer for video in
print("[INFO] accessing video stream...")
# if input provided use, else use webcam
vs = cv2.VideoCapture(args["input"] if args["input"] else 0)

# loop over frames from the video stream
while True:
    # read frame from video stream
    (grabbed, frame) = vs.read()

    # if the frame was not grabbed, exit
    if not grabbed:
        print("[INFO] no frame read from stream - exit")
        break

    # PREPROCESSING resize the frame, convert to grayscale, blur it, edge detect
    frame = imutils.resize(frame, width=450)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(blurred, 30, 150)

    # initialize the text and color
    text = "Low contrast image: No"
    color = (0, 255, 0)

    # check if low contrast
    if is_low_contrast(gray, fraction_threshold=args["thresh"]):
        text = "Low contrast image: Yes"
        color = (0, 0, 255)

    else:
        # find contours in the edge map and largest one
        # assume largest is the edge
        cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        # draw the largest contours
        cv2.drawContours(frame, [c], -2, (0, 255, 0), 2)

    # draw the text on the output frame
    cv2.putText(frame, text, (5, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                color, 2)

    # stack the output frame and the edge map next to each other
    # horizontally stacked with frame (RGB) and edge map (grayscale)
    # stack the edged 3 times so it matches the array dimensions of the RGB...grayx3
    output = np.dstack([edged] * 3)
    output = np.hstack([frame, output])

    # show the output to screen
    cv2.imshow("Output", output)
    # q-key will break the script
    key = cv2.waitKey(1) & 0xFF
