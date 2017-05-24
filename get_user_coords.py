#------------------------------------------------------------------------
# Description
#   Get a list of coordinates from finding the objects of images based
#   on a user defined box
#
# Usage
#   python get_user_coords.py --image_directory cars_images
#
#------------------------------------------------------------------------
import argparse
import cv2
import glob
import os
import sys

#------------------------------------------------------------------------
#------------------------------------------------------------------------
current_path = os.getcwd()
refPt = list()
gotCoords = False

def click_and_getCoords(event, x, y, flags, param):
    global refPt, gotCoords

    if event == cv2.EVENT_LBUTTONDOWN: #see if mouse is pressed (downwards)
        refPt = [(x,y)]
        gotCoords = True

    elif event == cv2.EVENT_LBUTTONUP: #see if mouse is released (upwards)
        refPt.append((x,y))
        gotCoords = False

        cv2.rectangle(image, refPt[0], refPt[1], (0,255,0),2) # draw green rectangle of width 2 around object
        cv2.imshow("Image in consideration", image)

#------------------------------------------------------------------------
#------------------------------------------------------------------------

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image_directory", required=True)
ap.add_argument("-o", "--outfile", required=True)
args = vars(ap.parse_args())

image_dir = args["image_directory"]
outfile_name = args["outfile"]
list_of_images = glob.glob(current_path + "/" + image_dir + "/*jpg")
list_of_coordinates = list()

with open(current_path + '/' + outfile_name, 'w') as f:
    continue_processing = True
    for imgfile in list_of_images:
        print("Processing: " + imgfile)
        if continue_processing == False:
            break

        image = cv2.imread(imgfile)
        clone = image.copy()
        cv2.namedWindow("image")
        cv2.setMouseCallback("image", click_and_getCoords)

        while continue_processing:
            cv2.imshow("image", image)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("r"): #refresh image because you messed up
                image = clone.copy()

            elif key == ord("d"): #d for done
                f.write("[" + str(refPt[0][1]) + "," + str(refPt[1][1] - refPt[0][1]) + "," + str(refPt[0][0]) + "," + str(refPt[1][0] - refPt[0][0]) + "]" + "\n")
                break

            elif key == ord("q"): # q for quit
                cv2.destroyAllWindows()
                continue_processing = False
                break

        if len(refPt) == 2:
            print("[" + str(refPt[0][1]) + "," + str(refPt[1][1] - refPt[0][1]) + "," + str(refPt[0][0]) + "," + str(refPt[1][0] - refPt[0][0]) + "]")

        cv2.destroyAllWindows()