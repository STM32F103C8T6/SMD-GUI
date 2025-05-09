# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SMD_GUI.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QFrame,
    QGridLayout, QGroupBox, QHBoxLayout, QHeaderView,
    QLabel, QLayout, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QMenu, QMenuBar,
    QProgressBar, QPushButton, QScrollArea, QSizePolicy,
    QTabWidget, QTextBrowser, QToolBox, QToolButton,
    QTreeView, QTreeWidget, QTreeWidgetItem, QVBoxLayout,
    QWidget)

class Ui_GMX_GUI(object):
    def setupUi(self, GMX_GUI):
        if not GMX_GUI.objectName():
            GMX_GUI.setObjectName(u"GMX_GUI")
        GMX_GUI.resize(1800, 1012)
        GMX_GUI.setAutoFillBackground(True)
        self.actionChange_working_path = QAction(GMX_GUI)
        self.actionChange_working_path.setObjectName(u"actionChange_working_path")
        self.actionDefault_Settings = QAction(GMX_GUI)
        self.actionDefault_Settings.setObjectName(u"actionDefault_Settings")
        self.Main_window = QWidget(GMX_GUI)
        self.Main_window.setObjectName(u"Main_window")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Main_window.sizePolicy().hasHeightForWidth())
        self.Main_window.setSizePolicy(sizePolicy)
        self.verticalLayout_3 = QVBoxLayout(self.Main_window)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout_47 = QHBoxLayout()
        self.horizontalLayout_47.setObjectName(u"horizontalLayout_47")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.path_display = QLabel(self.Main_window)
        self.path_display.setObjectName(u"path_display")

        self.verticalLayout.addWidget(self.path_display)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.Filter_line = QLineEdit(self.Main_window)
        self.Filter_line.setObjectName(u"Filter_line")

        self.horizontalLayout_3.addWidget(self.Filter_line)

        self.Clear_filters_button = QPushButton(self.Main_window)
        self.Clear_filters_button.setObjectName(u"Clear_filters_button")

        self.horizontalLayout_3.addWidget(self.Clear_filters_button)


        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.folder_tree_view = QTreeView(self.Main_window)
        self.folder_tree_view.setObjectName(u"folder_tree_view")

        self.verticalLayout.addWidget(self.folder_tree_view)

        self.select_numb_count = QLabel(self.Main_window)
        self.select_numb_count.setObjectName(u"select_numb_count")

        self.verticalLayout.addWidget(self.select_numb_count)


        self.horizontalLayout_47.addLayout(self.verticalLayout)

        self.Seting_Tab = QTabWidget(self.Main_window)
        self.Seting_Tab.setObjectName(u"Seting_Tab")
        self.Seting_Tab.setAutoFillBackground(True)
        self.Run_Step_Interface = QWidget()
        self.Run_Step_Interface.setObjectName(u"Run_Step_Interface")
        self.horizontalLayout_36 = QHBoxLayout(self.Run_Step_Interface)
        self.horizontalLayout_36.setObjectName(u"horizontalLayout_36")
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.Config_Tree = QTreeWidget(self.Run_Step_Interface)
        self.Config_Tree.setObjectName(u"Config_Tree")
        self.Config_Tree.setAutoScroll(True)
        self.Config_Tree.setColumnCount(0)

        self.verticalLayout_6.addWidget(self.Config_Tree)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label = QLabel(self.Run_Step_Interface)
        self.label.setObjectName(u"label")

        self.horizontalLayout_4.addWidget(self.label)

        self.task_folder_select = QComboBox(self.Run_Step_Interface)
        self.task_folder_select.setObjectName(u"task_folder_select")

        self.horizontalLayout_4.addWidget(self.task_folder_select)

        self.Execute_toolButton = QToolButton(self.Run_Step_Interface)
        self.Execute_toolButton.setObjectName(u"Execute_toolButton")

        self.horizontalLayout_4.addWidget(self.Execute_toolButton)

        self.horizontalLayout_4.setStretch(1, 1)

        self.verticalLayout_6.addLayout(self.horizontalLayout_4)

        self.Run_Step_Task = QPushButton(self.Run_Step_Interface)
        self.Run_Step_Task.setObjectName(u"Run_Step_Task")

        self.verticalLayout_6.addWidget(self.Run_Step_Task)


        self.horizontalLayout_36.addLayout(self.verticalLayout_6)

        self.line = QFrame(self.Run_Step_Interface)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_36.addWidget(self.line)

        self.scrollArea = QScrollArea(self.Run_Step_Interface)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setAutoFillBackground(True)
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 720, 874))
        self.scrollAreaWidgetContents.setAutoFillBackground(True)
        self.verticalLayout_7 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.Config_list = QToolBox(self.scrollAreaWidgetContents)
        self.Config_list.setObjectName(u"Config_list")
        self.Config_list.setAutoFillBackground(True)
        self.Config_Move_File = QWidget()
        self.Config_Move_File.setObjectName(u"Config_Move_File")
        self.Config_Move_File.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_8 = QVBoxLayout(self.Config_Move_File)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.Auto_Move_File = QGroupBox(self.Config_Move_File)
        self.Auto_Move_File.setObjectName(u"Auto_Move_File")
        self.Auto_Move_File.setEnabled(True)
        self.Auto_Move_File.setAutoFillBackground(True)
        self.Auto_Move_File.setCheckable(True)
        self.Auto_Move_File.setChecked(True)
        self.verticalLayout_9 = QVBoxLayout(self.Auto_Move_File)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.Ligand_endswith_label = QLabel(self.Auto_Move_File)
        self.Ligand_endswith_label.setObjectName(u"Ligand_endswith_label")

        self.horizontalLayout_5.addWidget(self.Ligand_endswith_label)

        self.Ligand_endswith = QLineEdit(self.Auto_Move_File)
        self.Ligand_endswith.setObjectName(u"Ligand_endswith")
        self.Ligand_endswith.setEnabled(True)
        self.Ligand_endswith.setDragEnabled(True)

        self.horizontalLayout_5.addWidget(self.Ligand_endswith)


        self.verticalLayout_9.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(5, 5, 5, 5)
        self.protein_endswith_label = QLabel(self.Auto_Move_File)
        self.protein_endswith_label.setObjectName(u"protein_endswith_label")

        self.horizontalLayout_6.addWidget(self.protein_endswith_label)

        self.protein_endswith = QLineEdit(self.Auto_Move_File)
        self.protein_endswith.setObjectName(u"protein_endswith")
        self.protein_endswith.setEnabled(True)
        self.protein_endswith.setDragEnabled(True)
        self.protein_endswith.setReadOnly(False)
        self.protein_endswith.setClearButtonEnabled(False)

        self.horizontalLayout_6.addWidget(self.protein_endswith)


        self.verticalLayout_9.addLayout(self.horizontalLayout_6)

        self.horizontalLayout_38 = QHBoxLayout()
        self.horizontalLayout_38.setObjectName(u"horizontalLayout_38")
        self.folder_name_index_label = QLabel(self.Auto_Move_File)
        self.folder_name_index_label.setObjectName(u"folder_name_index_label")

        self.horizontalLayout_38.addWidget(self.folder_name_index_label)

        self.folder_name_index = QLineEdit(self.Auto_Move_File)
        self.folder_name_index.setObjectName(u"folder_name_index")

        self.horizontalLayout_38.addWidget(self.folder_name_index)


        self.verticalLayout_9.addLayout(self.horizontalLayout_38)

        self.Copy_receptor = QGroupBox(self.Auto_Move_File)
        self.Copy_receptor.setObjectName(u"Copy_receptor")
        self.Copy_receptor.setCheckable(True)
        self.Copy_receptor.setChecked(False)
        self.verticalLayout_11 = QVBoxLayout(self.Copy_receptor)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(-1, -1, 1, -1)
        self.receptor_file_path_label = QLabel(self.Copy_receptor)
        self.receptor_file_path_label.setObjectName(u"receptor_file_path_label")

        self.horizontalLayout_7.addWidget(self.receptor_file_path_label)

        self.receptor_file_path = QLineEdit(self.Copy_receptor)
        self.receptor_file_path.setObjectName(u"receptor_file_path")
        self.receptor_file_path.setEnabled(False)
        self.receptor_file_path.setDragEnabled(True)

        self.horizontalLayout_7.addWidget(self.receptor_file_path)


        self.verticalLayout_11.addLayout(self.horizontalLayout_7)


        self.verticalLayout_9.addWidget(self.Copy_receptor)


        self.verticalLayout_8.addWidget(self.Auto_Move_File)

        self.Config_list.addItem(self.Config_Move_File, u"Distribute task files")
        self.Ligand_protein_prep_Seting = QWidget()
        self.Ligand_protein_prep_Seting.setObjectName(u"Ligand_protein_prep_Seting")
        self.Ligand_protein_prep_Seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_13 = QVBoxLayout(self.Ligand_protein_prep_Seting)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_12 = QVBoxLayout()
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.Rename_Ligane = QGroupBox(self.Ligand_protein_prep_Seting)
        self.Rename_Ligane.setObjectName(u"Rename_Ligane")
        self.Rename_Ligane.setCheckable(True)
        self.verticalLayout_14 = QVBoxLayout(self.Rename_Ligane)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.Ligand_Name_label = QLabel(self.Rename_Ligane)
        self.Ligand_Name_label.setObjectName(u"Ligand_Name_label")

        self.horizontalLayout_8.addWidget(self.Ligand_Name_label)

        self.Ligand_Name = QLineEdit(self.Rename_Ligane)
        self.Ligand_Name.setObjectName(u"Ligand_Name")

        self.horizontalLayout_8.addWidget(self.Ligand_Name)


        self.verticalLayout_14.addLayout(self.horizontalLayout_8)


        self.verticalLayout_12.addWidget(self.Rename_Ligane)

        self.Repair_Receptor = QGroupBox(self.Ligand_protein_prep_Seting)
        self.Repair_Receptor.setObjectName(u"Repair_Receptor")
        self.Repair_Receptor.setCheckable(True)
        self.verticalLayout_16 = QVBoxLayout(self.Repair_Receptor)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_15 = QVBoxLayout()
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.Repair_main_chain = QCheckBox(self.Repair_Receptor)
        self.Repair_main_chain.setObjectName(u"Repair_main_chain")

        self.verticalLayout_15.addWidget(self.Repair_main_chain)

        self.Repair_missing_side_chain = QCheckBox(self.Repair_Receptor)
        self.Repair_missing_side_chain.setObjectName(u"Repair_missing_side_chain")
        self.Repair_missing_side_chain.setChecked(True)

        self.verticalLayout_15.addWidget(self.Repair_missing_side_chain)


        self.verticalLayout_16.addLayout(self.verticalLayout_15)


        self.verticalLayout_12.addWidget(self.Repair_Receptor)


        self.verticalLayout_13.addLayout(self.verticalLayout_12)

        self.Config_list.addItem(self.Ligand_protein_prep_Seting, u"Prepare ligand receptor files")
        self.Ligand_top_Seting = QWidget()
        self.Ligand_top_Seting.setObjectName(u"Ligand_top_Seting")
        self.Ligand_top_Seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_17 = QVBoxLayout(self.Ligand_top_Seting)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.Gen_ligand_top = QGroupBox(self.Ligand_top_Seting)
        self.Gen_ligand_top.setObjectName(u"Gen_ligand_top")
        self.Gen_ligand_top.setCheckable(True)
        self.Gen_ligand_top.setChecked(True)
        self.verticalLayout_18 = QVBoxLayout(self.Gen_ligand_top)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.Generate_top_by_GAFF = QGroupBox(self.Gen_ligand_top)
        self.Generate_top_by_GAFF.setObjectName(u"Generate_top_by_GAFF")
        self.Generate_top_by_GAFF.setCheckable(True)
        self.gridLayout = QGridLayout(self.Generate_top_by_GAFF)
        self.gridLayout.setObjectName(u"gridLayout")
        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.Sob_top_PATH_label = QLabel(self.Generate_top_by_GAFF)
        self.Sob_top_PATH_label.setObjectName(u"Sob_top_PATH_label")

        self.horizontalLayout_10.addWidget(self.Sob_top_PATH_label)

        self.Sob_top_PATH = QLineEdit(self.Generate_top_by_GAFF)
        self.Sob_top_PATH.setObjectName(u"Sob_top_PATH")

        self.horizontalLayout_10.addWidget(self.Sob_top_PATH)


        self.gridLayout.addLayout(self.horizontalLayout_10, 0, 0, 1, 1)

        self.horizontalLayout_15 = QHBoxLayout()
        self.horizontalLayout_15.setObjectName(u"horizontalLayout_15")
        self.IF_rename_ligand = QCheckBox(self.Generate_top_by_GAFF)
        self.IF_rename_ligand.setObjectName(u"IF_rename_ligand")
        self.IF_rename_ligand.setChecked(True)

        self.horizontalLayout_15.addWidget(self.IF_rename_ligand)

        self.Rename_ligand_name = QLineEdit(self.Generate_top_by_GAFF)
        self.Rename_ligand_name.setObjectName(u"Rename_ligand_name")

        self.horizontalLayout_15.addWidget(self.Rename_ligand_name)


        self.gridLayout.addLayout(self.horizontalLayout_15, 1, 0, 1, 1)


        self.verticalLayout_18.addWidget(self.Generate_top_by_GAFF)

        self.Generate_top_by_CGENFF = QGroupBox(self.Gen_ligand_top)
        self.Generate_top_by_CGENFF.setObjectName(u"Generate_top_by_CGENFF")
        self.Generate_top_by_CGENFF.setCheckable(True)
        self.Generate_top_by_CGENFF.setChecked(False)
        self.verticalLayout_21 = QVBoxLayout(self.Generate_top_by_CGENFF)
        self.verticalLayout_21.setObjectName(u"verticalLayout_21")
        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.CGENFF_web_URL_label = QLabel(self.Generate_top_by_CGENFF)
        self.CGENFF_web_URL_label.setObjectName(u"CGENFF_web_URL_label")

        self.gridLayout_2.addWidget(self.CGENFF_web_URL_label, 0, 0, 1, 4)

        self.CGENFF_web_URL = QLineEdit(self.Generate_top_by_CGENFF)
        self.CGENFF_web_URL.setObjectName(u"CGENFF_web_URL")

        self.gridLayout_2.addWidget(self.CGENFF_web_URL, 0, 4, 1, 1)

        self.CGENFF_user_name_abel = QLabel(self.Generate_top_by_CGENFF)
        self.CGENFF_user_name_abel.setObjectName(u"CGENFF_user_name_abel")

        self.gridLayout_2.addWidget(self.CGENFF_user_name_abel, 1, 0, 1, 2)

        self.CGENFF_pw_label = QLabel(self.Generate_top_by_CGENFF)
        self.CGENFF_pw_label.setObjectName(u"CGENFF_pw_label")

        self.gridLayout_2.addWidget(self.CGENFF_pw_label, 2, 0, 1, 1)

        self.IF_use_Proxy = QCheckBox(self.Generate_top_by_CGENFF)
        self.IF_use_Proxy.setObjectName(u"IF_use_Proxy")

        self.gridLayout_2.addWidget(self.IF_use_Proxy, 3, 0, 1, 3)

        self.CGENFF_user_name = QLineEdit(self.Generate_top_by_CGENFF)
        self.CGENFF_user_name.setObjectName(u"CGENFF_user_name")

        self.gridLayout_2.addWidget(self.CGENFF_user_name, 1, 4, 1, 1)

        self.CGENFF_pw = QLineEdit(self.Generate_top_by_CGENFF)
        self.CGENFF_pw.setObjectName(u"CGENFF_pw")

        self.gridLayout_2.addWidget(self.CGENFF_pw, 2, 4, 1, 1)

        self.Web_Proxy = QLineEdit(self.Generate_top_by_CGENFF)
        self.Web_Proxy.setObjectName(u"Web_Proxy")

        self.gridLayout_2.addWidget(self.Web_Proxy, 3, 4, 1, 1)


        self.verticalLayout_21.addLayout(self.gridLayout_2)


        self.verticalLayout_18.addWidget(self.Generate_top_by_CGENFF)


        self.verticalLayout_17.addWidget(self.Gen_ligand_top)

        self.Config_list.addItem(self.Ligand_top_Seting, u"Generate ligand topology")
        self.Protein_top_Seting = QWidget()
        self.Protein_top_Seting.setObjectName(u"Protein_top_Seting")
        self.Protein_top_Seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_24 = QVBoxLayout(self.Protein_top_Seting)
        self.verticalLayout_24.setObjectName(u"verticalLayout_24")
        self.Gen_Protein_top = QGroupBox(self.Protein_top_Seting)
        self.Gen_Protein_top.setObjectName(u"Gen_Protein_top")
        self.Gen_Protein_top.setCheckable(True)
        self.verticalLayout_22 = QVBoxLayout(self.Gen_Protein_top)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(-1, -1, 200, -1)
        self.horizontalLayout_11 = QHBoxLayout()
        self.horizontalLayout_11.setObjectName(u"horizontalLayout_11")
        self.Force_Field_selt_label = QLabel(self.Gen_Protein_top)
        self.Force_Field_selt_label.setObjectName(u"Force_Field_selt_label")

        self.horizontalLayout_11.addWidget(self.Force_Field_selt_label)

        self.Force_Field_selt = QComboBox(self.Gen_Protein_top)
        self.Force_Field_selt.setObjectName(u"Force_Field_selt")

        self.horizontalLayout_11.addWidget(self.Force_Field_selt)


        self.verticalLayout_22.addLayout(self.horizontalLayout_11)

        self.horizontalLayout_17 = QHBoxLayout()
        self.horizontalLayout_17.setObjectName(u"horizontalLayout_17")
        self.water_model_selt_label = QLabel(self.Gen_Protein_top)
        self.water_model_selt_label.setObjectName(u"water_model_selt_label")

        self.horizontalLayout_17.addWidget(self.water_model_selt_label)

        self.water_model_selt = QComboBox(self.Gen_Protein_top)
        self.water_model_selt.setObjectName(u"water_model_selt")

        self.horizontalLayout_17.addWidget(self.water_model_selt)


        self.verticalLayout_22.addLayout(self.horizontalLayout_17)

        self.horizontalLayout_18 = QHBoxLayout()
        self.horizontalLayout_18.setObjectName(u"horizontalLayout_18")
        self.N_term_selt_label = QLabel(self.Gen_Protein_top)
        self.N_term_selt_label.setObjectName(u"N_term_selt_label")

        self.horizontalLayout_18.addWidget(self.N_term_selt_label)

        self.N_term_selt = QComboBox(self.Gen_Protein_top)
        self.N_term_selt.setObjectName(u"N_term_selt")

        self.horizontalLayout_18.addWidget(self.N_term_selt)


        self.verticalLayout_22.addLayout(self.horizontalLayout_18)

        self.horizontalLayout_19 = QHBoxLayout()
        self.horizontalLayout_19.setObjectName(u"horizontalLayout_19")
        self.C_term_selt_label = QLabel(self.Gen_Protein_top)
        self.C_term_selt_label.setObjectName(u"C_term_selt_label")

        self.horizontalLayout_19.addWidget(self.C_term_selt_label)

        self.C_term_selt = QComboBox(self.Gen_Protein_top)
        self.C_term_selt.setObjectName(u"C_term_selt")

        self.horizontalLayout_19.addWidget(self.C_term_selt)


        self.verticalLayout_22.addLayout(self.horizontalLayout_19)


        self.verticalLayout_24.addWidget(self.Gen_Protein_top)

        self.Morge_complex_gro = QGroupBox(self.Protein_top_Seting)
        self.Morge_complex_gro.setObjectName(u"Morge_complex_gro")
        self.Morge_complex_gro.setCheckable(True)
        self.verticalLayout_23 = QVBoxLayout(self.Morge_complex_gro)
        self.verticalLayout_23.setObjectName(u"verticalLayout_23")
        self.horizontalLayout_20 = QHBoxLayout()
        self.horizontalLayout_20.setObjectName(u"horizontalLayout_20")
        self.horizontalLayout_20.setContentsMargins(-1, -1, 200, -1)
        self.merge_top_file_ff_selt_label = QLabel(self.Morge_complex_gro)
        self.merge_top_file_ff_selt_label.setObjectName(u"merge_top_file_ff_selt_label")

        self.horizontalLayout_20.addWidget(self.merge_top_file_ff_selt_label)

        self.merge_top_file_ff_selt = QComboBox(self.Morge_complex_gro)
        self.merge_top_file_ff_selt.setObjectName(u"merge_top_file_ff_selt")

        self.horizontalLayout_20.addWidget(self.merge_top_file_ff_selt)


        self.verticalLayout_23.addLayout(self.horizontalLayout_20)


        self.verticalLayout_24.addWidget(self.Morge_complex_gro)

        self.Config_list.addItem(self.Protein_top_Seting, u"Generate protein topology")
        self.Solvation_box_seting = QWidget()
        self.Solvation_box_seting.setObjectName(u"Solvation_box_seting")
        self.Solvation_box_seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_26 = QVBoxLayout(self.Solvation_box_seting)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.Gen_Solvation_box = QGroupBox(self.Solvation_box_seting)
        self.Gen_Solvation_box.setObjectName(u"Gen_Solvation_box")
        self.Gen_Solvation_box.setCheckable(True)
        self.gridLayout_4 = QGridLayout(self.Gen_Solvation_box)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, -1, 350, -1)
        self.Box_size_set_label = QLabel(self.Gen_Solvation_box)
        self.Box_size_set_label.setObjectName(u"Box_size_set_label")

        self.gridLayout_4.addWidget(self.Box_size_set_label, 1, 0, 1, 1)

        self.Box_shape_sele = QComboBox(self.Gen_Solvation_box)
        self.Box_shape_sele.setObjectName(u"Box_shape_sele")

        self.gridLayout_4.addWidget(self.Box_shape_sele, 0, 1, 1, 1)

        self.Box_size_set = QLineEdit(self.Gen_Solvation_box)
        self.Box_size_set.setObjectName(u"Box_size_set")

        self.gridLayout_4.addWidget(self.Box_size_set, 1, 1, 1, 1)

        self.Box_shape_sele_label = QLabel(self.Gen_Solvation_box)
        self.Box_shape_sele_label.setObjectName(u"Box_shape_sele_label")

        self.gridLayout_4.addWidget(self.Box_shape_sele_label, 0, 0, 1, 1)


        self.verticalLayout_26.addWidget(self.Gen_Solvation_box)

        self.Add_ions_to_box = QGroupBox(self.Solvation_box_seting)
        self.Add_ions_to_box.setObjectName(u"Add_ions_to_box")
        self.Add_ions_to_box.setCheckable(True)
        self.verticalLayout_27 = QVBoxLayout(self.Add_ions_to_box)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.Neutralize_System = QGroupBox(self.Add_ions_to_box)
        self.Neutralize_System.setObjectName(u"Neutralize_System")
        self.Neutralize_System.setCheckable(False)
        self.verticalLayout_28 = QVBoxLayout(self.Neutralize_System)
        self.verticalLayout_28.setObjectName(u"verticalLayout_28")
        self.horizontalLayout_12 = QHBoxLayout()
        self.horizontalLayout_12.setObjectName(u"horizontalLayout_12")
        self.horizontalLayout_12.setContentsMargins(-1, -1, 150, -1)
        self.label_16 = QLabel(self.Neutralize_System)
        self.label_16.setObjectName(u"label_16")

        self.horizontalLayout_12.addWidget(self.label_16)

        self.add_positive_set = QComboBox(self.Neutralize_System)
        self.add_positive_set.setObjectName(u"add_positive_set")

        self.horizontalLayout_12.addWidget(self.add_positive_set)

        self.add_negative_set = QComboBox(self.Neutralize_System)
        self.add_negative_set.setObjectName(u"add_negative_set")

        self.horizontalLayout_12.addWidget(self.add_negative_set)

        self.label_17 = QLabel(self.Neutralize_System)
        self.label_17.setObjectName(u"label_17")

        self.horizontalLayout_12.addWidget(self.label_17)


        self.verticalLayout_28.addLayout(self.horizontalLayout_12)


        self.verticalLayout_27.addWidget(self.Neutralize_System)

        self.Add_salt_density = QGroupBox(self.Add_ions_to_box)
        self.Add_salt_density.setObjectName(u"Add_salt_density")
        self.Add_salt_density.setCheckable(True)
        self.Add_salt_density.setChecked(False)
        self.verticalLayout_29 = QVBoxLayout(self.Add_salt_density)
        self.verticalLayout_29.setObjectName(u"verticalLayout_29")
        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setObjectName(u"horizontalLayout_13")
        self.horizontalLayout_13.setContentsMargins(-1, -1, 330, -1)
        self.Salt_density_set_label = QLabel(self.Add_salt_density)
        self.Salt_density_set_label.setObjectName(u"Salt_density_set_label")

        self.horizontalLayout_13.addWidget(self.Salt_density_set_label)

        self.Salt_density_set = QLineEdit(self.Add_salt_density)
        self.Salt_density_set.setObjectName(u"Salt_density_set")

        self.horizontalLayout_13.addWidget(self.Salt_density_set)

        self.label_19 = QLabel(self.Add_salt_density)
        self.label_19.setObjectName(u"label_19")

        self.horizontalLayout_13.addWidget(self.label_19)


        self.verticalLayout_29.addLayout(self.horizontalLayout_13)

        self.horizontalLayout_14 = QHBoxLayout()
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(-1, -1, 350, -1)
        self.selt_positive_ion_label = QLabel(self.Add_salt_density)
        self.selt_positive_ion_label.setObjectName(u"selt_positive_ion_label")

        self.horizontalLayout_14.addWidget(self.selt_positive_ion_label)

        self.selt_positive_ion = QComboBox(self.Add_salt_density)
        self.selt_positive_ion.setObjectName(u"selt_positive_ion")

        self.horizontalLayout_14.addWidget(self.selt_positive_ion)

        self.horizontalLayout_14.setStretch(1, 2)

        self.verticalLayout_29.addLayout(self.horizontalLayout_14)

        self.horizontalLayout_16 = QHBoxLayout()
        self.horizontalLayout_16.setObjectName(u"horizontalLayout_16")
        self.horizontalLayout_16.setContentsMargins(-1, -1, 350, -1)
        self.selt_negatibe_ion_label = QLabel(self.Add_salt_density)
        self.selt_negatibe_ion_label.setObjectName(u"selt_negatibe_ion_label")

        self.horizontalLayout_16.addWidget(self.selt_negatibe_ion_label)

        self.selt_negatibe_ion = QComboBox(self.Add_salt_density)
        self.selt_negatibe_ion.setObjectName(u"selt_negatibe_ion")

        self.horizontalLayout_16.addWidget(self.selt_negatibe_ion)

        self.horizontalLayout_16.setStretch(1, 2)

        self.verticalLayout_29.addLayout(self.horizontalLayout_16)


        self.verticalLayout_27.addWidget(self.Add_salt_density)

        self.verticalLayout_27.setStretch(0, 2)
        self.verticalLayout_27.setStretch(1, 3)

        self.verticalLayout_26.addWidget(self.Add_ions_to_box)

        self.Config_list.addItem(self.Solvation_box_seting, u"Generate Solvation Box")
        self.EM_NVT_NPT_seting = QWidget()
        self.EM_NVT_NPT_seting.setObjectName(u"EM_NVT_NPT_seting")
        self.EM_NVT_NPT_seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_30 = QVBoxLayout(self.EM_NVT_NPT_seting)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.Auto_balance = QGroupBox(self.EM_NVT_NPT_seting)
        self.Auto_balance.setObjectName(u"Auto_balance")
        self.Auto_balance.setCheckable(True)
        self.verticalLayout_31 = QVBoxLayout(self.Auto_balance)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.horizontalLayout_21 = QHBoxLayout()
        self.horizontalLayout_21.setObjectName(u"horizontalLayout_21")
        self.horizontalLayout_21.setContentsMargins(-1, -1, 0, -1)
        self.Ligand_name_set_label = QLabel(self.Auto_balance)
        self.Ligand_name_set_label.setObjectName(u"Ligand_name_set_label")

        self.horizontalLayout_21.addWidget(self.Ligand_name_set_label)

        self.Ligand_name_set = QLineEdit(self.Auto_balance)
        self.Ligand_name_set.setObjectName(u"Ligand_name_set")

        self.horizontalLayout_21.addWidget(self.Ligand_name_set)


        self.verticalLayout_31.addLayout(self.horizontalLayout_21)

        self.EM_Seting = QGroupBox(self.Auto_balance)
        self.EM_Seting.setObjectName(u"EM_Seting")
        self.EM_Seting.setCheckable(True)
        self.verticalLayout_32 = QVBoxLayout(self.EM_Seting)
        self.verticalLayout_32.setObjectName(u"verticalLayout_32")
        self.horizontalLayout_22 = QHBoxLayout()
        self.horizontalLayout_22.setObjectName(u"horizontalLayout_22")
        self.horizontalLayout_22.setContentsMargins(-1, -1, 0, -1)
        self.EM_steps_label = QLabel(self.EM_Seting)
        self.EM_steps_label.setObjectName(u"EM_steps_label")

        self.horizontalLayout_22.addWidget(self.EM_steps_label)

        self.EM_steps = QLineEdit(self.EM_Seting)
        self.EM_steps.setObjectName(u"EM_steps")

        self.horizontalLayout_22.addWidget(self.EM_steps)


        self.verticalLayout_32.addLayout(self.horizontalLayout_22)

        self.horizontalLayout_26 = QHBoxLayout()
        self.horizontalLayout_26.setObjectName(u"horizontalLayout_26")
        self.horizontalLayout_26.setContentsMargins(-1, -1, 0, -1)
        self.EM_rvdw_label = QLabel(self.EM_Seting)
        self.EM_rvdw_label.setObjectName(u"EM_rvdw_label")

        self.horizontalLayout_26.addWidget(self.EM_rvdw_label)

        self.EM_rvdw = QLineEdit(self.EM_Seting)
        self.EM_rvdw.setObjectName(u"EM_rvdw")

        self.horizontalLayout_26.addWidget(self.EM_rvdw)

        self.EM_extend_rvdw = QCheckBox(self.EM_Seting)
        self.EM_extend_rvdw.setObjectName(u"EM_extend_rvdw")

        self.horizontalLayout_26.addWidget(self.EM_extend_rvdw)


        self.verticalLayout_32.addLayout(self.horizontalLayout_26)

        self.horizontalLayout_30 = QHBoxLayout()
        self.horizontalLayout_30.setObjectName(u"horizontalLayout_30")
        self.Check_custom_EM_mdp = QCheckBox(self.EM_Seting)
        self.Check_custom_EM_mdp.setObjectName(u"Check_custom_EM_mdp")

        self.horizontalLayout_30.addWidget(self.Check_custom_EM_mdp)

        self.Custom_EM_mdp = QLineEdit(self.EM_Seting)
        self.Custom_EM_mdp.setObjectName(u"Custom_EM_mdp")

        self.horizontalLayout_30.addWidget(self.Custom_EM_mdp)


        self.verticalLayout_32.addLayout(self.horizontalLayout_30)


        self.verticalLayout_31.addWidget(self.EM_Seting)

        self.NVT_Seting = QGroupBox(self.Auto_balance)
        self.NVT_Seting.setObjectName(u"NVT_Seting")
        self.NVT_Seting.setCheckable(True)
        self.verticalLayout_33 = QVBoxLayout(self.NVT_Seting)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.horizontalLayout_23 = QHBoxLayout()
        self.horizontalLayout_23.setObjectName(u"horizontalLayout_23")
        self.horizontalLayout_23.setContentsMargins(-1, -1, 0, -1)
        self.NVT_step_label = QLabel(self.NVT_Seting)
        self.NVT_step_label.setObjectName(u"NVT_step_label")

        self.horizontalLayout_23.addWidget(self.NVT_step_label)

        self.NVT_step = QLineEdit(self.NVT_Seting)
        self.NVT_step.setObjectName(u"NVT_step")

        self.horizontalLayout_23.addWidget(self.NVT_step)


        self.verticalLayout_33.addLayout(self.horizontalLayout_23)

        self.horizontalLayout_24 = QHBoxLayout()
        self.horizontalLayout_24.setObjectName(u"horizontalLayout_24")
        self.horizontalLayout_24.setContentsMargins(-1, -1, 0, -1)
        self.NVT_rvdw_label = QLabel(self.NVT_Seting)
        self.NVT_rvdw_label.setObjectName(u"NVT_rvdw_label")

        self.horizontalLayout_24.addWidget(self.NVT_rvdw_label)

        self.NVT_rvdw = QLineEdit(self.NVT_Seting)
        self.NVT_rvdw.setObjectName(u"NVT_rvdw")

        self.horizontalLayout_24.addWidget(self.NVT_rvdw)

        self.NVT_extend_rvdw = QCheckBox(self.NVT_Seting)
        self.NVT_extend_rvdw.setObjectName(u"NVT_extend_rvdw")

        self.horizontalLayout_24.addWidget(self.NVT_extend_rvdw)


        self.verticalLayout_33.addLayout(self.horizontalLayout_24)

        self.horizontalLayout_25 = QHBoxLayout()
        self.horizontalLayout_25.setObjectName(u"horizontalLayout_25")
        self.horizontalLayout_25.setContentsMargins(-1, -1, 0, -1)
        self.NVT_Tem_label = QLabel(self.NVT_Seting)
        self.NVT_Tem_label.setObjectName(u"NVT_Tem_label")

        self.horizontalLayout_25.addWidget(self.NVT_Tem_label)

        self.NVT_Tem = QLineEdit(self.NVT_Seting)
        self.NVT_Tem.setObjectName(u"NVT_Tem")

        self.horizontalLayout_25.addWidget(self.NVT_Tem)


        self.verticalLayout_33.addLayout(self.horizontalLayout_25)

        self.horizontalLayout_31 = QHBoxLayout()
        self.horizontalLayout_31.setObjectName(u"horizontalLayout_31")
        self.Check_custum_NVT_file = QCheckBox(self.NVT_Seting)
        self.Check_custum_NVT_file.setObjectName(u"Check_custum_NVT_file")

        self.horizontalLayout_31.addWidget(self.Check_custum_NVT_file)

        self.NVT_mdp_file = QLineEdit(self.NVT_Seting)
        self.NVT_mdp_file.setObjectName(u"NVT_mdp_file")

        self.horizontalLayout_31.addWidget(self.NVT_mdp_file)


        self.verticalLayout_33.addLayout(self.horizontalLayout_31)


        self.verticalLayout_31.addWidget(self.NVT_Seting)

        self.NPT_Seting = QGroupBox(self.Auto_balance)
        self.NPT_Seting.setObjectName(u"NPT_Seting")
        self.NPT_Seting.setFlat(False)
        self.NPT_Seting.setCheckable(True)
        self.verticalLayout_34 = QVBoxLayout(self.NPT_Seting)
        self.verticalLayout_34.setObjectName(u"verticalLayout_34")
        self.horizontalLayout_27 = QHBoxLayout()
        self.horizontalLayout_27.setObjectName(u"horizontalLayout_27")
        self.horizontalLayout_27.setContentsMargins(-1, -1, 0, -1)
        self.NPT_Setps_labe = QLabel(self.NPT_Seting)
        self.NPT_Setps_labe.setObjectName(u"NPT_Setps_labe")

        self.horizontalLayout_27.addWidget(self.NPT_Setps_labe)

        self.NPT_Setps = QLineEdit(self.NPT_Seting)
        self.NPT_Setps.setObjectName(u"NPT_Setps")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(200)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.NPT_Setps.sizePolicy().hasHeightForWidth())
        self.NPT_Setps.setSizePolicy(sizePolicy1)

        self.horizontalLayout_27.addWidget(self.NPT_Setps)


        self.verticalLayout_34.addLayout(self.horizontalLayout_27)

        self.horizontalLayout_28 = QHBoxLayout()
        self.horizontalLayout_28.setObjectName(u"horizontalLayout_28")
        self.horizontalLayout_28.setContentsMargins(-1, -1, 0, -1)
        self.NPT_rvdw_label = QLabel(self.NPT_Seting)
        self.NPT_rvdw_label.setObjectName(u"NPT_rvdw_label")

        self.horizontalLayout_28.addWidget(self.NPT_rvdw_label)

        self.NPT_rvdw = QLineEdit(self.NPT_Seting)
        self.NPT_rvdw.setObjectName(u"NPT_rvdw")

        self.horizontalLayout_28.addWidget(self.NPT_rvdw)

        self.NPT_extend_rvdw = QCheckBox(self.NPT_Seting)
        self.NPT_extend_rvdw.setObjectName(u"NPT_extend_rvdw")

        self.horizontalLayout_28.addWidget(self.NPT_extend_rvdw)


        self.verticalLayout_34.addLayout(self.horizontalLayout_28)

        self.horizontalLayout_29 = QHBoxLayout()
        self.horizontalLayout_29.setObjectName(u"horizontalLayout_29")
        self.horizontalLayout_29.setContentsMargins(-1, -1, 0, -1)
        self.NPT_pres_label = QLabel(self.NPT_Seting)
        self.NPT_pres_label.setObjectName(u"NPT_pres_label")

        self.horizontalLayout_29.addWidget(self.NPT_pres_label)

        self.NPT_pres = QLineEdit(self.NPT_Seting)
        self.NPT_pres.setObjectName(u"NPT_pres")

        self.horizontalLayout_29.addWidget(self.NPT_pres)


        self.verticalLayout_34.addLayout(self.horizontalLayout_29)

        self.horizontalLayout_32 = QHBoxLayout()
        self.horizontalLayout_32.setObjectName(u"horizontalLayout_32")
        self.Check_NPT_mdp_file = QCheckBox(self.NPT_Seting)
        self.Check_NPT_mdp_file.setObjectName(u"Check_NPT_mdp_file")

        self.horizontalLayout_32.addWidget(self.Check_NPT_mdp_file)

        self.NPT_mdp_file_path = QLineEdit(self.NPT_Seting)
        self.NPT_mdp_file_path.setObjectName(u"NPT_mdp_file_path")

        self.horizontalLayout_32.addWidget(self.NPT_mdp_file_path)


        self.verticalLayout_34.addLayout(self.horizontalLayout_32)


        self.verticalLayout_31.addWidget(self.NPT_Seting)

        self.verticalLayout_31.setStretch(3, 1)

        self.verticalLayout_30.addWidget(self.Auto_balance)

        self.Config_list.addItem(self.EM_NVT_NPT_seting, u"Energy minimization and system balance")
        self.SMD_MD_Seting = QWidget()
        self.SMD_MD_Seting.setObjectName(u"SMD_MD_Seting")
        self.SMD_MD_Seting.setGeometry(QRect(0, 0, 702, 600))
        self.verticalLayout_35 = QVBoxLayout(self.SMD_MD_Seting)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.verticalLayout_35.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.Run_SMD = QGroupBox(self.SMD_MD_Seting)
        self.Run_SMD.setObjectName(u"Run_SMD")
        self.Run_SMD.setCheckable(True)
        self.verticalLayout_10 = QVBoxLayout(self.Run_SMD)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.horizontalLayout_39 = QHBoxLayout()
        self.horizontalLayout_39.setObjectName(u"horizontalLayout_39")
        self.horizontalLayout_39.setContentsMargins(-1, -1, 300, -1)
        self.label_2 = QLabel(self.Run_SMD)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_39.addWidget(self.label_2)

        self.Ligand_name_set_2 = QLineEdit(self.Run_SMD)
        self.Ligand_name_set_2.setObjectName(u"Ligand_name_set_2")

        self.horizontalLayout_39.addWidget(self.Ligand_name_set_2)


        self.verticalLayout_10.addLayout(self.horizontalLayout_39)

        self.horizontalLayout_33 = QHBoxLayout()
        self.horizontalLayout_33.setObjectName(u"horizontalLayout_33")
        self.horizontalLayout_33.setContentsMargins(-1, -1, 300, -1)
        self.label_32 = QLabel(self.Run_SMD)
        self.label_32.setObjectName(u"label_32")

        self.horizontalLayout_33.addWidget(self.label_32)

        self.SMD_Cycle_numb = QLineEdit(self.Run_SMD)
        self.SMD_Cycle_numb.setObjectName(u"SMD_Cycle_numb")

        self.horizontalLayout_33.addWidget(self.SMD_Cycle_numb)

        self.SMD_Cycle_numb_label = QLabel(self.Run_SMD)
        self.SMD_Cycle_numb_label.setObjectName(u"SMD_Cycle_numb_label")

        self.horizontalLayout_33.addWidget(self.SMD_Cycle_numb_label)


        self.verticalLayout_10.addLayout(self.horizontalLayout_33)

        self.Check_rm_xtc_file = QCheckBox(self.Run_SMD)
        self.Check_rm_xtc_file.setObjectName(u"Check_rm_xtc_file")

        self.verticalLayout_10.addWidget(self.Check_rm_xtc_file)


        self.verticalLayout_35.addWidget(self.Run_SMD)

        self.Run_MD = QGroupBox(self.SMD_MD_Seting)
        self.Run_MD.setObjectName(u"Run_MD")
        self.Run_MD.setCheckable(True)
        self.verticalLayout_25 = QVBoxLayout(self.Run_MD)
        self.verticalLayout_25.setObjectName(u"verticalLayout_25")
        self.horizontalLayout_40 = QHBoxLayout()
        self.horizontalLayout_40.setObjectName(u"horizontalLayout_40")
        self.horizontalLayout_40.setContentsMargins(-1, -1, 300, -1)
        self.label_3 = QLabel(self.Run_MD)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_40.addWidget(self.label_3)

        self.Ligand_name_set_3 = QLineEdit(self.Run_MD)
        self.Ligand_name_set_3.setObjectName(u"Ligand_name_set_3")

        self.horizontalLayout_40.addWidget(self.Ligand_name_set_3)


        self.verticalLayout_25.addLayout(self.horizontalLayout_40)

        self.horizontalLayout_42 = QHBoxLayout()
        self.horizontalLayout_42.setObjectName(u"horizontalLayout_42")
        self.MD_Time_label = QLabel(self.Run_MD)
        self.MD_Time_label.setObjectName(u"MD_Time_label")

        self.horizontalLayout_42.addWidget(self.MD_Time_label)

        self.MD_Time = QLineEdit(self.Run_MD)
        self.MD_Time.setObjectName(u"MD_Time")

        self.horizontalLayout_42.addWidget(self.MD_Time)


        self.verticalLayout_25.addLayout(self.horizontalLayout_42)

        self.horizontalLayout_43 = QHBoxLayout()
        self.horizontalLayout_43.setObjectName(u"horizontalLayout_43")
        self.MD_Time_Step_label = QLabel(self.Run_MD)
        self.MD_Time_Step_label.setObjectName(u"MD_Time_Step_label")

        self.horizontalLayout_43.addWidget(self.MD_Time_Step_label)

        self.MD_Time_Step = QLineEdit(self.Run_MD)
        self.MD_Time_Step.setObjectName(u"MD_Time_Step")

        self.horizontalLayout_43.addWidget(self.MD_Time_Step)


        self.verticalLayout_25.addLayout(self.horizontalLayout_43)

        self.horizontalLayout_44 = QHBoxLayout()
        self.horizontalLayout_44.setObjectName(u"horizontalLayout_44")
        self.Recording_interval = QLabel(self.Run_MD)
        self.Recording_interval.setObjectName(u"Recording_interval")

        self.horizontalLayout_44.addWidget(self.Recording_interval)

        self.Trajectory_label = QLabel(self.Run_MD)
        self.Trajectory_label.setObjectName(u"Trajectory_label")

        self.horizontalLayout_44.addWidget(self.Trajectory_label)

        self.Trajectory_Recording = QLineEdit(self.Run_MD)
        self.Trajectory_Recording.setObjectName(u"Trajectory_Recording")

        self.horizontalLayout_44.addWidget(self.Trajectory_Recording)

        self.Energy_label = QLabel(self.Run_MD)
        self.Energy_label.setObjectName(u"Energy_label")

        self.horizontalLayout_44.addWidget(self.Energy_label)

        self.Energy_Recording = QLineEdit(self.Run_MD)
        self.Energy_Recording.setObjectName(u"Energy_Recording")

        self.horizontalLayout_44.addWidget(self.Energy_Recording)


        self.verticalLayout_25.addLayout(self.horizontalLayout_44)

        self.horizontalLayout_46 = QHBoxLayout()
        self.horizontalLayout_46.setObjectName(u"horizontalLayout_46")
        self.Frame_Export_label = QLabel(self.Run_MD)
        self.Frame_Export_label.setObjectName(u"Frame_Export_label")

        self.horizontalLayout_46.addWidget(self.Frame_Export_label)

        self.Frame_Export = QLineEdit(self.Run_MD)
        self.Frame_Export.setObjectName(u"Frame_Export")

        self.horizontalLayout_46.addWidget(self.Frame_Export)


        self.verticalLayout_25.addLayout(self.horizontalLayout_46)

        self.horizontalLayout_45 = QHBoxLayout()
        self.horizontalLayout_45.setObjectName(u"horizontalLayout_45")
        self.MD_Cutoff_Rafius_label = QLabel(self.Run_MD)
        self.MD_Cutoff_Rafius_label.setObjectName(u"MD_Cutoff_Rafius_label")

        self.horizontalLayout_45.addWidget(self.MD_Cutoff_Rafius_label)

        self.MD_Cutoff_Rafius = QLineEdit(self.Run_MD)
        self.MD_Cutoff_Rafius.setObjectName(u"MD_Cutoff_Rafius")

        self.horizontalLayout_45.addWidget(self.MD_Cutoff_Rafius)


        self.verticalLayout_25.addLayout(self.horizontalLayout_45)

        self.horizontalLayout_37 = QHBoxLayout()
        self.horizontalLayout_37.setObjectName(u"horizontalLayout_37")
        self.check_custum_mdp_file = QCheckBox(self.Run_MD)
        self.check_custum_mdp_file.setObjectName(u"check_custum_mdp_file")

        self.horizontalLayout_37.addWidget(self.check_custum_mdp_file)

        self.md_mdp_file_path = QLineEdit(self.Run_MD)
        self.md_mdp_file_path.setObjectName(u"md_mdp_file_path")

        self.horizontalLayout_37.addWidget(self.md_mdp_file_path)


        self.verticalLayout_25.addLayout(self.horizontalLayout_37)


        self.verticalLayout_35.addWidget(self.Run_MD)

        self.verticalLayout_35.setStretch(0, 1)
        self.verticalLayout_35.setStretch(1, 2)
        self.Config_list.addItem(self.SMD_MD_Seting, u"Perform SMD or MD calculations")
        self.Server_list_Seting = QWidget()
        self.Server_list_Seting.setObjectName(u"Server_list_Seting")
        self.Server_list_Seting.setGeometry(QRect(0, 0, 702, 600))
        self.horizontalLayout_34 = QHBoxLayout(self.Server_list_Seting)
        self.horizontalLayout_34.setObjectName(u"horizontalLayout_34")
        self.Server_Seting = QGroupBox(self.Server_list_Seting)
        self.Server_Seting.setObjectName(u"Server_Seting")
        self.Server_Seting.setCheckable(True)
        self.horizontalLayout_35 = QHBoxLayout(self.Server_Seting)
        self.horizontalLayout_35.setObjectName(u"horizontalLayout_35")
        self.EM_Server_list = QGroupBox(self.Server_Seting)
        self.EM_Server_list.setObjectName(u"EM_Server_list")
        self.EM_Server_list.setFlat(False)
        self.EM_Server_list.setCheckable(False)
        self.verticalLayout_37 = QVBoxLayout(self.EM_Server_list)
        self.verticalLayout_37.setObjectName(u"verticalLayout_37")
        self.EM_Server_Slect_List = QListWidget(self.EM_Server_list)
        self.EM_Server_Slect_List.setObjectName(u"EM_Server_Slect_List")

        self.verticalLayout_37.addWidget(self.EM_Server_Slect_List)

        self.Select_all_EM_Server = QPushButton(self.EM_Server_list)
        self.Select_all_EM_Server.setObjectName(u"Select_all_EM_Server")

        self.verticalLayout_37.addWidget(self.Select_all_EM_Server)

        self.Clear_all_EM_Server = QPushButton(self.EM_Server_list)
        self.Clear_all_EM_Server.setObjectName(u"Clear_all_EM_Server")

        self.verticalLayout_37.addWidget(self.Clear_all_EM_Server)


        self.horizontalLayout_35.addWidget(self.EM_Server_list)

        self.NVT_Server_list = QGroupBox(self.Server_Seting)
        self.NVT_Server_list.setObjectName(u"NVT_Server_list")
        self.verticalLayout_38 = QVBoxLayout(self.NVT_Server_list)
        self.verticalLayout_38.setObjectName(u"verticalLayout_38")
        self.NVT_Server_Slect_List = QListWidget(self.NVT_Server_list)
        self.NVT_Server_Slect_List.setObjectName(u"NVT_Server_Slect_List")

        self.verticalLayout_38.addWidget(self.NVT_Server_Slect_List)

        self.Select_all_NVT_Server = QPushButton(self.NVT_Server_list)
        self.Select_all_NVT_Server.setObjectName(u"Select_all_NVT_Server")

        self.verticalLayout_38.addWidget(self.Select_all_NVT_Server)

        self.Clear_all_NVT_Server = QPushButton(self.NVT_Server_list)
        self.Clear_all_NVT_Server.setObjectName(u"Clear_all_NVT_Server")

        self.verticalLayout_38.addWidget(self.Clear_all_NVT_Server)


        self.horizontalLayout_35.addWidget(self.NVT_Server_list)

        self.NPT_Server_list = QGroupBox(self.Server_Seting)
        self.NPT_Server_list.setObjectName(u"NPT_Server_list")
        self.verticalLayout_39 = QVBoxLayout(self.NPT_Server_list)
        self.verticalLayout_39.setObjectName(u"verticalLayout_39")
        self.NPT_Server_Slect_List = QListWidget(self.NPT_Server_list)
        self.NPT_Server_Slect_List.setObjectName(u"NPT_Server_Slect_List")

        self.verticalLayout_39.addWidget(self.NPT_Server_Slect_List)

        self.Select_all_NPT_Server_list = QPushButton(self.NPT_Server_list)
        self.Select_all_NPT_Server_list.setObjectName(u"Select_all_NPT_Server_list")

        self.verticalLayout_39.addWidget(self.Select_all_NPT_Server_list)

        self.Clear_all_NPT_Server_list = QPushButton(self.NPT_Server_list)
        self.Clear_all_NPT_Server_list.setObjectName(u"Clear_all_NPT_Server_list")

        self.verticalLayout_39.addWidget(self.Clear_all_NPT_Server_list)


        self.horizontalLayout_35.addWidget(self.NPT_Server_list)

        self.SMD_Server_list = QGroupBox(self.Server_Seting)
        self.SMD_Server_list.setObjectName(u"SMD_Server_list")
        self.verticalLayout_41 = QVBoxLayout(self.SMD_Server_list)
        self.verticalLayout_41.setObjectName(u"verticalLayout_41")
        self.SMD_Server_Slect_List = QListWidget(self.SMD_Server_list)
        self.SMD_Server_Slect_List.setObjectName(u"SMD_Server_Slect_List")

        self.verticalLayout_41.addWidget(self.SMD_Server_Slect_List)

        self.Select_all_SMD_Server_list = QPushButton(self.SMD_Server_list)
        self.Select_all_SMD_Server_list.setObjectName(u"Select_all_SMD_Server_list")

        self.verticalLayout_41.addWidget(self.Select_all_SMD_Server_list)

        self.Clear_all_SMD_Server_list = QPushButton(self.SMD_Server_list)
        self.Clear_all_SMD_Server_list.setObjectName(u"Clear_all_SMD_Server_list")

        self.verticalLayout_41.addWidget(self.Clear_all_SMD_Server_list)


        self.horizontalLayout_35.addWidget(self.SMD_Server_list)

        self.MD_Server_list = QGroupBox(self.Server_Seting)
        self.MD_Server_list.setObjectName(u"MD_Server_list")
        self.verticalLayout_42 = QVBoxLayout(self.MD_Server_list)
        self.verticalLayout_42.setObjectName(u"verticalLayout_42")
        self.MD_Server_Slect_List = QListWidget(self.MD_Server_list)
        self.MD_Server_Slect_List.setObjectName(u"MD_Server_Slect_List")

        self.verticalLayout_42.addWidget(self.MD_Server_Slect_List)

        self.Select_all_MD_Server_list = QPushButton(self.MD_Server_list)
        self.Select_all_MD_Server_list.setObjectName(u"Select_all_MD_Server_list")

        self.verticalLayout_42.addWidget(self.Select_all_MD_Server_list)

        self.Cler_all_MD_Server_list = QPushButton(self.MD_Server_list)
        self.Cler_all_MD_Server_list.setObjectName(u"Cler_all_MD_Server_list")

        self.verticalLayout_42.addWidget(self.Cler_all_MD_Server_list)


        self.horizontalLayout_35.addWidget(self.MD_Server_list)


        self.horizontalLayout_34.addWidget(self.Server_Seting)

        self.Config_list.addItem(self.Server_list_Seting, u"Calculation server selection")

        self.verticalLayout_7.addWidget(self.Config_list)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.horizontalLayout_36.addWidget(self.scrollArea)

        self.horizontalLayout_36.setStretch(0, 2)
        self.horizontalLayout_36.setStretch(2, 3)
        self.Seting_Tab.addTab(self.Run_Step_Interface, "")
        self.run_command = QWidget()
        self.run_command.setObjectName(u"run_command")
        self.verticalLayout_4 = QVBoxLayout(self.run_command)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_5 = QVBoxLayout()
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 5, 5, 5)
        self.Log_Monitor = QTextBrowser(self.run_command)
        self.Log_Monitor.setObjectName(u"Log_Monitor")

        self.verticalLayout_5.addWidget(self.Log_Monitor)

        self.progressBar = QProgressBar(self.run_command)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(100)

        self.verticalLayout_5.addWidget(self.progressBar)


        self.verticalLayout_4.addLayout(self.verticalLayout_5)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.Host_Select_Combo = QComboBox(self.run_command)
        self.Host_Select_Combo.setObjectName(u"Host_Select_Combo")

        self.horizontalLayout.addWidget(self.Host_Select_Combo)

        self.Folder_Path_Select_Combo = QComboBox(self.run_command)
        self.Folder_Path_Select_Combo.setObjectName(u"Folder_Path_Select_Combo")

        self.horizontalLayout.addWidget(self.Folder_Path_Select_Combo)

        self.Command_line = QLineEdit(self.run_command)
        self.Command_line.setObjectName(u"Command_line")

        self.horizontalLayout.addWidget(self.Command_line)

        self.Run_Command_Button = QPushButton(self.run_command)
        self.Run_Command_Button.setObjectName(u"Run_Command_Button")

        self.horizontalLayout.addWidget(self.Run_Command_Button)


        self.verticalLayout_4.addLayout(self.horizontalLayout)

        self.Seting_Tab.addTab(self.run_command, "")
        self.Result_Summary = QWidget()
        self.Result_Summary.setObjectName(u"Result_Summary")
        self.verticalLayout_20 = QVBoxLayout(self.Result_Summary)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_19 = QVBoxLayout()
        self.verticalLayout_19.setObjectName(u"verticalLayout_19")
        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton = QPushButton(self.Result_Summary)
        self.pushButton.setObjectName(u"pushButton")

        self.horizontalLayout_9.addWidget(self.pushButton)

        self.pushButton_2 = QPushButton(self.Result_Summary)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_9.addWidget(self.pushButton_2)


        self.verticalLayout_19.addLayout(self.horizontalLayout_9)


        self.verticalLayout_20.addLayout(self.verticalLayout_19)

        self.tabWidget = QTabWidget(self.Result_Summary)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setTabPosition(QTabWidget.TabPosition.West)
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabBarAutoHide(False)
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tabWidget.addTab(self.tab_3, "")

        self.verticalLayout_20.addWidget(self.tabWidget)

        self.Seting_Tab.addTab(self.Result_Summary, "")

        self.horizontalLayout_47.addWidget(self.Seting_Tab)

        self.horizontalLayout_47.setStretch(0, 3)
        self.horizontalLayout_47.setStretch(1, 7)

        self.verticalLayout_2.addLayout(self.horizontalLayout_47)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.folder_tree_collapse = QPushButton(self.Main_window)
        self.folder_tree_collapse.setObjectName(u"folder_tree_collapse")

        self.horizontalLayout_2.addWidget(self.folder_tree_collapse)

        self.Clear_Selection = QPushButton(self.Main_window)
        self.Clear_Selection.setObjectName(u"Clear_Selection")

        self.horizontalLayout_2.addWidget(self.Clear_Selection)

        self.Refresh_Button = QPushButton(self.Main_window)
        self.Refresh_Button.setObjectName(u"Refresh_Button")

        self.horizontalLayout_2.addWidget(self.Refresh_Button)

        self.Clear_Log_Button = QPushButton(self.Main_window)
        self.Clear_Log_Button.setObjectName(u"Clear_Log_Button")

        self.horizontalLayout_2.addWidget(self.Clear_Log_Button)


        self.verticalLayout_2.addLayout(self.horizontalLayout_2)


        self.verticalLayout_3.addLayout(self.verticalLayout_2)

        GMX_GUI.setCentralWidget(self.Main_window)
        self.menubar = QMenuBar(GMX_GUI)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1800, 23))
        self.menubar_file = QMenu(self.menubar)
        self.menubar_file.setObjectName(u"menubar_file")
        self.menubar_config = QMenu(self.menubar)
        self.menubar_config.setObjectName(u"menubar_config")
        self.menubar_info = QMenu(self.menubar)
        self.menubar_info.setObjectName(u"menubar_info")
        GMX_GUI.setMenuBar(self.menubar)

        self.menubar.addAction(self.menubar_file.menuAction())
        self.menubar.addAction(self.menubar_config.menuAction())
        self.menubar.addAction(self.menubar_info.menuAction())
        self.menubar_file.addAction(self.actionChange_working_path)
        self.menubar_config.addAction(self.actionDefault_Settings)

        self.retranslateUi(GMX_GUI)

        self.Seting_Tab.setCurrentIndex(0)
        self.Config_list.setCurrentIndex(6)
        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(GMX_GUI)
    # setupUi

    def retranslateUi(self, GMX_GUI):
        GMX_GUI.setWindowTitle(QCoreApplication.translate("GMX_GUI", u"MainWindow", None))
        self.actionChange_working_path.setText(QCoreApplication.translate("GMX_GUI", u"Change Working PATH", None))
        self.actionDefault_Settings.setText(QCoreApplication.translate("GMX_GUI", u"Default Settings", None))
        self.path_display.setText(QCoreApplication.translate("GMX_GUI", u"Current PATH:", None))
        self.Filter_line.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"Enter folder name to filter", None))
        self.Clear_filters_button.setText(QCoreApplication.translate("GMX_GUI", u"Clear filters", None))
        self.select_numb_count.setText(QCoreApplication.translate("GMX_GUI", u"Total:          Filtered:          Selected:", None))
        self.label.setText(QCoreApplication.translate("GMX_GUI", u"Run Folder List:", None))
        self.Execute_toolButton.setText(QCoreApplication.translate("GMX_GUI", u"...", None))
        self.Run_Step_Task.setText(QCoreApplication.translate("GMX_GUI", u"Execute the task", None))
        self.Auto_Move_File.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatically assign task files", None))
        self.Ligand_endswith_label.setText(QCoreApplication.translate("GMX_GUI", u"Ligand File Suffix:", None))
        self.Ligand_endswith.setInputMask("")
        self.Ligand_endswith.setText(QCoreApplication.translate("GMX_GUI", u".mol2", None))
        self.Ligand_endswith.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u".mol2", None))
        self.protein_endswith_label.setText(QCoreApplication.translate("GMX_GUI", u"Receptor File Suffix:", None))
        self.protein_endswith.setInputMask("")
        self.protein_endswith.setText(QCoreApplication.translate("GMX_GUI", u".pdb", None))
        self.protein_endswith.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u".pdb", None))
        self.folder_name_index_label.setText(QCoreApplication.translate("GMX_GUI", u"Folder Name Index:", None))
        self.folder_name_index.setText(QCoreApplication.translate("GMX_GUI", u"0", None))
        self.Copy_receptor.setTitle(QCoreApplication.translate("GMX_GUI", u"Copy the same receptor file", None))
        self.receptor_file_path_label.setText(QCoreApplication.translate("GMX_GUI", u"Receptor File Path:", None))
        self.receptor_file_path.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"recepror pdb file path", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Config_Move_File), QCoreApplication.translate("GMX_GUI", u"Distribute task files", None))
        self.Rename_Ligane.setTitle(QCoreApplication.translate("GMX_GUI", u"Rename ligand file residues", None))
        self.Ligand_Name_label.setText(QCoreApplication.translate("GMX_GUI", u"Unified ligand names", None))
        self.Ligand_Name.setText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.Ligand_Name.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.Repair_Receptor.setTitle(QCoreApplication.translate("GMX_GUI", u"Check and repair the receptor file", None))
        self.Repair_main_chain.setText(QCoreApplication.translate("GMX_GUI", u"Repair main chain missing as much as possible", None))
        self.Repair_missing_side_chain.setText(QCoreApplication.translate("GMX_GUI", u"Repair missing side chain atoms", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Ligand_protein_prep_Seting), QCoreApplication.translate("GMX_GUI", u"Prepare ligand receptor files", None))
        self.Gen_ligand_top.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatical generation of ligand topology structure", None))
        self.Generate_top_by_GAFF.setTitle(QCoreApplication.translate("GMX_GUI", u"Generate molecular topology using GAFF", None))
        self.Sob_top_PATH_label.setText(QCoreApplication.translate("GMX_GUI", u"Sobtop PATH:", None))
        self.IF_rename_ligand.setText(QCoreApplication.translate("GMX_GUI", u"Rename the ligand molecule:", None))
        self.Rename_ligand_name.setText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.Rename_ligand_name.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.Generate_top_by_CGENFF.setTitle(QCoreApplication.translate("GMX_GUI", u"Generate molecular topology using CGENFF", None))
        self.CGENFF_web_URL_label.setText(QCoreApplication.translate("GMX_GUI", u"CgenFF Web URL:", None))
        self.CGENFF_web_URL.setText(QCoreApplication.translate("GMX_GUI", u"https://app.cgenff.com/login", None))
        self.CGENFF_user_name_abel.setText(QCoreApplication.translate("GMX_GUI", u"User Name:", None))
        self.CGENFF_pw_label.setText(QCoreApplication.translate("GMX_GUI", u"PassWord:", None))
        self.IF_use_Proxy.setText(QCoreApplication.translate("GMX_GUI", u"Use Proxy:", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Ligand_top_Seting), QCoreApplication.translate("GMX_GUI", u"Generate ligand topology", None))
        self.Gen_Protein_top.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatically generate protein ligands", None))
        self.Force_Field_selt_label.setText(QCoreApplication.translate("GMX_GUI", u"Select Molecular Force Field:", None))
        self.water_model_selt_label.setText(QCoreApplication.translate("GMX_GUI", u"Select water model:", None))
        self.N_term_selt_label.setText(QCoreApplication.translate("GMX_GUI", u"Select the N-terminal protonation state:", None))
        self.C_term_selt_label.setText(QCoreApplication.translate("GMX_GUI", u"Select the C-terminal protonation state:", None))
        self.Morge_complex_gro.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatically check and merge top files and automatically generate complex.gro files", None))
        self.merge_top_file_ff_selt_label.setText(QCoreApplication.translate("GMX_GUI", u"Force Field Used", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Protein_top_Seting), QCoreApplication.translate("GMX_GUI", u"Generate protein topology", None))
        self.Gen_Solvation_box.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatically generate solvation boxes", None))
        self.Box_size_set_label.setText(QCoreApplication.translate("GMX_GUI", u"Box size distace(A)", None))
        self.Box_size_set.setText(QCoreApplication.translate("GMX_GUI", u"10", None))
        self.Box_size_set.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"10", None))
        self.Box_shape_sele_label.setText(QCoreApplication.translate("GMX_GUI", u"Box shape", None))
        self.Add_ions_to_box.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatically add ions to the box", None))
        self.Neutralize_System.setTitle(QCoreApplication.translate("GMX_GUI", u"Ion placement", None))
        self.label_16.setText(QCoreApplication.translate("GMX_GUI", u"Neutralize by addine", None))
        self.label_17.setText(QCoreApplication.translate("GMX_GUI", u"ions", None))
        self.Add_salt_density.setTitle(QCoreApplication.translate("GMX_GUI", u"Add salt", None))
        self.Salt_density_set_label.setText(QCoreApplication.translate("GMX_GUI", u"Salt concentration:", None))
        self.label_19.setText(QCoreApplication.translate("GMX_GUI", u"M", None))
        self.selt_positive_ion_label.setText(QCoreApplication.translate("GMX_GUI", u"Salt positive ion:", None))
        self.selt_negatibe_ion_label.setText(QCoreApplication.translate("GMX_GUI", u"Salt negative ion:", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Solvation_box_seting), QCoreApplication.translate("GMX_GUI", u"Generate Solvation Box", None))
        self.Auto_balance.setTitle(QCoreApplication.translate("GMX_GUI", u"Automatic energy minimization and NVT, NPT", None))
        self.Ligand_name_set_label.setText(QCoreApplication.translate("GMX_GUI", u"Ligand name", None))
        self.Ligand_name_set.setText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.Ligand_name_set.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"LIG", None))
        self.EM_Seting.setTitle(QCoreApplication.translate("GMX_GUI", u"Energy minimization", None))
        self.EM_steps_label.setText(QCoreApplication.translate("GMX_GUI", u"Max setps:", None))
        self.EM_steps.setText(QCoreApplication.translate("GMX_GUI", u"2000", None))
        self.EM_rvdw_label.setText(QCoreApplication.translate("GMX_GUI", u"Default rvdw(nm):", None))
        self.EM_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"1.2", None))
        self.EM_extend_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"Extend rvdw if run fails", None))
        self.Check_custom_EM_mdp.setText(QCoreApplication.translate("GMX_GUI", u"Using custom mdp parameters", None))
        self.Custom_EM_mdp.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"mdp file path", None))
        self.NVT_Seting.setTitle(QCoreApplication.translate("GMX_GUI", u"NVT", None))
        self.NVT_step_label.setText(QCoreApplication.translate("GMX_GUI", u"Steps:", None))
        self.NVT_step.setText(QCoreApplication.translate("GMX_GUI", u"50000", None))
        self.NVT_rvdw_label.setText(QCoreApplication.translate("GMX_GUI", u"Default rvdw(nm):", None))
        self.NVT_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"1.2", None))
        self.NVT_extend_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"Extend rvdw if run fails", None))
        self.NVT_Tem_label.setText(QCoreApplication.translate("GMX_GUI", u"Temperature(K):", None))
        self.NVT_Tem.setText(QCoreApplication.translate("GMX_GUI", u"300", None))
        self.Check_custum_NVT_file.setText(QCoreApplication.translate("GMX_GUI", u"Using custom mdp parameters", None))
        self.NVT_mdp_file.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"mdp file path", None))
        self.NPT_Seting.setTitle(QCoreApplication.translate("GMX_GUI", u"NPT", None))
        self.NPT_Setps_labe.setText(QCoreApplication.translate("GMX_GUI", u"Steps:", None))
        self.NPT_Setps.setText(QCoreApplication.translate("GMX_GUI", u"50000", None))
        self.NPT_rvdw_label.setText(QCoreApplication.translate("GMX_GUI", u"Default rvdw(nm):", None))
        self.NPT_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"1.2", u"1.2"))
        self.NPT_extend_rvdw.setText(QCoreApplication.translate("GMX_GUI", u"Extend rvdw if run fails", None))
        self.NPT_pres_label.setText(QCoreApplication.translate("GMX_GUI", u"Pressure(bar):", None))
        self.NPT_pres.setText(QCoreApplication.translate("GMX_GUI", u"1.0", None))
        self.Check_NPT_mdp_file.setText(QCoreApplication.translate("GMX_GUI", u"Using custom mdp parameters", None))
        self.NPT_mdp_file_path.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"mdp file path", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.EM_NVT_NPT_seting), QCoreApplication.translate("GMX_GUI", u"Energy minimization and system balance", None))
        self.Run_SMD.setTitle(QCoreApplication.translate("GMX_GUI", u"Run SMD", None))
        self.label_2.setText(QCoreApplication.translate("GMX_GUI", u"Ligand name", None))
        self.label_32.setText(QCoreApplication.translate("GMX_GUI", u"Run", None))
        self.SMD_Cycle_numb.setText(QCoreApplication.translate("GMX_GUI", u"3", None))
        self.SMD_Cycle_numb.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"3", None))
        self.SMD_Cycle_numb_label.setText(QCoreApplication.translate("GMX_GUI", u"replicates per molecule", None))
        self.Check_rm_xtc_file.setText(QCoreApplication.translate("GMX_GUI", u"Delete the trajectory file after running", None))
        self.Run_MD.setTitle(QCoreApplication.translate("GMX_GUI", u"Run MD", None))
        self.label_3.setText(QCoreApplication.translate("GMX_GUI", u"Ligand name", None))
        self.MD_Time_label.setText(QCoreApplication.translate("GMX_GUI", u"Total time(ns):", None))
        self.MD_Time.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"1", None))
        self.MD_Time_Step_label.setText(QCoreApplication.translate("GMX_GUI", u"Time step(fs):", None))
        self.MD_Time_Step.setText(QCoreApplication.translate("GMX_GUI", u"2", None))
        self.MD_Time_Step.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"2", None))
        self.Recording_interval.setText(QCoreApplication.translate("GMX_GUI", u"Recording interval(ps):", None))
        self.Trajectory_label.setText(QCoreApplication.translate("GMX_GUI", u"Trajectory:", None))
        self.Energy_label.setText(QCoreApplication.translate("GMX_GUI", u"Energy:", None))
        self.Frame_Export_label.setText(QCoreApplication.translate("GMX_GUI", u"Approximate number of frames:", None))
        self.Frame_Export.setText("")
        self.Frame_Export.setPlaceholderText("")
        self.MD_Cutoff_Rafius_label.setText(QCoreApplication.translate("GMX_GUI", u"Cutoff rafius(A):", None))
        self.MD_Cutoff_Rafius.setText(QCoreApplication.translate("GMX_GUI", u"9", None))
        self.MD_Cutoff_Rafius.setPlaceholderText(QCoreApplication.translate("GMX_GUI", u"9", None))
        self.check_custum_mdp_file.setText(QCoreApplication.translate("GMX_GUI", u"Using custom mdp parameters", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.SMD_MD_Seting), QCoreApplication.translate("GMX_GUI", u"Perform SMD or MD calculations", None))
        self.Server_Seting.setTitle(QCoreApplication.translate("GMX_GUI", u"Distribute tasks to servers", None))
        self.EM_Server_list.setTitle(QCoreApplication.translate("GMX_GUI", u"EM Server", None))
        self.Select_all_EM_Server.setText(QCoreApplication.translate("GMX_GUI", u"Select all", None))
        self.Clear_all_EM_Server.setText(QCoreApplication.translate("GMX_GUI", u"Clear all", None))
        self.NVT_Server_list.setTitle(QCoreApplication.translate("GMX_GUI", u"NVT Server", None))
        self.Select_all_NVT_Server.setText(QCoreApplication.translate("GMX_GUI", u"Select all", None))
        self.Clear_all_NVT_Server.setText(QCoreApplication.translate("GMX_GUI", u"Clear all", None))
        self.NPT_Server_list.setTitle(QCoreApplication.translate("GMX_GUI", u"NPT Server", None))
        self.Select_all_NPT_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Select all", None))
        self.Clear_all_NPT_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Clear all", None))
        self.SMD_Server_list.setTitle(QCoreApplication.translate("GMX_GUI", u"SMD Server", None))
        self.Select_all_SMD_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Select all", None))
        self.Clear_all_SMD_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Clear all", None))
        self.MD_Server_list.setTitle(QCoreApplication.translate("GMX_GUI", u"MD Server", None))
        self.Select_all_MD_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Select all", None))
        self.Cler_all_MD_Server_list.setText(QCoreApplication.translate("GMX_GUI", u"Clear all", None))
        self.Config_list.setItemText(self.Config_list.indexOf(self.Server_list_Seting), QCoreApplication.translate("GMX_GUI", u"Calculation server selection", None))
        self.Seting_Tab.setTabText(self.Seting_Tab.indexOf(self.Run_Step_Interface), QCoreApplication.translate("GMX_GUI", u"Run steps", None))
        self.Run_Command_Button.setText(QCoreApplication.translate("GMX_GUI", u"Run", None))
        self.Seting_Tab.setTabText(self.Seting_Tab.indexOf(self.run_command), QCoreApplication.translate("GMX_GUI", u"Run Command", None))
        self.pushButton.setText(QCoreApplication.translate("GMX_GUI", u"Load summary of results", None))
        self.pushButton_2.setText(QCoreApplication.translate("GMX_GUI", u"Rerun the results analysis", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("GMX_GUI", u"Overview", None))
        self.Seting_Tab.setTabText(self.Seting_Tab.indexOf(self.Result_Summary), QCoreApplication.translate("GMX_GUI", u"Result Summary", None))
        self.folder_tree_collapse.setText(QCoreApplication.translate("GMX_GUI", u"Collapse All", None))
        self.Clear_Selection.setText(QCoreApplication.translate("GMX_GUI", u"Clear All Selections", None))
        self.Refresh_Button.setText(QCoreApplication.translate("GMX_GUI", u"refrash", None))
        self.Clear_Log_Button.setText(QCoreApplication.translate("GMX_GUI", u"Clear Log", None))
        self.menubar_file.setTitle(QCoreApplication.translate("GMX_GUI", u"File", None))
        self.menubar_config.setTitle(QCoreApplication.translate("GMX_GUI", u"Config", None))
        self.menubar_info.setTitle(QCoreApplication.translate("GMX_GUI", u"Info", None))
    # retranslateUi

