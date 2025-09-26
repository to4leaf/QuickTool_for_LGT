# -*- coding: utf-8 -*-
import nuke
import nukescripts


try:
    import shotgrid
    reload(shotgrid)
except:
    pass
    

def run():

    x_pos, y_pos = get_position()
    nodes = get_setup_nodes()
    print nodes
    for i in nodes:
        i.setXYpos(i.xpos() + x_pos, i.ypos() + y_pos)    
       
        
def get_setup_nodes():
    nodes = []
    nukescripts.clear_selection_recursive()
    shotgrid.nuke_setup()

    sel_node = nuke.selectedNode()
    if sel_node.Class() == 'Read':
        nodes.append(sel_node)

    all_backdrops = nuke.allNodes('BackdropNode')
    for i in all_backdrops:
        if i.xpos() == 200 and i.ypos() == 0:
            nodes.append(i)        

    all_Viewer = nuke.allNodes('Viewer')
    for j in all_Viewer:
        if j.xpos() == 0 and j.ypos() == 200:
            nodes.append(j)        

    return nodes
    
    
def get_position():
    n = nuke.createNode("NoOp")
    x_pos = n.xpos()
    y_pos = n.ypos()
    nuke.delete(n)    
    
    return x_pos, y_pos                  
      
    
    

