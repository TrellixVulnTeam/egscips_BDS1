import sys
import os

# import redis

from os.path import dirname as dir
from src import admin_map_creator as mc

"""
Access point to launch the program.
Do note of the following points before development:
1. Please look up to how set up an executable file for this. I remembered that when I had to do it it was kind of painful due to the 
   import weirdness in Python. I have commented these out but they may be needed when you debug or something.

2. In the event of debug, I recalled writing log statements on a text file. Probably a dumb way but yeah.
"""
# _root = dir(dir(dir(sys.executable)))
# _root = dir(dir(dir(__file__)))
# print(_root)
# sys.path.append(os.path.join(_root, "Node Manager"))
# sys.path.append(os.path.join(_root, "Redis"))
# sys.path.append(os.path.join(_root))


if __name__ == "__main__":
    mc.main()
