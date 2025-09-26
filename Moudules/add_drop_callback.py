# -*- coding: utf-8 -*-
import os
import re
import nuke
import nukescripts
import collections

from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtWidgets import *

from QuickTool_forLGT import QuickTool_run
from QuickTool_forLGT.Moudules import drop_events_moudule


def get_pane():
    for widget in QtWidgets.QApplication.allWidgets():
        if  widget.objectName() == 'QuickTool_forLGT':
            return widget


def get_items():
    # get selected items at treeview
    sel_item = get_pane().items_treeview.selectedIndexes()
    get_pane().items_treeview.clearSelection()

    item_dict = collections.OrderedDict()
    for i in range(len(sel_item)):
        try:
            item_name = str(get_pane().items_treeview.selectedIndexes()[i].data())
        except:
            item_name = 'blank'
  
        model_file_system = QFileSystemModel()     
        path = str(model_file_system.filePath(sel_item[i]))          
        if path not in item_dict:
            sub_item_dict = {}
            #get color
            color = None
            if get_pane().backdrop_check_btn.isChecked():
                if get_pane().backdrop_radio1.isChecked(): # self color
                    color = get_pane().backdrop_get_color.palette().button().color().getRgb()
                elif get_pane().backdrop_radio2.isChecked(): # random
                    color = QuickTool_run.ramdon_color()
                elif get_pane().backdrop_radio3.isChecked(): # gray
                    color = (125, 125, 125, 255)    
                                                  
            if color != None:                      
                color = QuickTool_run.rgb2hex(color)
            sub_item_dict = {'name': item_name, 'color': color}
            item_dict[path] = sub_item_dict           
    return item_dict


def lgt_dropper(mimeType, text):
    nuke.Undo().new()
    
    if 'text/plain' == mimeType:
        # precomp/r1 하위 폴더만 적용
        if not re.match('v\d\d\d', os.path.basename(text)) and 'precomp/r1' in text and os.path.isdir(text):
            # 체킹 그룹에 들어가 있는 이름으로 드랍시 원하지 않게 드랍이 되고 드랍할 필요가 없는 경우의 수
            check_grp = ['r1', 'r2', 'r3', 'r4']                
            if os.path.basename(text) not in check_grp:                
                pane = get_pane()
                sel_item = pane.items_treeview.selectedIndexes()                    
                # Quick tool에서만 실행 가능하게, 일반 폴더로는 멀티 드랍 알고리즘이 안 떠올라서
                if pane.isVisible():
                    # 멀티 드랍 언두 이슈, 따로 빼지 않으면 쓸모없는 스택이 계산됨
                    if sel_item:
                        QuickTool_run.drop_items_run(get_items()) 
                        return True               
                    else:
                        return True                    
                                  
        # 일단은 모든 기즈모,                                                                 
        if os.path.isfile(text) and os.path.basename(text).endswith('.gizmo'):
            QuickTool_run.drop_items_run(get_items())
            return True    


nukescripts.addDropDataCallback(lgt_dropper)














