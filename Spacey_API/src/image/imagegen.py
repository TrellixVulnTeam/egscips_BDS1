# 5c98e2

from PIL import Image, ImageDraw, ImageFilter
import os
from .. import config


def imagegen():
    # cfg.decompile(cfg.json_path)
    floorplan_path = config.get_output_floor_plan_path()

    node_off = Image.open(config.nodeOff_path)
    node_off = node_off.resize(
        (int(config.box_len * 2.5), config.box_len * 2)
    )
    node_on = Image.open(config.nodeOn_path)
    node_on = node_on.resize(
        (int(config.box_len * 2.5), config.box_len * 2)
    )
    print("box_len: ", config.box_len)

    config.output_graphic_coord["box_len"] = config.box_len

    config.canvas_xlen = config.x_bb2 - config.x_bb1
    config.canvas_ylen = config.y_bb2 - config.y_bb1
    output_img_x_bb1 = config.img_x_bb1 - config.x_bb1
    output_img_y_bb1 = config.img_y_bb1 - config.y_bb1

    bg = Image.new(
        "RGBA",
        (config.canvas_xlen, config.canvas_ylen),
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
        config.error.updateText("No photo", "yellow")
    # bg.paste(floorplan, (0,0), mask = floorplan)

    for i in config.node_controller.idxList:
        x = config.node_controller.x_coord[i] - (
            config.x_bb1 + config.box_len
        )
        y = config.node_controller.y_coord[i] - (
            config.y_bb1 + config.box_len
        )
        config.output_graphic_coord[i] = str(x) + "," + str(y)

        x = config.output_graphic_coord.get(i).rsplit(",")[0]
        y = config.output_graphic_coord.get(i).rsplit(",")[1]
        print(x, type(x))

        if int(config.node_controller.occupancy[i]) == 0:
            node = node_on
        else:
            node = node_off
        bg.paste(node, (int(x), int(y)))

    # bg.paste(node_off,(0, 0))
    # bg.paste(node_off,(100, 500))
    bg.show()

    print(bg.size)
    bg.save(config.get_output_graphic_path(), quality=95, format="PNG")
