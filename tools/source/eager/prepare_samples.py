#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import cv2
import json
import os
import argparse
from eager.libs.mergevec import merge_vec_files
join = os.path.join

CREATE_SAMPLES = ("opencv_createsamples.exe -img {img} -num {num} "
                  "-bg {negatives} -bgthresh 0  -bgcolor 0 "
                  "-maxzangle {z} -maxyangle {y} -maxxangle {x} "
                  "-vec {vecfile}.vec -w {w} -h {h}  {show} ")


def safe_open_dir(dir_path):
    """
        This function ensures the folders needed exists and abstracts that away
    """
    try:
        os.stat(dir_path)
    except:
        os.mkdir(dir_path)


def crop_img(img, positions):
    """
        This function crops images based o array of positions defined for the
        project
            @img the original image as numpy.array
            @postion [[minW, minH], [maxW, maxH]]
    """
    mins = positions[0]
    maxs = positions[1]
    return img[mins[1]:maxs[1], mins[0]:maxs[0]]


def format_add_dat(file, folder, image_name, positions):
    """
        This adds on more line on the dat file already on the needed format
            @file already open to write dat file
            @folder relative path to the dat file to access the image
            @image_name string
            @postion [[minW, minH], [maxW, maxH]]
    """
    x = positions[0][0]
    y = positions[0][1]
    width = positions[1][0] - x
    heigth = positions[1][1] - y
    line = folder + '/' + image_name + " " + "1" + " "
    line += str(x) + " " + str(y) + " " + str(width) + " " + str(heigth) + '\n'
    file.write(line)


def resize(img, new_width):
    """
        This function resizes the image withou distorting the ratio
            @img to be transformed
            @new_width with to be used as base
            @return
                new_img resized image
                dsize tuple (with, heigth) with new dimensions
    """
    ratio = float(new_width) / img.shape[1]
    new_heigth = int(img.shape[0] * ratio)
    dsize = (new_width, new_heigth)
    new_img = cv2.resize(img, dsize, interpolation=cv2.INTER_AREA)

    return new_img, dsize


def bouding_box_recalc(positions, old_dim, new_dim):
    """
        This functions calculates the new position for the bounding boxes
            @positions [[minW, minH], [maxW, maxH]]
            @old_dim old dimensions (with, height)
            @new_dim new dimensions
    """
    wr = float(new_dim[0]) / old_dim[0]
    hr = float(new_dim[1]) / old_dim[1]
    positions[0][0] = int(positions[0][0] * wr)
    positions[1][0] = int(positions[1][0] * wr)
    positions[0][1] = int(positions[0][1] * hr)
    positions[1][1] = int(positions[1][1] * hr)

    return positions


def set_name(json_doc):
    full_path = os.path.abspath(json_doc)
    splitted = full_path.split(os.path.sep)
    return splitted[len(splitted) - 2]


def root_dir(json_doc):
    full_path = os.path.abspath(json_doc)
    root = join(full_path, "..", "..")
    return os.path.abspath(root)


def create_samples(cropped, dirpath, options={}):
    """
        This function calls the opencv_createsamples tool.
    it takes a cropped image, save it, format the options and
    call the tool.
    """
    try:
        create_samples.counter += 1
    except AttributeError:
        create_samples.counter = 1

    temp = "temp" + str(create_samples.counter)
    img_name = temp + ".jpg"
    vecfile = temp
    imgpath = join(dirpath, img_name)
    vecpath = join(dirpath, vecfile)
    cv2.imwrite(imgpath, cropped)
    options["img"] = imgpath
    options["vecfile"] = vecpath
    os.popen(CREATE_SAMPLES.format(**options)).close()


def process_raw_samples(json_doc, base_width_resize, options):
    """
            This function is responsible for coordinating the whole process
        it checks files and folders, open some and clean up at the end.
            It takes the json document which describes where are the images 
        and its area of interest. Then converts to gray scale, resizes and
        crops all the images.
    """

    meta = json.load(open(json_doc))

    photosdir = os.path.dirname(os.path.abspath(json_doc))
    setname = set_name(json_doc)
    graydir = join(photosdir, "gray")
    safe_open_dir(graydir)
    # rootdir = root_dir(json_doc)
    generateddir = join(photosdir, "generated_samples")
    safe_open_dir(generateddir)

    dat_name = join(photosdir, setname + ".dat")
    out_dat = open(dat_name, "w")

    for doc in meta:
        path = join(photosdir, doc["file_name"])
        image = cv2.imread(path)
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        small, dimensions = resize(gray, base_width_resize)
        old_dim = (image.shape[1], image.shape[0])
        pos = bouding_box_recalc(doc["box"], old_dim, dimensions)

        format_add_dat(out_dat, "gray", doc["file_name"], pos)

        cropped = crop_img(small, pos)
        create_samples(cropped, generateddir, options)

        gray_path = join(graydir, doc["file_name"])
        cv2.imwrite(gray_path, small)

    merge_vec_files(generateddir, setname + ".vec")
    out_dat.close()
    os.popen("del {}\*.vec".format(generateddir)).close()


def main():

    options = {
        "num": 3,
        "z": 0.1,
        "y": 0.5,
        "x": 0.5,
        "show": "",
        "w": 80,
        "h": 80,
        "negatives": ""
    }

    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-n", "--num", type=int, default=None,
                    help="amount of samples to create from each positive"
                    "example")

    ap.add_argument("-z", "--max-z-angle", type=float, default=None,
                    help="max z axis distortion over generated samples")
    ap.add_argument("-x", "--max-x-angle", type=float, default=None,
                    help="max x axis distortion over generated samples")
    ap.add_argument("-y", "--max-y-angle", type=float, default=None,
                    help="max y axis distortion over generated samples")

    ap.add_argument("-wd", "--width", type=int, default=None, required=True,
                    help="width for the training set")

    ap.add_argument("-ht", "--height", type=int, default=None, required=True,
                    help="height for the training set")

    ap.add_argument("-bg", "--background", type=str, default=None,
                    required=True, help="background to be used on the new"
                    " sample")
    ap.add_argument("-s", "--sample", type=str, default=None, required=True,
                    help="json sample file")
    args = vars(ap.parse_args())
    options["num"] = args["num"] or options["num"]
    options["z"] = args["max_z_angle"] or options["z"]
    options["y"] = args["max_y_angle"] or options["y"]
    options["x"] = args["max_x_angle"] or options["x"]
    options["w"] = args["width"] or options["w"]
    options["h"] = args["height"] or options["h"]
    options["negatives"] = args["background"] or options["negatives"]

    process_raw_samples(args["sample"], 25, options)
