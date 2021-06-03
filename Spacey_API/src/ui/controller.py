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

from .. import config
from ..node.node_controller import *
from ..commons.constants import *
from os.path import dirname as dir
from platform import system as platf
from .frame.frame import *

def set_window_icon(root, gif_path, icon_path):
    # Icon of the window
    if platf() == "Linux":
        img = PhotoImage(
            file = gif_path
            )
        root.tk.call("wm", "iconphoto", root._w, img)
    elif platf() == "Windows":
        root.iconbitmap(icon_path)

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
    config.root.destroy()


def focus_toggle_between_sensor_id_frame_and_map_frame(event, widget):
    """
    Toggle focus between sensor id frame and map frame.
    Focus = You can use keyboard controls.
    Called upon when you press Ctrl-Z.
    """
    config.toggle = 1 - config.toggle
    if config.toggle:
        # Set focus to canvas, so that you can use key controls on map
        config.map_canvas.canvas.focus_set()
    else:
        # Set fous to sensor id frame, so you can type values in
        widget.focus_set()


def focus_toggle(mode, widget=None):
    """
    Toggle focus between Map frame, and the widget in question.
    """
    if mode:
        config.map_canvas.canvas.focus_set()
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
    config.root = set_up_tkinter_config(config.root)

    map = set_up_map_panel(config.root)
    # Align right with padding
    map.pack(padx=20, pady=20, side=tk.RIGHT)  
    # Fix frame size to dimensions
    map.pack_propagate(False)  
    ## Configure global variables.

    # Set canvas within map to draw.
    config.map_canvas = map_canvasObject(
        map,
        TKINTER_WIDGET_MAP_WIDTH,
        TKINTER_WIDGET_MAP_HEIGHT,
    )

    # Handles node operations and recording
    config.node_controller = NodeController(
        config.map_canvas.canvas
    )

    # Creates rectangle cursor (in red)
    cursor = CursorNode(config.map_canvas.canvas)

    # Creates gridlines so that the boxes inserted will appear more organised
    config.map_grid = CanvasGridFrame(
        config.map_canvas.canvas, config.scale
    )

    ### Creation of Config menu ###
    config_panel = set_up_config_panel(config.root)

    # Refers to the left menu packed on the config panel.
    config_menu_labelframe = set_up_config_menu_labelframe(config_panel)

    config_menu_frame = tk.Frame(
        config_menu_labelframe, 
        borderwidth = 0, 
        bg = TKINTER_CONFIG_MENU_FRAME_COLOUR_BACKGROUND)

    config_menu_frame.pack()

    left_menu_labelframe = set_up_left_menu_labelframe(config_menu_frame)
    set_up_widgets_in_left_menu_labelframe(left_menu_labelframe, cursor)

    right_menu_labelframe = set_up_right_menu_labelframe(config_menu_frame)
    set_up_widgets_in_right_menu_labelframe(right_menu_labelframe)

    config.map_canvas.canvas.pack(padx=10, pady=10)  # Set padding

    # When the user press escape, the window will exit.
    config.root.bind(
        "<Escape>", lambda event: destroy(event, config.root)
    )

    ##############################################################################
    # cfg.res.decompile('mc.bin')
    config.map_canvas.canvas.focus_set()
    config.root.mainloop()

def set_up_tkinter_config(root):
    """
    Configure tkinter root with basic display settings.
    """
    root = tk.Tk()

    default_font = font.nametofont(TKINTER_DEFAULT_FONT)
    default_font.configure(
        family = TKINTER_DEFAULT_FONT_FAMILY,
        size = TKINTER_DEFAULT_FONT_SIZE)

    # cfg.root.state('zoomed') # Full window view

    # Set title name

    root.title(TKINTER_WINDOW_TITLE)
    # Set BG colour
    root.configure(bg=TKINTER_WINDOW_COLOUR_BACKGROUND)

    # Set Icon of the window
    set_window_icon(
        root,
        config.gif_path,
        config.icon_path
        )

    # cfg.root.iconbitmap(cfg.icon_path)
    # cfg.root.geometry('1280x720')  #size of w
    # config.root.update_idletasks()

    # Set Window size by factor
    window_size_factor = 1

    # cfg.root.geometry(str(int(1366*factor)) + "x" + str(int(768*factor)))  #size of w

    # Set the window size
    root.geometry(
        str(int(TKINTER_WINDOW_DEFAULT_WIDTH * window_size_factor))
        + "x"
        + str(int(TKINTER_WINDOW_DEFAULT_HEIGHT * window_size_factor))
    )  

    # To retain our sanity, strictly disallow users from resizing the window.
    root.resizable(0, 0)

    ### Log current window info ###
    print(root.winfo_height())
    print(root.winfo_width())
    print(root.winfo_geometry())
    print(root.winfo_screenheight())
    print(root.winfo_screenwidth())
    return root



def destroy(event, root):
    root.destroy()


def main():
    setup()
