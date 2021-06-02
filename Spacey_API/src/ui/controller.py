from platform import system as platf
from tkinter import *


def set_window_icon(window_config):
    # Icon of the window
    if platf() == "Linux":
        img = PhotoImage(file=window_config.gif_path)
        window_config.root.tk.call("wm", "iconphoto", window_config.root._w, img)
    elif platf() == "Windows":
        window_config.root.iconbitmap(window_config.icon_path)
