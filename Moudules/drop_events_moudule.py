# -*- coding: utf-8 -*-
import re
import os
import sys
import random

import nuke
import nukescripts

from PySide2 import QtWidgets



def run_palette(path, color, x_pos, y_pos):
    #group list
    MAIN_GRP = ['primary', 'ML', 'LPE', 'MatteID', 'LOBE', 'DeepID']
    DENOISE_GRP = ['Denoise', 'Filtered']
    EXTRA_GRP = ['Extra']
    SHADOW_GRP = ['Occ', 'Holdout']
    ELSE_GRP = []    
    main_count = 0 

    #PATH_LIST = os.listdir(path)
    PATH_LIST = nuke.getFileNameList(path)
    if 'DeepID' in PATH_LIST:
        deep_index = PATH_LIST.index('DeepID')
        PATH_LIST[deep_index], PATH_LIST[-1] = PATH_LIST[-1], PATH_LIST[deep_index]
    if 'MatteID' in PATH_LIST:
        matte_index = PATH_LIST.index('MatteID')
        PATH_LIST[matte_index], PATH_LIST[-2] = PATH_LIST[-2], PATH_LIST[matte_index]
    
    # issue(포지션값에 대한 변수들)
    for i in PATH_LIST:
        if i in MAIN_GRP:
            main_count += 1
        elif i in DENOISE_GRP or i in EXTRA_GRP or i in SHADOW_GRP:
            continue  
        else:
            i_path = os.path.join(path, i)
            ELSE_GRP.append(i)
                
    # xpos grp
    main_xpos = x_pos
    denoise_xpos = main_xpos
    extra_xpos = denoise_xpos
    shadow_xpos = extra_xpos 
    else_xpos = shadow_xpos

    #ypos grp
    main_ypos = y_pos
    if main_count == 0:
        main_ypos -= 150 
    denoise_ypos = main_ypos
    if 'Denoise' in PATH_LIST or 'Filtered' in PATH_LIST:
        denoise_ypos += 150 
    extra_ypos = denoise_ypos
    if 'Extra' in PATH_LIST:
        extra_ypos += 150 
    shadow_ypos = extra_ypos
    if 'Occ' in PATH_LIST or 'Holdout' in PATH_LIST:
        shadow_ypos += 150 
    else_ypos = shadow_ypos
    if len(ELSE_GRP) != 0:
        else_ypos += 150


    # crete_node
    for folder in PATH_LIST:
        add_path = os.path.join(path, folder)
        
        # empty_file(폴더는 존재하지만 파일이 없을때)
        if nuke.getFileNameList(add_path) == []:
            continue
        else:
            file_name = nuke.getFileNameList(add_path)

        # pattern_grp
        if folder in MAIN_GRP:
            if folder != 'DeepID':
                get_xpos = set_read_node(add_path, file_name[0], main_xpos, main_ypos, check=False)
                main_xpos = get_xpos + 100
            else:
                get_xpos = create_deep(add_path, file_name[0], main_xpos, main_ypos)

        elif folder in DENOISE_GRP:    
            if folder == 'Filtered':
                denoise_xpos += 40

            for denoise_folder in os.listdir(add_path):
                get_xpos = set_read_node(add_path, denoise_folder, denoise_xpos, denoise_ypos)
                denoise_xpos = get_xpos + 100

        elif folder in EXTRA_GRP:    
            for extra_folder in os.listdir(add_path):
                get_xpos = set_read_node(add_path, extra_folder, extra_xpos, extra_ypos)
                extra_xpos = get_xpos + 100

        elif folder in SHADOW_GRP and path.endswith('Occ') == False:    
            for shadow_folder in os.listdir(add_path):
                get_xpos = set_read_node(add_path, shadow_folder, shadow_xpos, shadow_ypos)
                shadow_xpos = get_xpos + 100      
        # unknown pattern (패턴을 알 수 없을 경우 무작정 불러오기,  오류 있을 수 있음..)
        else:
            if ".exr" in folder:
                if 'DeepID' in folder:
                    get_xpos = create_deep(path, folder, else_xpos, else_ypos)
                    else_xpos = get_xpos + 100   
                else:
                    get_xpos = set_read_node(path, folder, else_xpos, else_ypos, check=False)
                    else_xpos = get_xpos + 100        
  
            elif "#" in file_name[0]:   
                get_xpos = set_read_node(add_path, file_name[0], else_xpos, else_ypos, check=False)
                else_xpos = get_xpos + 100
                
            else:          
                # add else path
                for else_file in file_name:
                    if else_file != 'Extra':
                        else_add_path = os.path.join(add_path, else_file)
                        # check else node(데이터 읽는 속도 오래걸림)
                        for else_path, dirs, files in os.walk(else_add_path):
                            else_file = nuke.getFileNameList(else_path)
                            if len(else_file) > 0 and "#" in else_file[0]:
                                get_xpos = set_read_node(else_path, else_file[0], else_xpos, else_ypos, check=False)
                                else_xpos = get_xpos + 100 

    # backdrop_size
    x_list = [x_pos, main_xpos, denoise_xpos, extra_xpos, shadow_xpos, else_xpos]
    x_list.sort()
 
    if color != None:
        # create backdrop
        backdrop = nukescripts.autoBackdrop()
        backdrop.setXYpos(x_pos - 20 , y_pos - 100)
        path_name = path.split('/')
        backdrop.knob('label').setValue(path_name[-1])
        backdrop.knob('note_font_size').setValue(50)
        backdrop.knob('bdwidth').setValue(x_list[-1] - x_list[0] + 50)
        backdrop.knob('bdheight').setValue(else_ypos - y_pos + 250)
        backdrop.knob('tile_color').setValue(color)
        #backdrop['selected'].setValue(True)  
        
    nukescripts.clear_selection_recursive()   
    return else_ypos


def set_read_node(path, folder, xpos, ypos, check=True):
    if check == True: 
        add_path = os.path.join(path, folder)
        file_name = nuke.getFileNameList(add_path)[0]
        
    elif check == False: 
        add_path = path
        file_name = folder
        
    read_node = nuke.createNode('Read')
    read_node.knob('file').fromUserText(add_path + '/' +file_name)
    read_node.setXYpos(xpos, ypos)
    return xpos


def get_position():
    selection = nuke.selectedNodes()
    if selection == []:
        n = nuke.createNode("NoOp")
        xPos = n.xpos()
        yPos = n.ypos()
        nuke.delete(n)
       
    else:
        xPos = selection[0].xpos() + 200
        yPos = selection[0].ypos() + 100
    return xPos, yPos
    
    
def create_deep(path, folder, xpos, ypos):
    DeepRead = nuke.createNode("DeepRead")
    DeepRead.knob('file').fromUserText(path + '/' +folder)
    DeepRead['xpos'].setValue(xpos)
    DeepRead['ypos'].setValue(ypos)

    Dexp = DeepRead = nuke.createNode("DeepExpression")
    Dexp['xpos'].setValue(xpos)
    Dexp['ypos'].setValue(ypos+25)
    Dexp.setName("DeepExpID")

    Dexp.setInput(0,DeepRead)
    nuke.Layer("other",["id"])

    Dexp.knob('temp_name0').setVisible(False)
    Dexp.knob('temp_expr0').setVisible(False)
    Dexp.knob('temp_name1').setVisible(False)
    Dexp.knob('temp_expr1').setVisible(False)
    Dexp.knob('temp_name2').setVisible(False)
    Dexp.knob('temp_expr2').setVisible(False)
    Dexp.knob('temp_name3').setVisible(False)
    Dexp.knob('temp_expr3').setVisible(False)

    Dexp.knob('chans0').setValue("other.id")

    Dexp.knob('chans1').setValue('none')
    Dexp.knob('chans1').setVisible(False)
    Dexp.knob('chans2').setVisible(False)
    Dexp.knob('chans3').setVisible(False)
    Dexp.knob('other.id').setValue("exponent(id)")
    Dexp.knob('other.id').setVisible(False)

    DRC = nuke.nodes.DeepRecolor()
    DRC['xpos'].setValue(xpos)
    DRC['ypos'].setValue(ypos+50)
    DRC.setInput(0,Dexp)

    constant = nuke.nodes.Constant()
    constant['xpos'].setValue(DRC.xpos()+100)
    constant['ypos'].setValue(DRC.ypos()-23)

    DRC.setInput(1,constant)

    DP = nuke.nodes.DeepID()
    DP['xpos'].setValue(xpos)
    DP['ypos'].setValue(ypos+100)

    DP.setInput(0,DRC)
    return constant.xpos()

# 아래로 모든 노드 선택
def nodes_setup(node, dot, name, path, x_pos, y_pos):
    # get pulldown_nodes
    pulldown_nodes = get_pulldown_nodes(dot)

    #render
    render_backdrop = nuke.createNode('BackdropNode')
    render_backdrop.setXYpos(x_pos - 2050  , y_pos + 200)
    render_backdrop['label'].setValue(name)    
    render_backdrop['bdwidth'].setValue(2917)
    render_backdrop['bdheight'].setValue(20)
    render_backdrop['note_font'].setValue('DejaVu Sans Bold')
    render_backdrop['note_font_size'].setValue(150)
    lpe_read = create_read_node(path, 'LPE', x_pos-1650 , y_pos+500)
    lpe_dot = nuke.createNode('Dot')
    primary_read = create_read_node(path, 'primary', lpe_read.xpos()-200, lpe_read.ypos())  
    ml_read = create_read_node(path, 'ML', primary_read.xpos()-200 , primary_read.ypos())    
    ml_dot = nuke.createNode('Dot')
    # 기즈모 등록전
    ml_node = nuke.createNode('ml')    
    ml_node.setXYpos(primary_read.xpos() , primary_read.ypos() +500)
    button1 = ml_node.knob('hide_load')    
    nuke.Script_Knob.execute(button1)  
    lpe_dot.setXYpos(ml_node.xpos() + 234  , ml_node.ypos() + 4)
    ml_dot.setXYpos(ml_node.xpos() - 166  , ml_node.ypos() + 4)
    ml_node.setInput(1, primary_read)
    ml_node.setInput(2, lpe_dot)
    unpremult = nuke.createNode('Unpremult')
    unpremult.setXYpos(ml_node.xpos() , ml_node.ypos() + 150)
    premult = nuke.createNode('Premult')
    premult.setXYpos(unpremult.xpos() , unpremult.ypos() + 700)
    dot_1 = nuke.createNode('Dot')
    dot_1.setXYpos(premult.xpos() + 34  , premult.ypos() + 250)
    new_xpos = dot_1.xpos() + 1600
    new_ypos = dot_1.ypos()
    new_input = dot_1
    # undistort_nodes
    align_node_list = if_undistort_nodes(new_input, new_xpos, new_ypos)

    merge = nuke.createNode('Merge2')
    merge.setXYpos(x_pos  , dot_1.ypos())
    merge.setInput(0, node)
    if align_node_list == []:
        merge.setInput(1, dot_1)
    dot.setInput(0, merge)

    # 정렬
    align_node_list.extend([[dot_1, 12],  [merge, 20]])
    for anl in align_node_list:
        node_size =  (anl[1] - 20 ) / -2
        anl[0].setYpos(merge.ypos() + node_size)           
    
    if merge.ypos() > dot.ypos():
        dot_ypos = dot.ypos()
        for pn in pulldown_nodes:
            pn_ypos = pn.ypos() - dot_ypos
            pn.setYpos(merge.ypos() + pn_ypos + 100)
    nukescripts.clear_selection_recursive()     
    return merge


# 선택한 템플릿에서 시작 노드, 닷 노드 가져오기
def find_standard_node(node):
    for i in downstream(node):
        if 'end_lgt_dot_' in i.name():
            deps = i.dependencies()
            nukescripts.clear_selection_recursive()
            return deps[0], i
    
    
# 리드파일이 있으면 만들고 없으면 constant노드
def create_read_node(path, folder, x_pos, y_pos):
    # 필터에 노드가 있을때
    if os.path.isdir(os.path.join(path, 'Filtered')):
        for f in os.listdir(os.path.join(path, 'Filtered')):
            if folder in f:
                add_path = os.path.join(path, 'Filtered', f)
                file_name = nuke.getFileNameList(add_path)[0]

                node = nuke.createNode('Read')
                node.knob('file').fromUserText(add_path + '/' +file_name)
                node.setXYpos(x_pos, y_pos)    
                return node
                
    # 디노이즈에 노드에 있을때    
    if os.path.isdir(os.path.join(path, 'Denoise')):
        for d in os.listdir(os.path.join(path, 'Denoise')):
            if folder in d:
                add_path = os.path.join(path, 'Denoise', d)
                file_name = nuke.getFileNameList(add_path)[0]

                node = nuke.createNode('Read')
                node.knob('file').fromUserText(add_path + '/' +file_name)
                node.setXYpos(x_pos, y_pos)    
                return node
    #나머지
    if os.path.isdir(os.path.join(path, folder)):
        try:
            add_path = os.path.join(path, folder)
            file_name = nuke.getFileNameList(add_path)[0]

            node = nuke.createNode('Read')
            node.knob('file').fromUserText(add_path + '/' +file_name)
            node.setXYpos(x_pos, y_pos)      
        except:
            node = nuke.createNode('Constant')
            node.setXYpos(x_pos, y_pos)

    else:
        node = nuke.createNode('Constant')
        node.setXYpos(x_pos, y_pos)
    return node   
            

def downstream(node):
    if not node.dependent():
        return

    deps = node.dependent()
    for dep in deps:
        dep.setSelected(True)
        
        if 'Viewer' in dep.Class():
            dep.setSelected(False)
        if not dep.dependent():
            continue
        downstream(node=dep)
    slected_nodes = nuke.selectedNodes()

    return slected_nodes


# 위로 모든 노드 선택
def upstream(node):
    if not node.dependencies():
        return
    deps = node.dependencies()
    for dep in deps:
        dep.setSelected(True)

        if 'end_lgt_dot_' in dep.name():
            continue
        if not dep.dependencies():
            continue
        upstream(node=dep)
    slected_nodes = nuke.selectedNodes()
    return slected_nodes                      


# 디스토션 노드 있으면 가져오기
def find_undistort_nodes():
    nodes = nuke.allNodes('Read')

    set_list = []
    for node in nodes:
        if 'UNDISTORT' in os.path.basename(node['file'].value()).upper():
            nukescripts.clear_selection_recursive()
            undistort_list =  downstream(node)

            if undistort_list:
                undistort_list.reverse()
            nukescripts.clear_selection_recursive()


            if undistort_list == None:
                set_list.append(None)
            else:
                node_grp = []
                for ul_node in undistort_list:
                    if 'Viewer' != ul_node.Class() and 'Read' != ul_node.Class():
                        node_grp.append([ul_node, ul_node.screenHeight()])
                set_list.append(node_grp)

    for s in set_list:
        if s != None:
            return  s
    return None       
    

def if_undistort_nodes(new_input, new_xpos, new_ypos):
    fn_nodes = find_undistort_nodes()
    align_node_list = []    
    if fn_nodes != None:    
        for fun in fn_nodes:
            find_node = fun[0]
            node_height = fun[1]

            newNode = nuke.createNode(find_node.Class(), find_node.writeKnobs(nuke.WRITE_NON_DEFAULT_ONLY | nuke.TO_SCRIPT), inpanel=False)
            newNode.setXYpos(new_xpos, new_ypos)
            newNode.setInput(0, new_input)
            new_xpos += 100
            new_input = newNode
            align_node_list.append([newNode, node_height])

    return align_node_list
    
    
def get_pulldown_nodes(dot):
    nukescripts.clear_selection_recursive()     
    pulldown_nodes = upstream(downstream(dot)[0])
    dot_num = dot.name().split('_')[-1]

    bx, by, bw, bz = None, None, None, None
    backdrop_nodes = nuke.allNodes('BackdropNode')
    for bn in backdrop_nodes:
        if int(bn['z_order'].getValue()) == int(dot_num):
            pulldown_nodes.append(bn)
            if 'FG_plate' in bn['label'].getValue() :
                bx, by = bn.xpos(), bn.ypos()
            elif 'write' in bn['label'].getValue() :              
                bw, bz = bn.xpos() + 2900, bn.ypos() + 1000
    
    all_node = nuke.allNodes()
    for i in all_node:
        if by <= i.ypos() <= bz and bx <= i.xpos() <= bw:              
            if i not in pulldown_nodes:
                pulldown_nodes.append(i)

    return pulldown_nodes
   

#
def get_gizmo(path):
    gizmo_line = 'Gizmo {\n'
    group_line = 'Group {\n'
    basename = os.path.basename(path)
    if basename=='.gizmo':
        name = 'untitled'
    else:
        name = os.path.splitext(basename)[0].replace(' ','_')

    #read gizmo file
    file = open(path)
    lines = []
    for line in file:
        lines.append(line)
    file.close()
    #change gizmo to group, and add name
    if lines.count(gizmo_line)==1:
        i = lines.index(gizmo_line)
        lines.pop(i)
        lines.insert(i,group_line)
        if name[-1].isdigit():
	        lines.insert(i+1,'name '+name+'_1\n')
        else:
	        lines.insert(i+1,'name '+name+'1\n')

    #load group
    groupText = ''
    for line in lines:
        groupText+=line
    nuke.scriptReadText(groupText)
    nukescripts.clear_selection_recursive()
		  
		  
		  
		  
############################################################# 밑에 안 쓰는중
        
def run_py(path, color, x_pos, y_pos):
    nukescripts.clear_selection_recursive()

    name, ext =  os.path.splitext(os.path.basename(path))
    run = eval(name + '.run()')
    run
    
    if color != None:    
        select_node = nuke.selectedNodes()
        for i in select_node:
            i.setSelected(True)
          
        backdrop = nukescripts.autoBackdrop()
        backdrop['tile_color'].setValue(color) 
    
    return 



##############################################################
def get_ocio_color():
    root_node = nuke.root()
    color_num =  root_node.knob('workingSpaceLUT').getValue()
    color_name = root_node.knob('workingSpaceLUT').enumName(int(color_num))


    if 'aces' in color_name.lower():
        return 'ACES'
    elif 'linear' in color_name.lower():
        return 'Alexa'
    else:
        return 'None'
        

def run_read(path, color, x_pos, y_pos):
    nukescripts.clear_selection_recursive()

    file_name = nuke.getFileNameList(path)[0]
    node = nuke.createNode('Read')
    node.knob('file').fromUserText(path + '/' + file_name)
    
    ocio = get_ocio_color()
    if ocio == 'ACES' and str(node.knob('file').getValue()).endswith('.exr'):
        node['colorspace'].setValue('ACES - ACES2065-1')
      
    elif ocio == 'Alexa' and str(node.knob('file').getValue()).endswith('.dpx'):
        node['colorspace'].setValue('AlexaV3LogC')    
    else:
        pass   
     
    if color != None:      
        backdrop = nukescripts.autoBackdrop()
        backdrop['tile_color'].setValue(color) 
    nukescripts.clear_selection_recursive()            
    return node

##############################################################
def run_video(path, color, x_pos, y_pos):
    nukescripts.clear_selection_recursive()

    node = nuke.createNode('Read')
    node.knob('file').fromUserText(path)
    
    if color != None:      
        backdrop = nukescripts.autoBackdrop()
        backdrop['tile_color'].setValue(color) 
    nukescripts.clear_selection_recursive()    
    return node
            

   
# 
def get_nk(path):
    nukescripts.clear_selection_recursive()

    f = open(path, "r")
    data = f.read()
    QtWidgets.QApplication.clipboard().setText(data)
    paste = nuke.nodePaste("%clipboard%")
    
    nukescripts.clear_selection_recursive()
    return
    
                
