from tkinter import *
from .ui.widgets.widgets import *
from tkinter import filedialog
from . import config as config
from .node.node_controller import *
from .image.imgpro import *
import sys
from .storage import redisDB
import os
from os.path import dirname as dir, splitext, basename, join, abspath
import sys
import base64
from platform import system as platf
import json

# Need to choose depending on running from exe or py. Should point to /Spacey API

if platf() == "Linux":
    parentdir = dir(dir(sys.executable))
    print(parentdir)
    if basename(parentdir) == "Node Manager":
        _root = dir(parentdir)
    else:
        _root = dir(dir(abspath(__file__)))


elif platf() == "Windows":
    parentdir = basename(dir(abspath(__file__)))
    if parentdir == "Node Manager":
        _root = dir(dir(abspath(__file__)))
    else:
        _root = dir(dir(dir(sys.executable)))


# _root = dir(dir(os.path.abspath(__file__)))

# To extract database interface functions
print(_root)
sys.path.append(join(_root, "Redis"))
with open("text.txt", "w") as outfile:
    outfile.write("from_redis: {}".format(_root))
print("here", sys.path)
# Relevant file directories

floorplan_folder_input = os.path.join(_root, "floorplan_images", "input floorplan")
floorplan_folder_output = os.path.join(_root, "floorplan_images", "output floorplan")
json_folder = os.path.join(_root, "json_files")

# Default folder for JSON files
json_folder_config = os.path.join(json_folder, "config")

# Image Assets
image_folder = os.path.join(_root, "images")
image_asset_folder = os.path.join(image_folder, "assets")
image_output_graphic_folder = os.path.join(image_folder, "output graphic")
icon_path = os.path.join(image_asset_folder, "spacey_icon.ico")
gif_path = os.path.join(image_asset_folder, "spacey_icon.gif")
nodeOn_path = os.path.join(image_asset_folder, "unoccupied_nodes.png")
nodeOff_path = os.path.join(image_asset_folder, "occupied_nodes.png")
private_key_folder = os.path.join(_root, "private key")

# Database information

remote_host = "uwu"
password = "0w0"
port = "@w@"  # 9


database = redisDB.redis_database(_root, remote_host, port, password)

# Global Variables
root = None  # TK window root
x_list = []  # list of all possible coordinates
y_list = []
img = None  # image file
num_coordinates_max = 0  # max num of coordinates
node_controller = None  # glb restaurant space
node = None  # node pointer
x, y = 0, 0  # mid coords of the latest node placed
x_bb1, y_bb1 = 0, 0  # Bounding box coordinates of active canva region (blue)
x_bb2, y_bb2 = 0, 0
deposit_flag = True  # If a node can be deposit on the spot
updateTextDone = False  # Signal update of err msg
map_canvas = None  # glb map_canvasObj
node_idx = None
prev_node_idx = None
step = 5  # dist between each grid line
toggle = 0  # toggle btw entry[left] or canvas
initflag = 0  # detect correct user input
err_inval_input = True  # Allow red color on entry boxes when user rehashes stored key
error = None  # error obj
error_font = None  # error font
json_font = None  # json font
max_step = 200  # prevent grid line from scaling down to self collapse
hlcolor = "yellow"  # glb highlight color
buttcolor = "gray80"
cursor = None  # glb cursor
box_len = step  # length of node
scale = 50  # num of grid lines along x axis
bg = None  # backgroun sky blue
prepimgpath = None  # path of image
postimgpath = None
pady = 5  # padding for widget format
padx = 5
map_grid = None
filename = ""
img_padding = 0
image_flag = False
load_flag = False
img_x_bb1 = -1  # img bb box corner
img_y_bb1 = -1
config.db_options = ["No Database Selected"]
userid = ""
session_name = ""
no_floor_plan = False

local_disk = False

# Restaurant info
res_addr = None
res_occup_hr = None
res_lat = None
res_lng = None

res_info_op = ["res_lat", "res_lng", "res_addr", "res_occup_hr"]

# Variables that will be stored to restore save states with the Node Manager
config_op = [
    "image_flag",
    "x_bb1",
    "x_bb2",
    "y_bb1",
    "y_bb2",
    "img_x_bb1",
    "img_y_bb1",
    "box_len",
    "prepimgpath",
    "scale",
    "postimgpath",
    "img_padding",
]

# Dictionaries for JSON compilation purposes.
configinfo = {}
devinfo = {}
resinfo = {}
json_zipinfo = {}
json_occupancy = {}
json_hash = {}
json_coord = {}
output_graphic_coord = {}


def getvar():
    return globals()


# File functions
def getbasename(path):
    return splitext(basename(path))[0]


# Return filename of the new output graphic
def get_output_graphic_path():
    if local_disk:
        name = config.session_name
    else:
        name = (
            config.userid + "_" + config.session_name
        ).lstrip("_")

    result = os.path.join(image_output_graphic_folder, "output_" + name + ".png")
    return result


def get_output_floor_plan_path():
    if no_floor_plan:
        return None
    if local_disk:
        name = config.session_name
    else:
        name = (
            config.userid + "_" + config.session_name
        ).lstrip("_")
    result = os.path.join(floorplan_folder_output, "processed_img_" + name + ".png")
    config.postimgpath = name
    return result


# Serializes image from png to string
def json_serialize_image(image_file):
    try:
        with open(image_file, mode="rb") as file:
            img = file.read()
        return base64.b64encode(img).decode("utf-8")  # picture to bytes, then to string
    except:
        return None


# Deserializes image from string to png, then save it in the specified file directory
def json_deserialize_image(encoded_str, image_file):
    try:
        result = encoded_str.encode("utf-8")
        result = base64.b64decode(result)
        image_result = open(
            image_file, "wb"
        )  # create a writable image and write the decoding result
        image_result.write(result)
    except:
        return None


def configJsonDir(root):
    json_folder = join(root, "json_files")
    json_file_config = join(json_folder, "config")
    json_file_occupancy = join(json_folder, "occupancy")
    json_file_hash = join(json_folder, "hash")
    json_file_coord = join(json_folder, "coord")
    return [json_file_config, json_file_occupancy, json_file_hash, json_file_coord]


def compile(root, local_disk=True):
    for i in config_op:
        configinfo[i] = globals()[i]

    for i in node_controller.devinfo:
        devinfo[i] = getattr(node_controller, i)

    # Populate the dictionary with the serialized information
    json_zipinfo["configinfo"] = json.dumps(configinfo)
    json_zipinfo["devinfo"] = json.dumps(devinfo)
    json_occupancy = config.node_controller.occupancy
    json_hash = config.node_controller.tuple_idx
    json_coord = config.output_graphic_coord
    if image_flag == True:

        json_zipinfo["processed_floorplan"] = json_serialize_image(
            config.get_output_floor_plan_path()
        )
    json_coord["processed_img"] = json_serialize_image(
        config.get_output_graphic_path()
    )
    # List of dictionaries containing serialised information. We will now write it into a json file to store in database/ local disk
    json_dict_list = [json_zipinfo, json_occupancy, json_hash, json_coord]
    name = config.userid + "_" + config.session_name

    if local_disk:
        name = session_name
        for i in range(len(json_dict_list)):

            path = os.path.join(
                configJsonDir(config._root)[i], name + ".json"
            )
            with open(path, "w") as outfile:
                json.dump(json_dict_list[i], outfile)
    else:
        for i in res_info_op:
            resinfo[i] = globals()[i]
        config.database.exportToDB(name, import_from_script=json_dict_list)
        config.database.setResInfo(name, resinfo)

    data = {}
    # Confirms the json file's existence and prints contents on console.
    if local_disk:

        path = os.path.join(configJsonDir(config._root)[0], name + ".json")
        with open(path, "r") as infile:
            data = json.loads(infile.read())
        return str(json.dumps(data["configinfo"], indent=1))
    else:

        data = config.database.importFromDB(name, export_to_script=[data])
        print("-------")

    return str(json.dumps(data[0]["configinfo"], indent=1))


def decompile(root, local_disk=True):
    global json_zipinfo, json_occupancy, json_hash, json_coord
    json_zipinfo.clear()
    json_occupancy.clear()
    json_hash.clear()
    json_coord.clear()
    config.output_graphic_coord.clear()
    # List of dictionaries containing serialised information. We will now write it into a json file to store in database/ local disk
    json_dict_list_name = ["json_zipinfo", "json_occupancy", "json_hash", "json_coord"]
    data = []
    name = config.userid + "_" + config.session_name
    for i in range(4):
        data.append({})

    if local_disk:
        name = config.session_name
        for i in range(len(configJsonDir(config._root))):
            path = os.path.join(
                configJsonDir(config._root)[i], name + ".json"
            )
            with open(path, "r") as outfile:
                globals()[json_dict_list_name[i]] = json.load(outfile)
    else:
        data = config.database.importFromDB(name, export_to_script=data)
        for i in json_dict_list_name:
            globals()[i] = data[json_dict_list_name.index(i)]
        resinfo = config.database.getResInfo(name)

    configinfo = json.loads(json_zipinfo.get("configinfo"))
    devinfo = json.loads(json_zipinfo.get("devinfo"))
    processed_img = json_coord.get("processed_img")
    processed_floorplan = json_zipinfo.get("processed_floorplan")

    if not local_disk:
        config.json_deserialize_image(
            processed_img, config.get_output_graphic_path()
        )
        config.json_deserialize_image(
            processed_floorplan, config.get_output_floor_plan_path()
        )
        for i in res_info_op:
            globals()[i] = resinfo[i]
    else:
        no_floor_plan = False
    output_graphic_coord = json_coord
    config.box_len = json_coord["box_len"]
    json_coord.pop("box_len")
    devinfo["tuple_idx"] = json_hash
    devinfo["occupancy"] = json_occupancy

    for i in config_op:
        globals()[i] = configinfo[i]

    for i in node_controller.devinfo:
        setattr(node_controller, i, devinfo[i])

    unpackFromJson()
    node_controller.unpackFromJson()

    return json.dumps(json_zipinfo["configinfo"], indent=1)


def unpackFromJson():
    global img

    if config.image_flag is True:
        img = imgpro.floorPlan(
            config.get_output_floor_plan_path(),
            config.map_canvas.canvas,
            False,
        )
    map_grid.refresh(delete=False, resize=False)
    config.map_canvas.restoreTagOrder()
