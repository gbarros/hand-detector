"""
    This module will contain any auxiliary tools that maybe shared
across functional scripts
"""
import cv2
import json


def draw_rects(img, rects, color):
    """
        Draw rects
        #Side-effect over @img

        @img
            image to have rectangles draw
        @rects
            4-tuple as upper-left corner, bottom-right corner
                as x1,y1,x2,y2
        @color
            3-tuple of 8bit integers
    """
    for x1, y1, x2, y2 in rects:
        cv2.rectangle(img, (x1, y1), (x1 + x2, y1 + y2), color, 2)


def variance_of_laplacian(img):
    """
        Variance of Laplacian
        @img
            image to be evaluated
        @return
            float number rusulted from the calculation
    """
    return cv2.Laplacian(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY),
                         cv2.CV_64F).var()


def equal(a, b):
    """
        This function compares the main name of the photos marked or not
    """
    if a.split("_")[0] == b.split("_")[0]:
        return True
    return False


def open_json(filename):
    file = open(filename)
    return json.load(file)


def save_json(json_file, filename):
    file = open(filename, "w")
    json.dump(json_file, file)


def filter_by_type(listdir, filter):
    files = []
    for f in listdir:
        if f.find(filter) >= 0:

            files.append(f)
    return files
