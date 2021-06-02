################################################# SPACEY Initiation GUI Wizard #############################################
# Author: Looi Kai Wen                                                                                                     #
# Last edited: 07/07/2020                                                                                                  #
# Summary:                                                                                                                 #
#   For use by BLE network administrators to configure their database with invariant information,                          #
#   eg. relative coordinates of the sensor mote, cluster level, etc.                                                       #
############################################################################################################################
"""
This file interfaces primarily with this library called Tkinter. 
It is a fairly convenient library to use in Windows. 
"""


import tkinter as tk
from tkinter import font

from .ui.controller import set_window_icon
from .ui import ui_props as ui
from . import config as tkinter_window_cfg
from . import sensor_data
from .commons.constants import *
from os.path import dirname as dir
from platform import system as platf
from PIL import (
    Image as p_Image,
    ImageEnhance as p_ImageEnhance,
    ImageOps as p_ImageOp,
    ImageTk as p_ImageTk,
)
import os


def onFrameConfigure(canvas):
    """
    Reset the scroll region to encompass the inner frame
    """
    canvas.configure(scrollregion=canvas.bbox("all"))


def track(event):
    """
    Tracks mouse coordinates.
    Possibly defunct.
    """
    print("x: " + str(event.x) + "\ny: " + str(event.y))


def quit(event):
    """
    Quit from the program window.
    """
    tkinter_window_cfg.root.destroy()


def focus_toggle_between_sensor_id_frame_and_map_frame(event, widget):
    """
    Toggle focus between sensor id frame and map frame.
    Focus = You can use keyboard controls.
    Called upon when you press Ctrl-Z.
    """
    tkinter_window_cfg.toggle = 1 - tkinter_window_cfg.toggle
    if tkinter_window_cfg.toggle:
        # Set focus to canvas, so that you can use key controls on map
        tkinter_window_cfg.myCanvas.canvas.focus_set()
    else:
        # Set fous to sensor id frame, so you can type values in
        widget.focus_set()


def focus_toggle(mode, widget=None):
    """
    Toggle focus between Map frame, and the widget in question.
    """
    if mode:
        tkinter_window_cfg.myCanvas.canvas.focus_set()
    else:
        widget.focus_set()


def focus_canvas():
    """
    Set focus onto map.
    """
    focus_toggle(mode=True)


def setup():
    """
    Set Tk configuration
    """
    global canvas_w, canvas_h, image_file

    tkinter_window_cfg.root = tk.Tk()

    default_font = font.nametofont(TKINTER_DEFAULT_FONT)
    default_font.configure(size=TKINTER_DEFAULT_FONT_SIZE)

    # cfg.root.state('zoomed') # Full window view

    # Set title name

    tkinter_window_cfg.root.title(TKINTER_WINDOW_TITLE)
    # Set BG colour
    tkinter_window_cfg.root.configure(bg=TKINTER_WINDOW_COLOUR_BACKGROUND)

    # Set Icon of the window
    set_window_icon(tkinter_window_cfg)

    # cfg.root.iconbitmap(cfg.icon_path)
    # cfg.root.geometry('1280x720')  #size of w
    # tkinter_window_cfg.root.update_idletasks()

    # Set Window size by factor
    window_size_factor = 1

    # cfg.root.geometry(str(int(1366*factor)) + "x" + str(int(768*factor)))  #size of w

    # Set the window size
    tkinter_window_cfg.root.geometry(
        str(int(TKINTER_WINDOW_DEFAULT_WIDTH * window_size_factor))
        + "x"
        + str(int(TKINTER_WINDOW_DEFAULT_HEIGHT * window_size_factor))
    )  # size of w

    # To retain our sanity, strictly disallow users from resizing the window.
    tkinter_window_cfg.root.resizable(0, 0)

    ### Log current window info ###
    print(tkinter_window_cfg.root.winfo_height())
    print(tkinter_window_cfg.root.winfo_width())
    print(tkinter_window_cfg.root.winfo_geometry())
    print(tkinter_window_cfg.root.winfo_screenheight())
    print(tkinter_window_cfg.root.winfo_screenwidth())

    ### Creation of GUI map ###
    # Set frame to embed canvas
    frame_canvas = tk.LabelFrame(
        tkinter_window_cfg.root,
        text=TKINTER_WIDGET_MAP_TEXT_TITLE,
        width=TKINTER_WIDGET_MAP_WIDTH,
        height=TKINTER_WIDGET_MAP_HEIGHT,
        bg=TKINTER_WIDGET_MAP_COLOUR_BACKGROUND,
    )

    # Set canvas within frame
    tkinter_window_cfg.myCanvas = ui.myCanvasObject(
        frame_canvas,
        TKINTER_WIDGET_MAP_WIDTH,
        TKINTER_WIDGET_MAP_HEIGHT,
    )

    # Handles node operations and recording
    tkinter_window_cfg.restaurant_space = sensor_data.RestaurantSpace(
        tkinter_window_cfg.myCanvas.canvas
    )

    # Creates rectangle cursor (in red)
    cursor = ui.CursorNode(tkinter_window_cfg.myCanvas.canvas)

    # Creates gridlines so that the boxes inserted will appear more organised
    tkinter_window_cfg.grid = ui.CanvasGridFrame(
        tkinter_window_cfg.myCanvas.canvas, tkinter_window_cfg.scale
    )

    ### Creation of Config menu ###
    _frame_menu = tk.LabelFrame(
        tkinter_window_cfg.root,
        text="Configurations",
        width=int(TKINTER_WIDGET_CONFIG_PANEL_WIDTH / 1.6),
        height=TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
        bg="gray40",
    )
    _frame_menu.pack(padx=20, pady=20, side=tk.LEFT, expand=1, anchor="w")
    _frame_menu.pack_propagate(False)

    menu_canvas = tk.Canvas(
        _frame_menu, borderwidth=0, bg="gray40", highlightbackground="gray40"
    )
    yscroll = tk.Scrollbar(_frame_menu, orient="vertical", command=menu_canvas.yview)

    yscroll.pack(padx=2, pady=2, side=tk.LEFT, fill=Y)
    menu_canvas.pack(side=tk.LEFT, expand=True, fill="both")
    menu_canvas.configure(yscrollcommand=yscroll.set)
    frame_menu = tk.Frame(menu_canvas, borderwidth=0, bg="gray40")
    frame_menu.pack()
    menu_canvas.create_window((0, 0), window=frame_menu, anchor="nw")
    frame_menu.bind(
        "<Configure>", lambda event, canvas=menu_canvas: onFrameConfigure(canvas)
    )

    frame_menu1 = tk.LabelFrame(
        frame_menu,
        text="Menu 1",
        width=TKINTER_WIDGET_CONFIG_PANEL_WIDTH / 3.4,
        height=TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
        bg="gray40",
    )
    frame_menu1.pack(side=tk.LEFT, expand=1, fill=tk.X)
    frame_menu1.pack_propagate(False)

    help = ui.menu_help(
        frame_menu1,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    upload = ui.menu_upload(
        frame_menu1,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    dev_info = ui.menu_devinfo(
        frame_menu1,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    status = ui.menu_status(
        frame_menu1,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    tkinter_window_cfg.error = ui.menu_debug(
        frame_menu1,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )

    # Set callbacks for cursor
    cursor.setCallback(status.updateText)
    cursor.setCallback(dev_info.highlightDeviceInfo)
    cursor.setCallback(lambda i: focus_toggle(i, dev_info.keyEntry))

    # Set callbacks for dev_info
    dev_info.setCallback(cursor.deposit)
    dev_info.setCallback(cursor.nodeDetectCallback)
    dev_info.setCallback(lambda i: focus_toggle(i, dev_info.keyEntry))
    dev_info.setCallback(focus_canvas)

    frame_menu2 = tk.LabelFrame(
        frame_menu,
        text="Menu 2",
        width=TKINTER_WIDGET_CONFIG_PANEL_WIDTH / 3.4,
        height=TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
        bg="gray40",
    )
    frame_menu2.pack(side=tk.LEFT, expand=1)
    frame_menu2.pack_propagate(False)

    nodescale = ui.node_scaleshift(
        frame_menu2,
        3,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    # upload2 = ui.img_scaleshift(frame_menu2, 10)
    dev_info2 = ui.img_xyshift(
        frame_menu2,
        10,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    maprefresh2 = ui.map_refresh(
        frame_menu2,
        10,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    jsonview = ui.json_viewer(
        frame_menu2,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )

    frame_canvas.pack(padx=20, pady=20, side=tk.RIGHT)  # Align right with padding
    frame_canvas.pack_propagate(False)  # Fix frame size to dimensions
    tkinter_window_cfg.myCanvas.canvas.pack(padx=10, pady=10)  # Set padding

    tkinter_window_cfg.root.bind(
        "<Escape>", lambda event: destroy(event, tkinter_window_cfg.root)
    )
    tkinter_window_cfg.root.bind(
        "<Control-z>",
        lambda event: focus_toggle_between_sensor_id_frame_and_map_frame(
            event, dev_info.keyEntry
        ),
    )
    ##############################################################################
    # cfg.res.decompile('mc.bin')
    tkinter_window_cfg.myCanvas.canvas.focus_set()

    tkinter_window_cfg.root.mainloop()


def destroy(event, root):
    root.destroy()


def main():
    setup()
