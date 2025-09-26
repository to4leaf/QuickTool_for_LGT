# -*- coding: utf-8 -*-
import os
import glob
import nuke
import nukescripts

from QuickTool_forLGT.Moudules import open_mm_end_ver, set_template


def run():   
    x_pos, y_pos = get_position()
    
    mm_read = open_mm_end_ver.run()
    if mm_read == None:
        return 'mm issue'

    template_nodes = set_template.run()

    for mm in mm_read:    
        mm.setXYpos(mm.xpos() + 1800, mm.ypos())

    for tn in template_nodes:    
        tn.setXYpos(tn.xpos() - 200, tn.ypos() + 3200)


def get_position():
    n = nuke.createNode("NoOp")
    x_pos = n.xpos()
    y_pos = n.ypos()
    nuke.delete(n)    
    
            
    return x_pos, y_pos
    
