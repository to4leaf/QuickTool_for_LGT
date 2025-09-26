# -*- coding: utf-8 -*-
'''
__ author __ = lighting_joonsoo

'''
from PySide2 import QtWidgets, QtGui, QtCore
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui(QWidget):
    def __init__(self, mainUI, toolName):
        super(Ui, self).__init__() 
        
        # init setting.
        self.WindowSize = [750, 1000]
        self.WindowTitle = 'QuickTool_forLGT'
        self.setGeometry(1700, 200, 0 ,0)
        self.setObjectName(toolName)
        self.setAcceptDrops(True)   
        

        if mainUI :
	        mainUI.setWindowPosition(self, mainUI)
        else:
	        main_layout = self.init_ui()
	        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
	        self.setWindowTitle(" %s "%self.WindowTitle)
	        self.setMinimumSize(*self.WindowSize)
	        self.setLayout(main_layout)


    def init_ui(self):
        # Create the main layout
        layout = QVBoxLayout()
        tab_main = QTabWidget()  
        layout.addWidget(tab_main)
        # start tab   
        tab_template_widget = QWidget()
        tab_template_layout = QVBoxLayout(tab_template_widget) 
        
        # start group1
        self.step01_group_box = QGroupBox(tab_template_widget)  
        self.step01_group_box.setTitle('Step01')       
        step01_layout_mian = QVBoxLayout(self.step01_group_box)
        # start group1 layout1           
        step01_btn_layout = QHBoxLayout()
        self.all_btn = double_Button(self.step01_group_box)
        self.all_btn.setText('All')         
        step01_btn_layout.addWidget(self.all_btn)
        btn_layout_spacer = QSpacerItem(200, 20, QSizePolicy.Preferred, QSizePolicy.Minimum)
        step01_btn_layout.addItem(btn_layout_spacer)      
        self.getPlate_btn = double_Button(self.step01_group_box)
        self.getPlate_btn.setText('get plate')                   
        step01_btn_layout.addWidget(self.getPlate_btn)
        self.getMM_btn = double_Button(self.step01_group_box)
        self.getMM_btn.setText('get mm')                 
        step01_btn_layout.addWidget(self.getMM_btn)        
        self.setTemplate_btn = double_Button(self.step01_group_box)
        self.setTemplate_btn.setText('set template')                
        step01_btn_layout.addWidget(self.setTemplate_btn)
        step01_layout_mian.addLayout(step01_btn_layout)        
        # start group1 layout2
        step01_text_layout = QHBoxLayout()        
        textEdit = QTextEdit(self.step01_group_box)
        textEdit.setText('All :\n'
        'get mm :\n'
        'get plate :\n'
        'set template :\n')        
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(textEdit.sizePolicy().hasHeightForWidth())
        textEdit.setSizePolicy(sizePolicy)        
        textEdit.setMaximumSize(QSize(16777215, 80))        
        textEdit.setStyleSheet(u"background: transparent\n""")
        textEdit.setEnabled(False)        
        step01_text_layout.addWidget(textEdit)
        step01_layout_mian.addLayout(step01_text_layout)        
        tab_template_layout.addWidget(self.step01_group_box)  
        
        # start group2
        self.step02_group_box = QGroupBox(tab_template_widget)  
        self.step02_group_box.setTitle('Step02')  
        step02_layout_mian = QVBoxLayout(self.step02_group_box)  
        # step02 layout sub treeview 
        step02_layout_sub = QVBoxLayout() ## 
        items_label = QLabel(tab_template_widget)      
        items_label.setText('Items')           
        step02_layout_sub.addWidget(items_label)  
        # start group2 layout1   
        step02_btn_layout = QHBoxLayout() ##
        self.palette_btn = double_Button(tab_template_widget)
        self.palette_btn.setText('Palette')
        self.palette_btn.setObjectName('Palette')             
        step02_btn_layout.addWidget(self.palette_btn)   
        self.macro_btn = double_Button(tab_template_widget)  
        self.macro_btn.setText('Macro')
        self.macro_btn.setObjectName('Macro')         
        step02_btn_layout.addWidget(self.macro_btn)        
        self.gizmo_btn = double_Button(tab_template_widget) 
        self.gizmo_btn.setText('Gizmo')
        self.gizmo_btn.setObjectName('Gizmo')  
        step02_btn_layout.addWidget(self.gizmo_btn)  
        self.wip_btn = double_Button(tab_template_widget)  
        self.wip_btn.setText('wip')
        self.wip_btn.setObjectName('wip')  
        
        #
        step02_btn_layout.addWidget(self.wip_btn)                
        step02_layout_sub.addLayout(step02_btn_layout) 
        step02_btn_layout2 = QHBoxLayout() 
        self.lgt_btn = double_Button(tab_template_widget)  
        self.lgt_btn.setText('lgt')
        self.lgt_btn.setObjectName('lgt')  
        step02_btn_layout2.addWidget(self.lgt_btn)       
        self.comp_btn = double_Button(tab_template_widget)  
        self.comp_btn.setText('comp')
        self.comp_btn.setObjectName('comp')       
        step02_btn_layout2.addWidget(self.comp_btn)  
        self.mm_btn = double_Button(tab_template_widget) 
        self.mm_btn.setText('mm')
        self.mm_btn.setObjectName('mm')   
        step02_btn_layout2.addWidget(self.mm_btn)         
        self.plate_btn = double_Button(tab_template_widget)  
        self.plate_btn.setText('plate')
        self.plate_btn.setObjectName('plate')       
        step02_btn_layout2.addWidget(self.plate_btn)          
        step02_layout_sub.addLayout(step02_btn_layout2) 
        
        #    
        step02_path_layout = QHBoxLayout() 
        self.path_lineedit = QLineEdit(tab_template_widget)                                
        step02_path_layout.addWidget(self.path_lineedit)
        self.path_btn = QPushButton(tab_template_widget)
        self.path_btn.setText('▼')        
        self.path_btn.setMaximumSize(QSize(35, 16777215))
        self.path_btn.setIconSize(QSize(20, 20))
        step02_path_layout.addWidget(self.path_btn)
        step02_layout_sub.addLayout(step02_path_layout) ##    
        self.items_treeview = MYtreeview(tab_template_widget)  
        step02_layout_sub.addWidget(self.items_treeview)
        step02_layout_mian.addLayout(step02_layout_sub) 
        
        # start group2 layout4 
        step02_backdrop_layout = QHBoxLayout() 
        extra_backdrop_spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        step02_backdrop_layout.addItem(extra_backdrop_spacer2)        
        self.backdrop_check_btn = QCheckBox(tab_template_widget)
        self.backdrop_check_btn.setText('Backdrop') 
        self.backdrop_check_btn.setChecked(True)
        step02_backdrop_layout.addWidget(self.backdrop_check_btn)
        extra_backdrop_spacer = QSpacerItem(20, 20, QSizePolicy.Fixed, QSizePolicy.Minimum)
        step02_backdrop_layout.addItem(extra_backdrop_spacer)        
        self.backdrop_get_color = QPushButton(tab_template_widget)
        self.backdrop_get_color.setText(' ')         
        self.backdrop_get_color.setMaximumSize(QSize(20, 20))  
        self.backdrop_get_color.setStyleSheet('background-color:rgb(125,125,125)')
        step02_backdrop_layout.addWidget(self.backdrop_get_color)             
        self.backdrop_radio1 = QRadioButton(tab_template_widget)
        self.backdrop_radio1.setText('Self')      
        step02_backdrop_layout.addWidget(self.backdrop_radio1)
        self.backdrop_radio2 = QRadioButton(tab_template_widget)
        self.backdrop_radio2.setText('Random')      
        step02_backdrop_layout.addWidget(self.backdrop_radio2)
        self.backdrop_radio3 = QRadioButton(tab_template_widget)
        self.backdrop_radio3.setText('Gray')      
        self.backdrop_radio3.setChecked(True)        
        step02_backdrop_layout.addWidget(self.backdrop_radio3)              
        step02_layout_mian.addLayout(step02_backdrop_layout)    
                
        # start group2 layout5
        step02_extra_layout = QHBoxLayout() ##
        extra_layout_spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        step02_extra_layout.addItem(extra_layout_spacer)        
        self.share_macro_btn = double_Button(tab_template_widget)
        self.share_macro_btn.setText('Macro Share')         
        step02_extra_layout.addWidget(self.share_macro_btn)
        step02_layout_mian.addLayout(step02_extra_layout) ##            
        tab_template_layout.addWidget(self.step02_group_box)  

        # end tab   
        tab_null = QWidget()      
        # add tab 
        tab_main.addTab(tab_template_widget, "")
        tab_main.addTab(tab_null, "")      
        tab_main.setTabText(tab_main.indexOf(tab_template_widget), 'template')      
        tab_main.setTabText(tab_main.indexOf(tab_null), 'Null')     
        # Set the layout for the panel
        self.setLayout(layout)
    
    #
    def keyPressEvent(self, event):
        #if event.modifiers() & Qt.ControlModifier:
         #   if event.modifiers() & Qt.AltModifier:
        if event.key() == Qt.Key_F5:
            self.setVisible(False)
            self.items_treeview.clearSelection()




#### QPushButton 더블클릭 이슈로 재맵핑 ####
class double_Button(QtWidgets.QPushButton):
    right_clicked = QtCore.Signal()
    left_clicked = QtCore.Signal()
    double_clicked = QtCore.Signal()


    def __init__(self, *args, **kwargs):
        super(double_Button, self).__init__(*args, **kwargs)
        self.setMinimumSize(16777215,30)    

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.timer.setInterval(250)
        self.timer.timeout.connect(self.timeout)
        
        self.is_double = False
        self.is_left_click = True

        self.installEventFilter(self)

        self.double_clicked.connect(self.double_click_event)
        self.left_clicked.connect(self.left_click_event)
        self.right_clicked.connect(self.right_click_event)


    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.setStyleSheet("QPushButton { background-color: rgb(40,40,40) }")         

            if not self.timer.isActive():
                self.timer.start()

            self.is_left_click = False
            
            if event.button() == QtCore.Qt.LeftButton:
                self.is_left_click = True                
    
            return True
            
        elif event.type() == QtCore.QEvent.MouseButtonRelease:
            self.setStyleSheet("QPushButton { background-color: 0 }")     
        
        elif event.type() == QtCore.QEvent.MouseButtonDblClick:
            self.setStyleSheet("QPushButton { background-color: rgb(40,40,40) }")            

            self.is_double = True
            return True
            
        return False


    def timeout(self):    
        if self.is_double:
            self.double_clicked.emit()
        else:
            if self.is_left_click:
                self.left_clicked.emit()
            else:
                self.right_clicked.emit()

        self.is_double = False


    def left_click_event(self):
        print('left clicked')


    def right_click_event(self):
        print('right clicked')


    def double_click_event(self):
        print('double clicked')     
                

####
class MYtreeview(QtWidgets.QTreeView):
    clicked = QtCore.Signal()

    def __init__(self, *args, **kwargs):
        super(MYtreeview, self).__init__(*args, **kwargs)        
        
        self.setMinimumHeight(200)  
        self.setDragEnabled(True)
        self.setDragDropMode(QtWidgets.QAbstractItemView.InternalMove)                
        self.setAcceptDrops(True)                   
        self.viewport().installEventFilter(self)       
        self.setContextMenuPolicy(QtCore.Qt.ActionsContextMenu)     
        self.setSelectionMode(QAbstractItemView.ExtendedSelection)   
        self.clicked.connect(self.click_event)        
        
                 
    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:                      
            if event.button() == QtCore.Qt.RightButton:                             
                self.clicked.emit()
                return True

        return False

    def click_event(self):
        print('clicked')
        
        
#### macro sub menu ####
class SubWindow(QDialog):
    def __init__(self):
        super(SubWindow, self).__init__()
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('Macro Share')
        self.setMinimumWidth(330)
        self.setMinimumHeight(130)        

        main_layout = QVBoxLayout(self)
        line_layout = QHBoxLayout()
        line_layout.setObjectName("horizontalLayout")
        name_label = QLabel(self)
        name_label.setText('Name')
        line_layout.addWidget(name_label)
        self.name_lineEdit = QLineEdit(self)
        line_layout.addWidget(self.name_lineEdit)
        main_layout.addLayout(line_layout)
        button_layout = QHBoxLayout()
        button_layout.setObjectName(u"horizontalLayout_2")
        horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        button_layout.addItem(horizontalSpacer)
        self.OK_Button = QPushButton(self)
        self.OK_Button.setText('OK')
        button_layout.addWidget(self.OK_Button)
        self.cancel_botton = QPushButton(self)
        self.cancel_botton.setText('Cancel')
        button_layout.addWidget(self.cancel_botton)
        main_layout.addLayout(button_layout)

        self.OK_Button.clicked.connect(self.onOKButtonClicked)
        self.cancel_botton.clicked.connect(self.onCancelButtonClicked)
        
    def onOKButtonClicked(self):
        self.accept()
        
    def onCancelButtonClicked(self):
        self.reject()
        
    def showModal(self):
        return super(SubWindow, self).exec_(), self.name_lineEdit.text()      
        
        
        
        

