from tkinter import *
from ..ui.widgets.widgets import *
from tkinter import filedialog
from .. import config 
from ..node.node_controller import *
from functools import partial
from queue import Queue

from PIL import (
    Image as p_Image,
    ImageEnhance as p_ImageEnhance,
    ImageOps as p_ImageOp,
    ImageTk as p_ImageTk,
)
import os


class floorPlan(object):
    # mode: True = preprocess, False = raw
    def __init__(self, path, canvas, mode=True):
        self.canvas = canvas
        self.path = path
        # assign backwards
        config.prepimgpath = path
        self.img = self.preprocess(mode)
        self.resize()
        self.x_mid = int(
            config.x_bb1
            + (config.x_bb2 - config.x_bb1) / 2
        )
        self.y_mid = int(
            config.y_bb1
            + (config.y_bb2 - config.y_bb1) / 2
        )

    def preprocess(self, mode):
        config.image_flag = True
        img = p_Image.open(self.path)
        if mode:
            img = img.convert("RGBA")
            enhancer = p_ImageEnhance.Contrast(img)
            img = enhancer.enhance(10)
            enhancer = p_ImageEnhance.Sharpness(img)
            img = enhancer.enhance(10)
            datas = img.getdata()
            newData = []
            for item in datas:
                if item[0] < 5 and item[1] < 5 and item[2] < 5 and item[3] != 0:
                    newData.append((0, 0, 0, 255))
                else:
                    newData.append((255, 255, 255, 0))
            img.putdata(newData)
        return img

    def resize(self):
        print("length = " + str(config.x_bb2 - config.x_bb1))
        print("x_bb1 = " + str(config.x_bb1))
        print("y_bb1 = " + str(config.y_bb1))

        if config.map_canvas.floorplan_obj is not None:
            self.canvas.delete(config.map_canvas.floorplan_obj)

        self.x_mid = int(
            config.x_bb1
            + (config.x_bb2 - config.x_bb1) / 2
        )
        self.y_mid = int(
            config.y_bb1
            + (config.y_bb2 - config.y_bb1) / 2
        )
        width_r = (
            config.x_bb2
            - config.x_bb1
            - config.img_padding
        )
        height_r = (
            config.y_bb2
            - config.y_bb1
            - config.img_padding
        )

        factor_w = width_r / float(self.img.size[0])
        factor_h = height_r / float(self.img.size[1])
        if factor_w > factor_h:
            factor = factor_h
        else:
            factor = factor_w
        height_r = int((float(self.img.size[1])) * float(factor))
        self.img = self.img.resize((width_r, height_r), p_Image.ANTIALIAS)
        print("resized, padding is {n}".format(n=config.img_padding))
        self.photoimg = p_ImageTk.PhotoImage(self.img)
        config.map_canvas.floorplan_obj = self.canvas.create_image(
            config.img_x_bb1,
            config.img_y_bb1,
            anchor="nw",
            image=self.photoimg,
        )
        config.map_canvas.restoreTagOrder()

    def save(self):
        print("boink")
        self.img.save(config.get_output_floor_plan_path(), "PNG")
