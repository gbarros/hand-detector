"""
    This script is created for facilitate the creation of datasets
together with the other scripts in this package, it is possible to train
cascade classifiers based on OpenCV Framework.

    Usage is exaplained using "-h" or "--help" when excuting the script

    @Output
        Images ending with:
            _c.jpg are marked images for users to view the annotation results
                When done all can be deleted safely, suggested solution:
                [Unix-like OS] rm *._c.jpg
                [Windows OS] del *._c.jpg
            _s.jpg are the actual images produced for the dataset and saved on
                the json file.
        Json file:
            Used for the sample preparation script, it describes where are the
            images relative to its path and where are the objects of interest
            (bounding boxes).
"""

import argparse
import imutils
import cv2
import sys
import numpy as np
from os import path
from datetime import datetime as d

from enums import PRESET_SCAN_POINTS


def countours_solution(img):
    kernel_op = np.ones((5, 5), np.uint8)
    opening = cv2.morphologyEx(img, cv2.MORPH_DILATE, kernel_op)

    blur = cv2.GaussianBlur(opening, (5, 5), 0)

    ret, thresh1 = cv2.threshold(
        blur, 100, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    cv2.imshow("Countours after filters", thresh1)

    a, contours, hierarchy = cv2.findContours(thresh1,
                                              cv2.RETR_TREE,
                                              cv2.CHAIN_APPROX_SIMPLE)
    if len(contours) == 0:
        return ((0, 0), (0, 0))

    # Find the larggest countour
    max_area = cv2.contourArea(contours[0])
    ci = 0
    for i in range(1, len(contours)):
        area = cv2.contourArea(contours[i])
        if(area > max_area):
            max_area = area
            ci = i

    x, y, w, h = cv2.boundingRect(contours[ci])
    rect = ((x, y), (x + w, y + h))
    return rect


def add_description(folder, original_frame, frame, rect):
    """
        This function is responsible for saving the photos and
    formating a new entry for the json file.
    """

    name = d.now().isoformat()[:19]
    name = name.replace(":", ".")

    marked_name_path = name + "frame_c.jpg"
    nomark_name_path = name + "frame_s.jpg"

    marked_name_path = path.join(folder, marked_name_path)
    nomark_name_path = path.join(folder, nomark_name_path)

    ok = cv2.imwrite(nomark_name_path, original_frame)
    ok2 = cv2.imwrite(marked_name_path, frame)

    if not (ok and ok2):
        print "ERROR COULD NOT SAVE THE IMAGE"
    return {
        "file_name": nomark_name_path,
        "box": rect
    }


def get_color_filter(camera, points=PRESET_SCAN_POINTS):
    cv2.destroyAllWindows()
    key = 0
    while(key != 13):
        _, image = camera.read()
        image = imutils.resize(image, width=400)
        for p in points:
            cv2.rectangle(image, p[0], p[1], (0, 0, 255), 1)
        cv2.destroyWindow("Center the object over the dots")
        cv2.imshow("Center the object over the dots", image)
        key = cv2.waitKey(0)

    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    color_filter = {"max": [255, 0, 0], "min": [0, 255, 255]}

    for p in points:
        cut = lab[p[0][1]:p[1][1], p[0][0]:p[1][0]]
        for line in cut:
            for pixel in line:
                for i in range(1, len(pixel)):
                    if color_filter["max"][i] < pixel[i]:
                        color_filter["max"][i] = pixel[i]
                    elif color_filter["min"][i] > pixel[i]:
                        color_filter["min"][i] = pixel[i]

    color_filter["max"] = np.array(color_filter["max"], dtype='uint8')
    color_filter["min"] = np.array(color_filter["min"], dtype='uint8')
    cv2.destroyAllWindows()
    return color_filter


def set_environment(args):
    name = d.now().isoformat()[:19] + " " + args["name"] + ".json"
    name = name.replace(":", ".")
    folder = path.abspath(args["folder"])
    name = path.join(folder, name)
    return (name, folder)


def save_annotation(name, data_list):
    import json
    f = open(name, "w")
    json.dump(data_list, f)
    f.close()


def parse_args():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()

    ap.add_argument("-name", type=str, default="save",
                    help="String to add to the JSON filename, default is "
                    "'save'")

    ap.add_argument("-folder", type=str, default=".",
                    help="folder to save the generated files, default"
                    " is current dir")

    return vars(ap.parse_args())


if __name__ == "__main__":

    args = parse_args()

    json_name, folder_path = set_environment(args)
    json_data = []

    print "[INFO] Starting the application"

    camera = cv2.VideoCapture(0)

    color_filter = get_color_filter(camera)

    subMOG2 = cv2.createBackgroundSubtractorMOG2()
    cv2.ocl.setUseOpenCL(False)
    maskMOG2 = None
    learn = 0.5
    while True:
        _, image = camera.read()
        frame = imutils.resize(image, width=400)

        maskMOG2 = subMOG2.apply(frame, maskMOG2, learn)
        back_frame = cv2.bitwise_and(frame, frame, mask=maskMOG2)

        frame_lab = cv2.cvtColor(back_frame, cv2.COLOR_BGR2LAB)
        mask = cv2.inRange(frame_lab, color_filter["min"], color_filter['max'])

        rect = countours_solution(mask)
        original_frame = frame.copy()
        cv2.rectangle(frame, rect[0], rect[1], (0, 0, 255), 1)
        cv2.imshow("FINAL", frame)

        while(True):
            key = cv2.waitKey(0)
            if key == 27:  # 'esc'
                save_annotation(json_name, json_data)
                cv2.destroyAllWindows()
                sys.exit()
            elif key == 97 or key == 65:  # 'a'
                learn = 0.05 if learn == 0.5 else 0.5
                print "The learn ratio is:" + str(learn)
                break
            elif key == 99:  # 'c'
                color_filter = get_color_filter(camera)
                break
            elif key == 13:  # 'ENTER'
                json_data.append(add_description(folder_path,
                                                 original_frame,
                                                 frame,
                                                 rect))
                break
            else:
                pass
                break

    # cleanup
    cv2.destroyAllWindows()
    camera.release()
