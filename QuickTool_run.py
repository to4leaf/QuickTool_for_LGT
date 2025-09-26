# -*- coding: utf-8 -*-
'''
__ author __ = lighting_joonsoo

'''
import os
import re
import glob
import nuke
import random
import subprocess
import nukescripts
import collections

from functools import partial

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import frequently_path as fp 
import QuickTool_ui 

from Moudules import drop_events_moudule
from QuickTool_forLGT.Moudules import get_plate, open_mm_end_ver, set_template, set_proj_all



class Widget():
    def __init__(self, mainUI, toolName): 
   
        # Load UI.
        self.ui = QuickTool_ui.Ui(mainUI, toolName)    

        # 초기셋팅 
        self.ui.path_lineedit.setText(fp.get_precomp_path())               
        self.set_filesystem_tree()
        self.ui.items_treeview.setColumnWidth(0, 300)
        self.ui.backdrop_radio2.setChecked(True)                  
        # Connect Button Command.        
        self.ui.path_btn.clicked.connect(partial(self.set_browser_btn, self.ui.path_lineedit))     
        self.ui.share_macro_btn.left_clicked.connect(self.share_macro)                 
        self.ui.backdrop_get_color.clicked.connect(self.set_color_button)     
        # step01 buttons     
        self.ui.getMM_btn.left_clicked.connect(self.mm_btn_click)     
        self.ui.getPlate_btn.left_clicked.connect(self.plate_btn_click)  
        self.ui.setTemplate_btn.left_clicked.connect(self.template_btn_click)  
        self.ui.all_btn.left_clicked.connect(self.all_btn_click)              
        # quick left click buttons
        self.ui.palette_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.palette_btn))                            
        self.ui.macro_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.macro_btn))   
        self.ui.gizmo_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.gizmo_btn))   
        self.ui.lgt_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.lgt_btn))
        self.ui.wip_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.wip_btn))                
        self.ui.mm_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.mm_btn))                                       
        self.ui.comp_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.comp_btn))    
        self.ui.plate_btn.left_clicked.connect(lambda:self.quick_btn_grp(self.ui.plate_btn))  
        # quick double click buttons
        self.ui.palette_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.palette_btn))                            
        self.ui.macro_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.macro_btn))   
        self.ui.gizmo_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.gizmo_btn))   
        self.ui.lgt_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.lgt_btn))
        self.ui.wip_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.wip_btn))                
        self.ui.mm_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.mm_btn))                                       
        self.ui.comp_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.comp_btn))    
        self.ui.plate_btn.double_clicked.connect(lambda:self.quick_double_click(self.ui.plate_btn))
        # right click on treeview
        self.ui.items_treeview.clicked.connect(self.treeview_add_action)      
        #
        self.ui.path_lineedit.textChanged.connect(self.set_filesystem_tree)
  

    # step01 buttons, below 4
    def mm_btn_click(self):
        open_mm_end_ver.run()
        
    def plate_btn_click(self):
        get_plate.run()

        
    def template_btn_click(self):
        set_template.run()
        
        
    def all_btn_click(self):
        set_proj_all.run()


    # 경로 관련, 밑으로 2개
    def set_browser_btn(self, widget):
        # get path at browser
        get_path = self.ui.path_lineedit.text()
        set_path = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select Folder', get_path)
        if not set_path:
            return
        widget.setText(set_path)
        
        
    def set_filesystem_tree(self):
        # get filesystem
        get_path = self.ui.path_lineedit.text()
        self.model_file_system = QFileSystemModel()
        self.model_file_system.setRootPath(get_path)
        self.model_file_system.setReadOnly(True)
        
        self.ui.items_treeview.setModel(self.model_file_system)       
        self.ui.items_treeview.setRootIndex(self.model_file_system.index(get_path))           
        
        
    # 버튼 관련, 밑으로 2개
    def quick_btn_grp(self, btn):
        # left_clicked / set tree view path
        btn_name = btn.objectName()  
        self.ui.backdrop_check_btn.setChecked(False)
        self.ui.backdrop_radio3.setChecked(True)            
        if btn_name == 'Palette':
            change_value = fp.get_precomp_path()
            self.ui.backdrop_check_btn.setChecked(True)
            self.ui.backdrop_radio2.setChecked(True) 
        elif btn_name == 'Macro':
            change_value = fp.get_macro_path()
        elif btn_name == 'Gizmo':
            change_value = fp.get_gizmo_path()  
        elif btn_name == 'lgt':       
            change_value = nuke.script_directory()  
        elif btn_name == 'wip':       
            change_value = fp.get_wip_path()                 
        elif btn_name == 'mm':
            change_value = fp.get_mm_path()                   
        elif btn_name == 'comp':
            change_value = fp.get_comp_path()                  
        elif btn_name == 'plate':
            change_value = fp.get_plate_path()                        
              
        if not change_value:
            change_value = 'Save or open your project'               
            
        self.ui.path_lineedit.setText(change_value)   
        self.set_filesystem_tree()


    def quick_double_click(self, btn):
        # open linux folder
        btn_name = btn.objectName()
        
        scene_loc = nuke.script_directory()            
        if scene_loc == "":
            printInfo = "open your project"
            nuke.message(printInfo)
        else:
            try:
                if btn_name == 'Palette':
                    change_value = fp.get_precomp_path()
                elif btn_name == 'Macro':
                    change_value = fp.get_macro_path()
                elif btn_name == 'Gizmo':
                    change_value = fp.get_gizmo_path()  
                elif btn_name == 'lgt':       
                    change_value = scene_loc 
                elif btn_name == 'wip':       
                    change_value = fp.get_wip_path()                 
                elif btn_name == 'mm':
                    change_value = fp.get_mm_path()                   
                elif btn_name == 'comp':
                    change_value = fp.get_comp_path()                  
                elif btn_name == 'plate':
                    change_value = fp.get_plate_path()       
                                                         
                subprocess.Popen(['xdg-open', change_value])   
            except:
                notinfo = "not found dirtory"
                nuke.message(notinfo)
           

    def share_macro(self):
        # share macro button function
        if nuke.nodesSelected() == True:
            win = QuickTool_ui.SubWindow()
            r = win.showModal()

            if r[0] == 1:
                #get path
                ori_path = fp.get_macro_path()
                add_path = r[1]
                # 확장자 안붙였을 경우 
                if not add_path.endswith('.nk'):
                    add_path = r[1] + '.nk'
                new_path = os.path.join(ori_path, add_path)       
                # 경로가 없을 경우
                if not os.path.isdir(os.path.dirname(new_path)):
                    os.makedirs(os.path.dirname(new_path))

                # get nodes                
                nuke.nodeCopy("%clipboard%")    
                clipboard = QtWidgets.QApplication.clipboard()
                script = clipboard.text()
                nukescripts.clear_selection_recursive()
                #
                with open(new_path, 'w') as temp_file:
                    temp_file.write(script)
                    
            else:
                return                
        else:
            info = "노드를 선택해주세요"
            nuke.message(info)
            return
     
     
            
    # 트리뷰 엑션버튼 관련, 마우스 오른쪽 버튼 기능
    def treeview_add_action(self):
        exist_action = self.ui.items_treeview.actions()
        for i in exist_action:
            self.ui.items_treeview.removeAction(i)    
        
        #디폴트값 생성 
        action_into = QAction('Into', self.ui.items_treeview)     
        action_into.triggered.connect(partial(self.go_to_child_folder))     
        action_back = QAction('Back', self.ui.items_treeview)   
        action_back.triggered.connect(self.go_to_parent_folder)
        action_reload = QAction('reload', self.ui.items_treeview)
        action_reload.triggered.connect(self.set_filesystem_tree)                  
        action_line1 = QAction(' ', self.ui.items_treeview)
        action_line1.setSeparator(True)    

        self.ui.items_treeview.addAction(action_into)       
        self.ui.items_treeview.addAction(action_back)  
        self.ui.items_treeview.addAction(action_reload)            
        self.ui.items_treeview.addAction(action_line1)     
        
        action1 = QAction('Drop Items', self.ui.items_treeview)
        action1.triggered.connect(partial(drop_items_run, self.get_items()))              
        self.ui.items_treeview.addAction(action1)       
    
        #precomp 템플릿 생성
        all_node =  nuke.allNodes()
        for j in all_node: 
            if 'Constant' ==  j.Class():
                if 'start_lgt_constant' in j.name():      
                    action3 = QAction(j.name(), self.ui.items_treeview)          
                    action3.triggered.connect(partial(set_items_run, j, self.get_items()))                                 
                    self.ui.items_treeview.addAction(action3)


    def go_to_child_folder(self):
        try:
            sel_item = self.ui.items_treeview.selectedIndexes()            
            sel_index = self.ui.items_treeview.selectedIndexes()[-2]
            sel_name = self.ui.items_treeview.selectedIndexes()[-4].data()                
            sel_info = self.ui.items_treeview.model().fileInfo(sel_index)
            sel_path = sel_info.absoluteFilePath()
            
            self.ui.path_lineedit.setText(sel_path) 
        except:
            print 'into error'

    
    def go_to_parent_folder(self):
        get_path = self.ui.path_lineedit.text()
        parent_folder = os.path.abspath(os.path.join(get_path, os.pardir))
        self.ui.path_lineedit.setText(parent_folder)            
        
                                
    def get_items(self):
        # get selected items at treeview

        sel_item = self.ui.items_treeview.selectedIndexes()
        item_dict = collections.OrderedDict()

        for i in range(len(sel_item)):
            # 인덱스 이슈 - name부터 date까지 다 불러옴
            try:
                item_name = str(self.ui.items_treeview.selectedIndexes()[i].data())
            except:
                item_name = 'blank'
                
            path = str(self.model_file_system.filePath(sel_item[i]))          
            if path not in item_dict:
                sub_item_dict = {}
                #get color
                color = None
                if self.ui.backdrop_check_btn.isChecked():
                    if self.ui.backdrop_radio1.isChecked(): # self color
                        color = self.ui.backdrop_get_color.palette().button().color().getRgb()
                    elif self.ui.backdrop_radio2.isChecked(): # random
                        color = ramdon_color()
                    elif self.ui.backdrop_radio3.isChecked(): # gray
                        color = (125, 125, 125, 255)    
                                                      
                if color != None:                      
                    color = rgb2hex(color)
                sub_item_dict = {'name': item_name, 'color': color}
                item_dict[path] = sub_item_dict
        return item_dict
      
  
    def set_color_button(self):
        V = dec2hex(nuke.getColor(4294967295)).rjust(8, "0")
        R = int(V[0:2], 16) 
        G = int(V[2:4], 16) 
        B = int(V[4:6], 16) 
        A = int(V[6:8], 16) 
        RGB = R, G, B

        if not V == 'ffffffff':
            self.ui.backdrop_get_color.setStyleSheet('background-color:rgb({0}, {1}, {2})'.format(R, G, B))



# 아이템 드랍 관련, 밑으로 2개
def drop_items_run(item_list):
    # drop items in nodegraph
    undo = nuke.Undo()  
    undo.name('Drop Item')
    undo.begin()
    # get position
    n = nuke.createNode("NoOp")
    x_pos = n.xpos()
    y_pos = n.ypos()
    nuke.delete(n)

    for key, value in item_list.items():
        # 젠팔렛트
        if os.path.isdir(key):       
            if not re.match('v\d\d\d', os.path.basename(key)) and 'precomp/r' in key:
                if os.path.isdir(key):
                    y_pos_palette = drop_events_moudule.run_palette(key, value.get('color'), x_pos, y_pos)
                    y_pos = y_pos_palette + 300                     

                    
        # 노드들                    
        elif os.path.isfile(key):
            if os.path.basename(key).endswith('.gizmo'):
                drop_events_moudule.get_gizmo(key)   


    undo.end()
    return 
    
    
def set_items_run(node, item_list):
    # set nodes in palette
    undo = nuke.Undo()  
    undo.name('Set strat constnat lgt')    
    undo.begin()        
    
    get_nodes = drop_events_moudule.find_standard_node(node)
    x_pos = get_nodes[0].xpos()
    y_pos = get_nodes[0].ypos()
    start_node = get_nodes[0]
    
    for key, value in item_list.items():
        if os.path.isdir(key):       
            if not re.match('v\d\d\d', os.path.basename(key)) and 'precomp/r' in key:
                if os.path.isdir(key):  
                    y_pos_palette = drop_events_moudule.run_palette(key, value.get('color'), x_pos + 1400, y_pos + 300)
                    end_node = drop_events_moudule.nodes_setup(start_node, get_nodes[1], value.get('name'), key, x_pos, y_pos)
                    start_node = end_node
                    x_pos = end_node.xpos()
                    y_pos = end_node.ypos()                        
                    
    undo.end()
    return 



# COLOR CONVERT FUNCTION, below 3
def dec2hex(n):
    # convert hex() to hex(16)
    return "%x"%n
    
    
def rgb2hex(item):            
    rgb2hex =  "{:02x}{:02x}{:02x}{:02x}".format(item[0], item[1], item[2], item[3])     
    hex_color = int(rgb2hex, 16)    
    return hex_color

    
def ramdon_color():
    # no rule ramdon 
    levels = range(40, 125, 10)
    random_color = list(random.choice(levels) for _ in range(3))
    random_color.append(255)
    return tuple(random_color)


#
def get_pane():
    for widget in QtWidgets.QApplication.allWidgets():
        if  widget.objectName() == 'QuickTool_forLGT':
            return widget
            
          
# Show the panel
def toggle_visiblity():     
    #   
    if not get_pane():
        srPanel = Widget('', 'QuickTool_forLGT')
        srPanel.ui.show()
        
    else:
        if get_pane().isVisible():
            get_pane().window().setVisible(False)
            get_pane().items_treeview.clearSelection()
        else:
            get_pane().window().setVisible(True)
    
           




                

