# 5c98e2

from PIL import Image, ImageDraw, ImageFilter
import os
from . import config as tkinter_window_cfg


def imagegen():
    # cfg.decompile(cfg.json_path)
    floorplan_path = tkinter_window_cfg.get_output_floor_plan_path()

    node_off = Image.open(tkinter_window_cfg.nodeOff_path)
    node_off = node_off.resize(
        (int(tkinter_window_cfg.box_len * 2.5), tkinter_window_cfg.box_len * 2)
    )
    node_on = Image.open(tkinter_window_cfg.nodeOn_path)
    node_on = node_on.resize(
        (int(tkinter_window_cfg.box_len * 2.5), tkinter_window_cfg.box_len * 2)
    )
    print("box_len: ", tkinter_window_cfg.box_len)

    tkinter_window_cfg.output_graphic_coord["box_len"] = tkinter_window_cfg.box_len

    tkinter_window_cfg.canvas_xlen = tkinter_window_cfg.x_bb2 - tkinter_window_cfg.x_bb1
    tkinter_window_cfg.canvas_ylen = tkinter_window_cfg.y_bb2 - tkinter_window_cfg.y_bb1
    output_img_x_bb1 = tkinter_window_cfg.img_x_bb1 - tkinter_window_cfg.x_bb1
    output_img_y_bb1 = tkinter_window_cfg.img_y_bb1 - tkinter_window_cfg.y_bb1

    bg = Image.new(
        "RGBA",
        (tkinter_window_cfg.canvas_xlen, tkinter_window_cfg.canvas_ylen),
        (92, 152, 226, 255),
    )
    # bg = Image.open(cfg.get_output_graphic_path())
    try:
        floorplan = Image.open(floorplan_path)
        datas = floorplan.getdata()
        newData = []
        for item in datas:
            if item[3] > 50:
                # newData.append((51,82,133,255))
                newData.append((50, 50, 50, 255))
            else:
                newData.append((0, 0, 0, 0))
        floorplan.putdata(newData)

        bg.paste(floorplan, (output_img_x_bb1, output_img_y_bb1), mask=floorplan)
    except:
        tkinter_window_cfg.error.updateText("No photo", "yellow")
    # bg.paste(floorplan, (0,0), mask = floorplan)

    for i in tkinter_window_cfg.restaurant_space.idxList:
        x = tkinter_window_cfg.restaurant_space.x_coord[i] - (
            tkinter_window_cfg.x_bb1 + tkinter_window_cfg.box_len
        )
        y = tkinter_window_cfg.restaurant_space.y_coord[i] - (
            tkinter_window_cfg.y_bb1 + tkinter_window_cfg.box_len
        )
        tkinter_window_cfg.output_graphic_coord[i] = str(x) + "," + str(y)

        x = tkinter_window_cfg.output_graphic_coord.get(i).rsplit(",")[0]
        y = tkinter_window_cfg.output_graphic_coord.get(i).rsplit(",")[1]
        print(x, type(x))

        if int(tkinter_window_cfg.restaurant_space.occupancy[i]) == 0:
            node = node_on
        else:
            node = node_off
        bg.paste(node, (int(x), int(y)))

    # bg.paste(node_off,(0, 0))
    # bg.paste(node_off,(100, 500))
    bg.show()

    print(bg.size)
    bg.save(tkinter_window_cfg.get_output_graphic_path(), quality=95, format="PNG")
