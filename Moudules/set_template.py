# -*- coding: utf-8 -*-
import os
import re
import sys
import nuke
import nukescripts

from PySide2 import QtWidgets

try:
    import shotgrid
    reload(shotgrid)
except:
    pass
    
GLOBAL_NODES = []
    
def run():
    undo = nuke.Undo()  
    undo.name('set_template')    
    undo.begin()         
    template = get_template()
    read_node, node_list = get_template_info(template)
    set_plate(read_node)
    list_numbering(node_list)
    undo.end() 
    
    return GLOBAL_NODES
    
   
def get_template():
    temp = '/storenext/personal/DeptPipeline/library/template/nuke/dept/light/template/defalut_template.nk'

    return temp
    
        
def get_template_info(template):
    global GLOBAL_NODES
    
    nukescripts.clear_selection_recursive()
    
    f = open(template, 'r')
    data = f.read()

    try:
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(data)    
        nuke.nodePaste('%clipboard%')    
    except:
        print ('clipboard issue')

    select_node = nuke.selectedNodes()
    nukescripts.clear_selection_recursive()     
    GLOBAL_NODES = select_node

    read_node = None
    checking_names = ['end_lgt_dot_', 'start_lgt_constant_', 'write_', 'FG_plate_', 'lgt_precomp_']
    node_list = []
    for node in select_node:
        if 'lgt_read' in node.name() and node.Class() == 'Constant':
            read_node = node                     
            GLOBAL_NODES.remove(node)   
        else:
            if re.sub(r'\d', '', node.name()) in checking_names:
                node_list.append(node)
                
    return read_node, node_list
            
            
def set_plate(read_node):
    global GLOBAL_NODES
    
    nukescripts.clear_selection_recursive()
    
    try: 
        shotgrid.nuke_setup()
        plate_node = nuke.selectedNode()
        if plate_node.Class() == 'Read':
            plate_node.setXYpos(read_node.xpos(), read_node.ypos())
    except:
        plate_node = nuke.createNode('Constant')     
        plate_node.setXYpos(0, 0)    
        plate_node.setXYpos(read_node.xpos(), read_node.ypos())    
    GLOBAL_NODES.append(plate_node)               
            
    all_backdrops = nuke.allNodes('BackdropNode')
    for i in all_backdrops:
        if i.xpos() == 200 and i.ypos() == 0:
            i.setXYpos(i.xpos() + read_node.xpos(), i.ypos() + read_node.ypos())
            GLOBAL_NODES.append(i)   
    all_Viewer = nuke.allNodes('Viewer')
    for j in all_Viewer:
        if j.xpos() == 0 and j.ypos() == 200:
            j.setXYpos(j.xpos() + read_node.xpos(), j.ypos() + read_node.ypos())
            GLOBAL_NODES.append(j)           

    deps = read_node.dependent()[0]
    deps.setInput(0, plate_node)
    nuke.delete(read_node)   
    



    
    
def start_num():
    ''' 그룹 네이밍 중복피하기 위해 넘버 부여 
        예시) Multi_Make_Alpha1 '''
    all_node = nuke.allNodes('Constant')
    node_list = []
    for i in all_node:
        if 'start_lgt_constant_' in i.name():
            node_list.append(i.name())
            
    if len(node_list) == 0:
        return 1
    else:
        num = 1 
        while True:
            if 'start_lgt_constant_' + str(num) in node_list:
                num += 1
            else:
                return num


    
def list_numbering(node_list):
    NAME_NUM = str(start_num())  

    for node in node_list:
        sub_name = re.sub(r'\d', '', node.name())
        node['name'].setValue(sub_name + NAME_NUM)   
        
        if node.Class() == 'BackdropNode':
            if 'lgt_precomp' in node.name():
                node['label'].setValue(sub_name + NAME_NUM)
            else:            
                node['z_order'].setValue(int(NAME_NUM))
        
        elif node.Class() == 'Constant':
            get_format = nuke.root()['format'].value().name()
            node['format'].setValue(get_format)
        
        else:
            pass
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
