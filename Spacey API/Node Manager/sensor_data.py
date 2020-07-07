from tkinter import *
import classdef as spc
from tkinter import filedialog
import config as cfg
from sensor_data import *
import json

class RestaurantSpace(object):
    def __init__(self, canvas):
        self.idxList = []
        self.x_coord = {}
        self.y_coord = {}
        self.space_id = {}
        self.device_cluster_level = {}
        self.device_cluster_id = {}
        self.size = 0
        self.dict_sensor_motes = {}
        self.canvas = canvas
        self.devinfo = ["x_coord", "y_coord", "space_id", "device_cluster_level", "device_cluster_id", "idxList"]
    
    def changeNodeSize(self):
        for i in self.idxList:
            x = self.x_coord[i]
            y = self.y_coord[i]
            cfg.myCanvas.canvas.coords(cfg.myCanvas.rec_obj[i], x-cfg.box_len, y-cfg.box_len, x+cfg.box_len, y+cfg.box_len)
        

    def registerNode(self,x,y,space,level,id, obj):
        
        newMote = sensor_mote_data(self)
        self.idxList.append(newMote.idx)
        self.x_coord[newMote.idx] = x
        self.y_coord[newMote.idx] = y
        self.space_id[newMote.idx] = space
        self.device_cluster_level[newMote.idx] = level
        self.device_cluster_id[newMote.idx] = id 
        cfg.myCanvas.placeNode(newMote.idx, x, y)
        self.dict_sensor_motes[(x,y)] = newMote
        self.size += 1
        """
        print("added")
        print(len(self.device_cluster_id))
        print(len(self.device_cluster_level))
        print(len(self.space_id))
        print(len(self.x_coord))
        print(len(self.y_coord))
        """
    
    def deleteNode(self,x,y):
        idx = self.dict_sensor_motes[(x,y)].idx
        print(idx)
        del self.x_coord[idx]
        del self.y_coord[idx]
        del self.space_id[idx]
        del self.device_cluster_level[idx]
        del self.device_cluster_id[idx]
        del self.idxList[int(idx)]
        self.size -= 1

        cfg.myCanvas.deleteNode(idx)

        del self.dict_sensor_motes[(x,y)]
        print(self.device_cluster_id)
        print(self.device_cluster_level)
        print(self.space_id)
        print(self.x_coord)
        print(self.y_coord)

    def deleteAllNodes(self):
        self.x_coord.clear()
        self.y_coord.clear()
        self.space_id.clear()
        self.device_cluster_level.clear()
        self.device_cluster_id.clear()

        for i in self.idxList:
            cfg.myCanvas.deleteNode(i)
            self.size -= 1
        self.idxList.clear()
     
        cfg.myCanvas.rec_obj.clear()
        if cfg.error is not None:
            cfg.error.updateText("Deleted all Nodes", "orange")

    def unpackFromJson(self):
        for idx in self.idxList:
            x = self.x_coord[idx]
            y = self.y_coord[idx]
            self.dict_sensor_motes[(x,y)] = sensor_mote_data(self)
            self.size += 1

        for i in self.idxList:
            print("xcoord: " + str(self.x_coord.get(i)))
            x = self.x_coord.get(i)
            y = self.y_coord.get(i)
            cfg.myCanvas.placeNode(i, x, y)
    
    def printMoteAt(self,x, y):
        if (x,y) in self.dict_sensor_motes.keys():
            return(self.dict_sensor_motes[(x,y)].printMote())
        else:
            print("No mote here")
        
    
    

class sensor_mote_data(object):
    def __init__(self,res):
        self.idx = str(res.size)
        self.res = res
    
    def printMote(self):
        print(self.idx)
        print(self.res.device_cluster_id)
        return ("Mote x: " + str(self.res.x_coord[self.idx])
        + "\nMote y: " + str(self.res.y_coord[self.idx])
        + "\nMote space: " + str(self.res.space_id[self.idx])
        + "\nMote cluster level: " + str(self.res.device_cluster_level[self.idx])
        + "\nMote cluster id: " + str(self.res.device_cluster_id[self.idx]) 
        )


  
        