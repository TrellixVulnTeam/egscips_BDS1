import sys
import os

# import redis

from os.path import dirname as dir

#_root = dir(dir(dir(sys.executable)))
_root = dir(dir(dir(__file__)))
print(_root)
sys.path.append(os.path.join(_root, "Node Manager"))
sys.path.append(os.path.join(_root, "Redis"))
sys.path.append(os.path.join(_root))

from src import admin_map_creator as mc

if __name__ == "__main__":
    mc.main()
