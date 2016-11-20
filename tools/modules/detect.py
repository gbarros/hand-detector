#!/usr/bin/env python
import cv2
import argparse
import sys
import tools as t
from enums import PRESET_COLORS
# import numpy as np


def detect_video(cascade1, camera, win_name="window", color=(255, 0, 0)):
    ret, image = camera.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    rects = cascade1.detectMultiScale2(gray, minSize=(
        30, 30), minNeighbors=4, scaleFactor=1.3)
    for rect in rects:
        if len(rect) == 0 or len(rect[0]) == 1:
            break
        t.draw_rects(image, rect, color)
    cv2.imshow(win_name, image)


def run(cascades, millis=0):
    camera = cv2.VideoCapture(0)
    key = 0
    while(key != 27):
        for cascade in cascades:
            detect_video(cascade["detector"],
                         camera,
                         cascade["win"],
                         color=cascade["color"])
        key = cv2.waitKey(millis)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade-file", type=str, default=None,
                    help='The path for the cascade file', nargs='+')
    ap.add_argument("-m", "--millis", type=int, default=1,
                    help="Amount of time to wait between frames;"
                    "set 0 for key press step only")
    args = vars(ap.parse_args())
    if not args["cascade_file"]:
        print "You need to input at least the one detector file"
        sys.exit()

    cascades = []
    i = 0
    for file_name in args["cascade_file"]:
        cascades.append({
            "detector": cv2.CascadeClassifier(file_name),
            "win": file_name,
            "color": PRESET_COLORS[i]
        })
        i += 1

    run(cascades, args["millis"])
