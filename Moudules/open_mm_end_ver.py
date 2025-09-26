# -*- coding: utf-8 -*-
import os
import re
import glob
import nuke
import nukescripts

from PySide2 import QtWidgets
from create_tex import plate_to_katana

from QuickTool_forLGT.Moudules import get_plate

GLOBAL_NODES = []

def get_mm(files):   
    global GLOBAL_NODES
    
    f = open(files[-1], 'r')
    data = f.read()
    try:
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(data)    
        nuke.nodePaste('%clipboard%')    
    except:
        print ('clipboard issue')

    select_node = nuke.selectedNodes()


    backdrop = nukescripts.autoBackdrop()
    backdrop['tile_color'].setValue(int('%02x%02x%02x%02x' % (0.4*255, 0.4*255, 0.4*255, 1), 16))
    backdrop['label'].setValue(os.path.basename(files[-1]))
    backdrop['note_font_size'].setValue(66)
    select_node.append(backdrop)    
    GLOBAL_NODES = select_node
        
    nukescripts.clear_selection_recursive()    
    get_plate = get_plate_set()
    
    jpg_node, jpg_x_pos, jpg_y_pos = get_jpg_position(select_node)
    get_plate.setXYpos(jpg_x_pos -500, jpg_y_pos)
    
    plate_version = re.findall(r'v\d+', get_plate['file'].value())[0]
    jpg_version = re.findall(r'v\d+', jpg_node['file'].value())[0]
    if jpg_version != plate_version:
        change_ver = get_plate['file'].getValue().replace(plate_version, jpg_version)
        get_plate['file'].setValue(change_ver)
            
    if 'src' in jpg_node['file'].value():
        # file로 찾는 방법
        loc = nuke.script_directory()        
        file_org = os.path.basename(jpg_node['file'].value())
        file_ver =  re.findall(r'v\d+', file_org)[0]

        plate_loc = loc.split('lgt/dev/nuke')[0] + 'plate/src'
        ver_loc = os.path.join(plate_loc, file_ver)        
        file_name = nuke.getFileNameList(ver_loc)[0].split(' ')[0]
        get_plate['file'].setValue(plate_loc + '/' + file_ver + '/' + file_name)
        

    mm_node = get_distort_node(get_plate, jpg_node)

    num = str(start_num())
    tex = tex_wirte(mm_node, num)
    tex_half = tex_wirte_half(mm_node, num)   
            
    return GLOBAL_NODES
    
    
def get_jpg_position(select_node):
    org_list= []
    get_x_pos = 9999999
    get_y_pos = 0
    for i in select_node:
        if get_x_pos > i.xpos():
            get_x_pos = i.xpos()           

        if i.Class() == 'Read':
            if 'org' in i['file'].value():
                get_y_pos = i.ypos()
                return i, get_x_pos, get_y_pos                
            else:            
                for j in select_node:
                    if 'src' in i['file'].value() and 'undistort' not in i['file'].value():
                        get_y_pos = i.ypos()
                        return i, get_x_pos, get_y_pos                    
                    else:
                        org_list.append(i)
                        get_y_pos = i.ypos()                                                 
                        return org_list[0], get_x_pos, get_y_pos                        

    
def get_plate_set():
    global GLOBAL_NODES
    
    nodes = get_plate.get_setup_nodes()
    
    node = None
    for i in nodes:
        if i.Class() == 'Read':
            node = i
        else:
            nuke.delete(i)   
            
    GLOBAL_NODES.append(node)
    return node                
                
    
def get_distort_node(plate_node, org_node):
    global GLOBAL_NODES
    
    dot_node = nuke.createNode('Dot')
    dot_node.setXYpos(plate_node.xpos()+34, plate_node.ypos()+150)  
    GLOBAL_NODES.append(dot_node)    
        
    newNode = dot_node
    nukescripts.clear_selection_recursive()
    distort_nodes = downstream(org_node)

    distort_nodes.reverse()


    nukescripts.clear_selection_recursive()
    if distort_nodes != None:
        newNode.setSelected(True)
        d_yos = plate_node.ypos() +150
        d_xos = plate_node.xpos()
        for d_node in distort_nodes:
            if d_node.Class() != 'Read' and d_node.Class() != 'Viewer' and d_node.Class() != 'ScanlineRender':
                newNode = nuke.createNode(d_node.Class(), d_node.writeKnobs(nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT), inpanel=False)
                d_yos += 50
                newNode.setXYpos(d_xos, d_yos)
                GLOBAL_NODES.append(newNode)    
                if d_node.Class() == 'Reformat':
                    break
                    
        
                      
    return newNode
       
       
def downstream(node):
    if not node.dependent():
        return

    deps = node.dependent()
    for dep in deps:
        dep.setSelected(True)
        if dep.Class() == 'ScanlineRender':
            slected_nodes = nuke.selectedNodes()
            return slected_nodes

        if not dep.dependent():
            continue
        downstream(node=dep)
    slected_nodes = nuke.selectedNodes()
    return slected_nodes
    

def start_num():
    ''' 그룹 네이밍 중복피하기 위해 넘버 부여 '''
    all_node = nuke.allNodes('Group')
    node_list = []
    for i in all_node:
        if 'Write_Tex_org' in i.name():
            node_list.append(i.name())
            
    if len(node_list) == 0:
        return 1
    else:
        num = 1 
        while True:
            if 'Write_Tex_org' + str(num) in node_list:
                num += 1
            else:
                return num
      
      
def tex_wirte(mm_node, num):
    global GLOBAL_NODES
    
    tex_wirte1 = plate_to_katana.write_tex_UI()
    tex_wirte1.setXYpos(mm_node.xpos()-70, mm_node.ypos()+100)
    tex_wirte1.setInput(0, mm_node)   
    tex_wirte1['name'].setValue( 'Write_Tex_org' + num ) 
    
    tex_wirte1['default'].setValue(0)
    button1 = tex_wirte1.knob('SetUP')    
    nuke.Script_Knob.execute(button1)   
    
    GLOBAL_NODES.append(tex_wirte1)    
    return tex_wirte1      

    
def tex_wirte_half(mm_node, num):
    global GLOBAL_NODES
    
    reformat_05 = nuke.createNode('Reformat')
    reformat_05['type'].setValue('scale')
    reformat_05['scale'].setValue(0.5)      
    reformat_05.setXYpos(mm_node.xpos()+70, mm_node.ypos()+50) 
    reformat_05.setInput(0, mm_node)
        
    tex_wirte2 = plate_to_katana.write_tex_UI()    
    tex_wirte2.setXYpos(reformat_05.xpos(), reformat_05.ypos()+50)              
    tex_wirte2['name'].setValue( 'Write_Tex_half' + num )    
            
    tex_wirte2['default'].setValue(0)
    button2 = tex_wirte2.knob('SetUP')
    nuke.Script_Knob.execute(button2)    
    file2 = tex_wirte2['file'].getValue().replace('exr/bg_plate.%4d.exr', 'exr_half/bg_plate_half.%4d.exr')
    tex_wirte2['file'].setValue(file2)
    texfile2 = tex_wirte2['TexFile'].getValue().replace('tex', 'tex_half')
    tex_wirte2['TexFile'].setValue(texfile2)
    
    GLOBAL_NODES.append(reformat_05)    
    GLOBAL_NODES.append(tex_wirte2)                   
    return tex_wirte2
          
      
def run():
    undo = nuke.Undo()  
    undo.name('get_MM')    
    undo.begin()
    loc = nuke.script_directory()

    mm_loc = loc.replace('lgt/dev/nuke', 'mm/pub/nuke')

    if mm_loc == '':
        printInfo = '누크를 저장하거나 열어주세요.'
        nuke.message(printInfo)
        return    
       
    files = glob.glob(os.path.join(mm_loc, '*.nk'))
    files.sort()    

    if files == [] or files == None:
        printInfo = 'mm폴더에 누크파일이 없습니다.'
        nuke.message(printInfo)
        return        
           
    get_data = get_mm(files)
    nukescripts.clear_selection_recursive()     
    undo.end()    
    
    return get_data
    

#def run3(path):
def run_no_gui(path):
    undo = nuke.Undo()  
    undo.name('get_MM')        
    undo.begin()
    loc = os.path.dirname(path)

    files = glob.glob(os.path.join(loc, '*.nk'))
    files.sort()

    if files == [] or files == None:
        print ('No nuke file in mm folder')
        return        

    get_data = get_mm(files)  
    nukescripts.clear_selection_recursive()     
    undo.end()    
    
    return get_data























