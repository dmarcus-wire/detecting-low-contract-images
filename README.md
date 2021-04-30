# Low contrast image detection
## Goal: safely detect edges with varying lighting conditions
- if >= threshold (we can safely find the outline), detect the edges on the frame(s), draw them
- if < threshold (we don't have sufficient conditions), transparently notify user and discard frames until we increase the image quality

## Assuming:
- some understanding of lightening consditions so you can set an acceptable contrast threshold

Procedure
- import necessary packages
- command line arguments
- loop over images
    - read from disk
    - resize to width 450
    - convert frm BGR to grayscale
    - smooth with 5x5 gaussin kernel
    - apply edge detection to blurred image
    - assuming text is not low contrast
    - loop if image is low contrast
        - check if low
            - if low, exit
        else
            - find contours in edge map
            - find largest one
    - draw the text on the image and outline
    