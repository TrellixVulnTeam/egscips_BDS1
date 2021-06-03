from ...commons.constants import *
import tkinter as tk
from ... import config
from ..widgets.widgets import *
from .. import controller 


def set_up_map_panel(root):
    ### Creation of GUI map ###
    # Set frame to embed canvas
    map = tk.LabelFrame(
        root,
        text=TKINTER_WIDGET_MAP_TEXT_TITLE,
        width=TKINTER_WIDGET_MAP_WIDTH,
        height=TKINTER_WIDGET_MAP_HEIGHT,
        bg=TKINTER_WIDGET_MAP_COLOUR_BACKGROUND,
    )
    return map


def set_up_config_panel(root):
    config_panel = tk.LabelFrame(
        root,
        text = TKINTER_WIDGET_CONFIG_PANEL_TEXT_TITLE,
        width = TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        height = TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
        bg = TKINTER_WIDGET_CONFIG_PANEL_COLOUR_BACKGROUND,
    )
    config_panel.pack_propagate(False)   

    config_panel.pack(
        padx = TKINTER_WIDGET_DEFAULT_PADX, 
        pady = TKINTER_WIDGET_DEFAULT_PADY, 
        side = tk.LEFT, 
        #expand = 0, 
        #anchor = "n"
        )
    return config_panel

def set_up_config_menu_labelframe(parent_frame):
    config_menu_labelframe = tk.Canvas(
        parent_frame, 
        #borderwidth=0, 
        bg = TKINTER_WIDGET_CONFIG_MENU_LABELFRAME_COLOUR_BACKGROUND, 
        # Ensures that even when focused, the default white ugly focus line around the 
        # border will not appear.
        highlightbackground = TKINTER_WIDGET_CONFIG_MENU_LABELFRAME_COLOUR_BACKGROUND
    )

    config_menu_labelframe.pack(
        side=tk.LEFT, 
        expand=True, 
        fill="both")

    # Implements a scrollbar that allows scrolling down the left menu panel.
    yscroll = tk.Scrollbar(
        parent_frame, 
        orient = "vertical", 
        command = config_menu_labelframe.yview)

    yscroll.pack(
        padx = TKINTER_WIDGET_DEFAULT_PADX, 
        pady = TKINTER_WIDGET_DEFAULT_PADY, 
        side = tk.LEFT, 
        fill = tk.Y)

    config_menu_labelframe.configure(yscrollcommand=yscroll.set)
    return config_menu_labelframe

def set_up_left_menu_labelframe(parent_frame):
    
    TKINTER_WIDGET_LEFT_MENU_TEXT_TITLE = "Menu 1"
    left_menu_labelframe = tk.LabelFrame(
        parent_frame,
        text = TKINTER_WIDGET_LEFT_MENU_TEXT_TITLE,
        width = TKINTER_WIDGET_LEFT_MENU_WIDTH,
        height = TKINTER_WIDGET_LEFT_MENU_HEIGHT,
        bg = TKINTER_WIDGET_LEFT_MENU_COLOUR_BACKGROUND,
    )
    left_menu_labelframe.pack(
        side = tk.LEFT, 
        expand = 1, 
        fill = tk.X)
    left_menu_labelframe.pack_propagate(False)
    return left_menu_labelframe

def set_up_right_menu_labelframe(parent_frame):

    right_menu_labelframe = tk.LabelFrame(
        parent_frame,
        text = TKINTER_WIDGET_RIGHT_MENU_TEXT_TITLE,
        width = TKINTER_WIDGET_RIGHT_MENU_WIDTH,
        height = TKINTER_WIDGET_RIGHT_MENU_HEIGHT,
        bg = TKINTER_WIDGET_RIGHT_MENU_COLOUR_BACKGROUND,
    )
    right_menu_labelframe.pack(side=tk.LEFT, expand=1)
    right_menu_labelframe.pack_propagate(False)
    return right_menu_labelframe

def set_up_widgets_in_left_menu_labelframe(parent_frame, cursor):
    help = menu_help(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    upload = menu_upload(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    dev_info = menu_devinfo(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    status = menu_status(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    config.error = menu_debug(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )

    # Set callbacks for cursor.

    # Update the text on status menu.
    cursor.setCallback(status.updateText)

    # Change the colour on the textbox under dev_info to enter.
    cursor.setCallback(dev_info.highlightDeviceInfo)

    # Toggle focus to textbox so that user can enter values.
    cursor.setCallback(lambda i: controller.focus_toggle(i, dev_info.keyEntry))

    # Set callbacks for dev_info

    # Deposit a square onto cursor position
    dev_info.setCallback(cursor.deposit)

    # Change colour of node when its sensor id is entered.
    dev_info.setCallback(cursor.nodeDetectCallback)
    
    # Toggle focus to textbox so that user can enter values.
    dev_info.setCallback(lambda i: controller.focus_toggle(i, dev_info.keyEntry))

    # Focus on canvas after the sensor id is correctly set.
    dev_info.setCallback(controller.focus_canvas)

    config.root.bind(
        "<Control-z>",
        lambda event: controller.focus_toggle_between_sensor_id_frame_and_map_frame(
            event, dev_info.keyEntry
        ),
    )

def set_up_widgets_in_right_menu_labelframe(parent_frame):
    nodescale = node_scaleshift(
        parent_frame,
        3,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    # upload2 = img_scaleshift(frame_menu2, 10)
    dev_info2 = img_xyshift(
        parent_frame,
        10,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    maprefresh2 = map_refresh(
        parent_frame,
        10,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )
    jsonview = json_viewer(
        parent_frame,
        TKINTER_WIDGET_CONFIG_PANEL_WIDTH,
        TKINTER_WIDGET_CONFIG_PANEL_HEIGHT,
    )