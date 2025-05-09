from PySide6.QtWidgets import QApplication, QFileDialog, QTreeView, QFileSystemModel, QMainWindow, QWidget, QVBoxLayout, QTextEdit, QPushButton, QTabWidget, QHBoxLayout, QListWidgetItem, QTreeWidgetItem
from PySide6.QtCore import QDir, Qt, QRegularExpression, QCoreApplication, QEvent, QStringListModel, QProcess, QThread, Signal, QObject
from PySide6.QtWidgets import QLineEdit, QMenu, QMessageBox, QStyle, QToolTip, QCompleter, QLineEdit, QTextBrowser, QCheckBox, QHeaderView, QComboBox, QGroupBox, QDialog, QLabel, QToolButton
from PySide6.QtGui import QAction, QColor, QTextCursor
from PySide6 import QtCore

import os
import logging
import shutil
import subprocess
import paramiko
from queue import Queue
from datetime import datetime
import re
import concurrent.futures
import time
from tqdm import tqdm
import json
from concurrent.futures import ThreadPoolExecutor, TimeoutError, ProcessPoolExecutor

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options

from SMD_GUI_ui import Ui_GMX_GUI 
from DefaultSettings_ui import Ui_Default_Settings

from SMD_caculate_pull_direction import caculate_pull_direciton


class CommandExecutionThread(QThread):
    progress_signal = Signal(int)
    log_signal = Signal(str, bool)

    def __init__(self, host_name, command, abs_folder_path_list, progress_bar=None, timeout=7200):
        super().__init__()
        self.host_name = host_name
        self.command = command
        self.abs_folder_path_list = abs_folder_path_list
        self.progress_bar = progress_bar
        self.timeout = timeout

    def run(self):
        task_queue = Queue()
        server_info = {'server': servers_lists[self.host_name]}
        for path in self.abs_folder_path_list:
            task_command = f'cd {path} && {self.command}'
            task_queue.put(task_command)

        total_tasks = task_queue.qsize()

        while not task_queue.empty():
            command = task_queue.get()

            try:
                if server_info['server']['host'] == "localhost":
                    # 使用 subprocess 执行本地命令
                    self.run_local_command(command)
                else:
                    # 远程执行命令（使用 SSH）
                    self.run_remote_command(command, server_info)

                # 更新进度条
                completed_tasks = total_tasks - task_queue.qsize()
                progress = (completed_tasks / total_tasks) * 100
                self.progress_signal.emit(int(progress))

            except Exception as e:
                self.log_signal.emit(f"Failed to execute command on {server_info['server']['host']}: {e}", True)
            finally:
                task_queue.task_done()

    def run_local_command(self, command):
        try:
            # 使用 subprocess 执行本地命令
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=self.timeout)

            # 处理标准输出
            if result.stdout:
                self.log_signal.emit(f"Output: {result.stdout}", False)
            if result.stderr:
                self.log_signal.emit(f"Error: {result.stderr}", True)

        except subprocess.TimeoutExpired:
            self.log_signal.emit(f"Command timed out: {command}", True)
        except Exception as e:
            self.log_signal.emit(f"Error executing command '{command}': {e}", True)

    def run_remote_command(self, command, server_info):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(server_info['server']['host'], username=server_info['server']['username'])

            stdin, stdout, stderr = ssh.exec_command(command, timeout=self.timeout)
            output = stdout.read().decode()
            error = stderr.read().decode()

            if error:
                self.log_signal.emit(f"Error from {server_info['server']['host']} for command '{command}':\n{error}", True)
            else:
                self.log_signal.emit(f"Output from {server_info['server']['host']} for command '{command}':\n{output}", False)

            ssh.close()

        except Exception as e:
            self.log_signal.emit(f"Failed to execute command on {server_info['server']['host']}: {e}", True)

    def on_process_finished(self, process, task_queue, total_tasks):
        # 更新进度条
        completed_tasks = total_tasks - task_queue.qsize()
        progress = (completed_tasks / total_tasks) * 100
        self.progress_signal.emit(int(progress))


class CommandLine(QLineEdit):
    def __init__(self, parent=None):
        # 调用父类 QLineEdit 的构造函数，并传递 parent 参数
        super().__init__(parent)
        
    def keyPressEvent(self, event):
        # 阻止 Tab 键的默认行为
        if event.key() == Qt.Key_Tab:
            event.ignore()  # 忽略 Tab 键事件
        else:
            super().keyPressEvent(event)  # 其他按键按默认行为处理

class CustomFileSystemModel(QFileSystemModel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.info_data = {}

    def data(self, index, role=Qt.DisplayRole):
        # 自定义 Info 列 (第 1 列)
        if index.column() == 1 and role == Qt.DisplayRole:
            file_path = self.filePath(index)
            return self.info_data.get(file_path, "")  # 返回 Info 数据
        elif index.column() == 2 and role == Qt.DisplayRole:  # 显示修改日期
            # 获取文件的修改时间
            file_info = self.fileInfo(index)
            return file_info.lastModified().toString("yyyy-MM-dd HH:mm:ss")
        return super().data(index, role)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            headers = ['Name', 'Info', 'Date Modified']
            if section < len(headers):
                return headers[section]
        return super().headerData(section, orientation, role)

    def columnCount(self, parent=None):
        # 只显示三列：Name, Info, Date Modified
        return 3

    def setInfoData(self, file_path, info):
        self.info_data[file_path] = info
        self.dataChanged.emit(self.index(0, 1), self.index(self.rowCount() - 1, 1))  # 更新Info列


class DefaultSettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.ui = Ui_Default_Settings()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):
    def __init__(self, script_path, servers_lists) -> None:
        super().__init__()
        self.script_path = script_path
        self.servers_lists = servers_lists

        # 设置 UI
        self.ui = Ui_GMX_GUI()
        self.ui.setupUi(self)
        # 初始化自定义文件系统模型
        self.model = CustomFileSystemModel()
        self.model.setRootPath(QDir.rootPath())
        # 设置 QTreeView 的模型为过滤代理模型
        self.ui.folder_tree_view.setModel(self.model)
        self.ui.folder_tree_view.doubleClicked.connect(self.open_file_in_tab)
        self.ui.folder_tree_view.setSortingEnabled(True)
        # 设置 QTreeView 为多选模式
        self.ui.folder_tree_view.setSelectionMode(QTreeView.MultiSelection)
        # 连接 QTreeView 的选中变化信号
        self.ui.folder_tree_view.selectionModel().selectionChanged.connect(self.update_selected_count)
        # 连接 QLineEdit 的文本变化信号到筛选方法
        self.ui.Filter_line.textChanged.connect(self.filter_tree)
        # 初始化tab列表
        self.ui.Seting_Tab.setTabsClosable(False)
        self.ui.Seting_Tab.tabCloseRequested.connect(self.close_tab)
        self.default_tab_index = self.ui.Seting_Tab.indexOf(self.ui.run_command)
        # 设置标签页文本
        self.ui.Seting_Tab.setTabText(self.ui.Seting_Tab.indexOf(self.ui.run_command), QCoreApplication.translate("GMX_GUI", u"Run Command", None))
        self.ui.Seting_Tab.setTabText(self.ui.Seting_Tab.indexOf(self.ui.Result_Summary), QCoreApplication.translate("GMX_GUI", u"Result Summary", None))
        # 调整列宽
        self.ui.folder_tree_view.setColumnWidth(0, 200)  # Name
        self.ui.folder_tree_view.setColumnWidth(1, 150)  # Info
        self.ui.folder_tree_view.setColumnWidth(2, 150)  # Date Modified
        # 加载初始文件夹
        try:
            self.current_path = QFileDialog.getExistingDirectory(self, 'Select Working Folder')
        except:
            self.current_path = os.getcwd()
        # print(self.current_path)
        self.load_folder_list(self.current_path)
        self.updata_path_display()
        # 连接 QAction 的信号
        self.ui.actionChange_working_path.triggered.connect(self.change_working_path)
        self.ui.actionDefault_Settings.triggered.connect(self.open_default_settings)
        # 连接按钮点击事件
        self.ui.Refresh_Button.clicked.connect(self.check_folder_file)
        self.ui.folder_tree_collapse.clicked.connect(self.collapse_folder_tree)
        self.ui.Clear_Selection.clicked.connect(self.clear_selection)
        self.ui.Run_Command_Button.clicked.connect(self.on_run_command_button_click)
        self.ui.Clear_Log_Button.clicked.connect(self.clear_log)
        self.ui.Clear_filters_button.clicked.connect(self.clear_filter)
        # self.ui.Command_line = CommandLine(self)
        # 绑定 QLineEdit 的回车键事件
        self.ui.Command_line.returnPressed.connect(self.on_run_command_button_click)
        # 绑定 QLineEdit 的上下键事件
        self.ui.Command_line.installEventFilter(self)
        # 初始化QLineEdit
        # self.ui.Command_line = QLineEdit(self)
        # 创建 QFileSystemModel 用于补全文件路径
        file_system_model = QFileSystemModel()
        file_system_model.setRootPath("")  # 设置为根路径
        # 初始化 QCompleter 并设置模型
        self.completer = QCompleter(file_system_model, self)
        self.ui.Command_line.setCompleter(self.completer)
        # 禁止按 Tab 键切换焦点
        # self.ui.Command_line.setFocusPolicy(QtCore.Qt.NoFocus)
        # 禁止按 Tab 键切换焦点，已通过重写 keyPressEvent 完成
        self.ui.Command_line.setFocusPolicy(QtCore.Qt.StrongFocus)
        # 初始化文件计数
        self.filtered_folders = 0
        self.selected_folders = 0
        self.update_counts()
        self.command_history = []
        self.history_index = -1
        # 初始化下拉菜单
        self.ui.Host_Select_Combo.addItems(self.servers_lists.keys())
        self.ui.folder_tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.ui.folder_tree_view.customContextMenuRequested.connect(self.show_context_menu)
        # 初始化log监视器
        self.ui.Log_Monitor.setReadOnly(True)
        # 初始化进度条
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)
        # 初始化服务器列表选择
        self.Server_list_select_init()
        self.setup_Server_list_button()
        self.setup_confige_link_tree()
        self.update_confige_tree()
        # 初始化运行更多设置按钮
        self.initial_Execute_toolButton()
        self.initial_default_seting()
        self.set_user_seting()

        # self.ui.task_folder_select.addItems(self.ui.Folder_Path_Select_Combo.itemText(i) for i in range(1, self.ui.Folder_Path_Select_Combo.count()))
        self.ui.Folder_Path_Select_Combo.currentTextChanged.connect(self.sync_folder_select_combobox)

        self.ui.Run_Step_Task.clicked.connect(self.run_take)


    def run_take(self):
        """执行运算"""

        # 获取文件夹选择的选项
        folder_select_option = self.ui.task_folder_select.currentText()

        # 获取文件夹路径列表
        folder_list = []
        if folder_select_option.startswith("Total"):
            folder_list = [os.path.join(self.current_path, item) for item in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, item)) and '.' not in item]
            # print(f'total folder: {folder_list}')
        elif folder_select_option.startswith("Filtered"):
            folder_list = self.get_filtered_folders()
            # print(f'filtered folder: {folder_list}')
        elif folder_select_option.startswith("Selected"):
            folder_list = self.get_selected_folders() 
            # print(f'selected folder: {folder_list}')

        # print(f'select EM list: {self.selected_EM_Server}')
        # print(f'select NVT list: {self.selected_NVT_Server}')
        # print(f'select NPT list: {self.selected_NPT_Server}')
        # print(f'select SMD list: {self.selected_SMD_Server}')
        # print(f'select MD list: {self.selected_MD_Server}') 

        run_task = Execute_task(server_info=servers_lists, current_path=self.current_path, folder_list=folder_list, 
                                selected_EM_Server=self.selected_EM_Server, selected_NVT_Server=self.selected_NVT_Server, selected_NPT_Server=self.selected_NPT_Server, selected_MD_Server=self.selected_MD_Server, selected_SMD_Server=self.selected_SMD_Server)

        if self.ui.Auto_Move_File.isChecked():
            if self.ui.Copy_receptor.isChecked():
                receptor_pdb_file_path = self.ui.receptor_file_path.text()
                if os.path.exists(receptor_pdb_file_path):
                    log_info(f'Find receptor file {receptor_pdb_file_path}, start copy...')
                else:
                    log_info(f'Cant find receptor file {receptor_pdb_file_path}, skipping...', error=True)
            else:
                receptor_pdb_file_path = None
            folder_name_index = int(self.ui.folder_name_index.text())
            run_task.move_receptor_pdb_ligand_mol2_makedir(current_path=self.current_path, folder_name_index=folder_name_index, receptor_file_path=receptor_pdb_file_path)


        if self.ui.Rename_Ligane.isChecked():
            ligand_name = self.ui.Ligand_Name.text()
            if len(ligand_name) != 3:
                log_info(f'The name of the ligand should be three letters long, skipping...', error=True)
            else:
                run_task.edit_mol2_file(ligand_name=ligand_name)


        if self.ui.Repair_Receptor.isChecked():
            if self.ui.Repair_missing_side_chain.isChecked():
                run_task.refile_protein()


        if self.ui.Gen_ligand_top.isChecked():
            rename_ligand_name = None
            sob_top_folder_path = self.ui.Sob_top_PATH.text()
            if self.ui.IF_rename_ligand.isChecked():
                rename_ligand_name = self.ui.Rename_ligand_name.text()
            run_task.gen_ligand_top_by_GAFF(Sobtop_PATH = sob_top_folder_path, rename_ligand_name = rename_ligand_name, timeout=60)


        if self.ui.Generate_top_by_CGENFF.isChecked():
            Web_URL = self.ui.CGENFF_web_URL.text()
            User_name = self.ui.CGENFF_user_name.text()
            Pass_Word = self.ui.CGENFF_pw.text()
            if self.ui.IF_use_Proxy.isChecked():
                Web_Proxy = self.ui.Web_Proxy.text()
            else:
                Web_Proxy = None
            run_task.gen_ligand_top_by_CGENFF(web_url=Web_URL, user_name=User_name, user_pw=Pass_Word, web_proxy=Web_Proxy)


        if self.ui.Gen_Protein_top.isChecked():
            force_filed = self.ui.Force_Field_selt.currentText()
            water_model = self.ui.water_model_selt.currentText()
            N_term = self.ui.N_term_selt.currentText()
            C_term = self.ui.C_term_selt.currentText()
            run_task.gen_receptor_top(force_filed=force_filed, water_model=water_model, N_term=N_term, C_term=C_term)


        if self.ui.Morge_complex_gro.isChecked():
            force_filed = self.ui.merge_top_file_ff_selt.currentText()
            run_task.edit_top_file_and_gro_file(force_filed=force_filed)


        if self.ui.Gen_Solvation_box.isChecked():
            Box_shape = self.ui.Box_shape_sele.currentText()
            Box_size_set = float(self.ui.Box_size_set.text())
            run_task.gen_new_box_gro_file(box_sharp=Box_shape, box_size=Box_size_set)
        

        if self.ui.Add_ions_to_box.isChecked():
            add_positive_set = self.ui.add_positive_set.currentText()
            add_negative_set = self.ui.add_negative_set.currentText()
            Salt_density_set = None
            selt_positive_ion = None
            selt_negatibe_ion = None
            if self.ui.Add_salt_density.isChecked():
                Salt_density_set = float(self.ui.Salt_density_set.text())
                selt_positive_ion = self.ui.selt_positive_ion.currentText()
                selt_negatibe_ion = self.ui.selt_negatibe_ion.currentText()
            run_task.Add_ions_to_box(Salt_density_set=Salt_density_set)


        if self.ui.Auto_balance.isChecked():
            ligand_name = self.ui.Ligand_name_set.text()
            run_task.gen_complex_index(ligand_name=ligand_name)

            if self.ui.EM_Seting.isChecked():
                EM_steps = None
                EM_rvdw = None
                EM_extend_rvdw = None
                em_mdp_file_path = None
                if not self.ui.Check_custom_EM_mdp.isChecked():
                    EM_steps = self.ui.EM_steps.text()
                    EM_rvdw = self.ui.EM_rvdw.text()
                    EM_extend_rvdw = self.ui.EM_extend_rvdw.isChecked()
                else:
                    em_mdp_file_path = self.ui.Custom_EM_mdp.text()
                run_task.run_EM(Custom_EM_mdp=em_mdp_file_path, EM_rvdw=EM_rvdw, EM_steps=EM_steps, EM_extend_rvdw=EM_extend_rvdw)
            
            if self.ui.NVT_Seting.isChecked():
                NVT_step = None
                NVT_rvdw = None
                NVT_Tem = None
                NVT_extend_rvdw = None
                NVT_mdp_file = None
                if not self.ui.Check_custum_NVT_file.isChecked():
                    NVT_step = self.ui.NVT_step.text()
                    NVT_rvdw = self.ui.NVT_rvdw.text()
                    NVT_Tem = self.ui.NVT_Tem.text()
                    NVT_extend_rvdw = self.ui.NVT_extend_rvdw.isChecked()
                else:
                    NVT_mdp_file = self.ui.NVT_mdp_file.text()
                run_task.run_nvt(ligand_name=ligand_name, NVT_mdp_file=NVT_mdp_file, NVT_step=NVT_step, NVT_rvdw=NVT_rvdw, NVT_Tem=NVT_Tem, NVT_extend_rvdw=NVT_extend_rvdw)
            
            if self.ui.NPT_Seting.isChecked():
                NPT_Setps = None
                NPT_rvdw = None
                NPT_pres = None
                NPT_mdp_file_path = None
                NPT_extend_rvdw = None
                if not self.ui.Check_NPT_mdp_file.isChecked():
                    NPT_Setps = self.ui.NPT_Setps.text()
                    NPT_rvdw = self.ui.NPT_rvdw.text()
                    NPT_pres = self.ui.NPT_pres.text()
                    NPT_extend_rvdw = self.ui.NPT_extend_rvdw.isChecked()
                else:
                    NPT_mdp_file_path = self.ui.NPT_mdp_file_path.text()
                run_task.run_npt(ligand_name=ligand_name, NPT_mdp_file_path=NPT_mdp_file_path, NPT_Setps=NPT_Setps, NPT_rvdw=NPT_rvdw, NPT_pres=NPT_pres, NPT_extend_rvdw=NPT_extend_rvdw)


        if self.ui.Run_SMD.isChecked():
            SMD_Cycle_numb = int(self.ui.SMD_Cycle_numb.text())
            rm_xtc_file = self.ui.Check_rm_xtc_file.isChecked()
            ligand_name = self.ui.Ligand_name_set_2.text()
            run_task.run_SMD(SMD_Cycle_numb, rm_xtc_file, ligand_name)


        if self.ui.Run_MD.isChecked():
            md_time = self.ui.MD_Time.text()
            MD_Time_Step = self.ui.MD_Time_Step.text()
            Trajectory_Recording = self.ui.Trajectory_Recording.text()
            Energy_Recording = self.ui.Energy_Recording.text()
            MD_Cutoff_Rafius = self.ui.MD_Cutoff_Rafius.text()
            ligand_name = self.ui.Ligand_name_set_3.text
            if self.ui.check_custum_mdp_file.isChecked:
                md_mdp_file_path = self.ui.md_mdp_file_path.text()
            else:
                md_mdp_file_path = None
            run_task.run_MD(ligand_name=ligand_name, md_mdp_file_path=md_mdp_file_path, md_time=md_time, MD_Time_Step=MD_Time_Step, Trajectory_Recording=Trajectory_Recording, Energy_Recording=Energy_Recording, MD_Cutoff_Rafius=MD_Cutoff_Rafius)


    def sync_folder_select_combobox(self):
        self.ui.task_folder_select.clear()
        for i in range(1, self.ui.Folder_Path_Select_Combo.count()):
            self.ui.task_folder_select.addItem(self.ui.Folder_Path_Select_Combo.itemText(i))


    def initial_default_seting(self):
        """初始化软件默认设置"""
        self.ui.Ligand_endswith.setText(default_setting['Ligand_endswith'])
        self.ui.protein_endswith.setText(default_setting['protein_endswith'])
        self.ui.Ligand_Name.setText(default_setting['Ligand_Name'])
        self.ui.Copy_receptor.setChecked(False)
        self.ui.Repair_main_chain.setChecked(False)
        self.ui.Repair_missing_side_chain.setChecked(True)
        self.ui.Generate_top_by_GAFF.setChecked(True)
        self.ui.IF_rename_ligand.setChecked(True)
        self.ui.Rename_ligand_name.setText(default_setting['Ligand_Name'])
        self.ui.Force_Field_selt.clear()
        self.ui.Force_Field_selt.addItems(default_setting['Force_Field'])
        self.ui.Force_Field_selt.setCurrentIndex(0)
        self.ui.water_model_selt.clear()
        self.ui.water_model_selt.addItems(default_setting['water_model'])
        self.ui.water_model_selt.setCurrentIndex(0)
        self.ui.N_term_selt.clear()
        self.ui.N_term_selt.addItems(default_setting['N_term'])
        self.ui.N_term_selt.setCurrentIndex(0)
        self.ui.C_term_selt.clear()
        self.ui.C_term_selt.addItems(default_setting['C_term'])
        self.ui.C_term_selt.setCurrentIndex(0)
        self.ui.merge_top_file_ff_selt.clear()
        self.ui.merge_top_file_ff_selt.addItems(default_setting['Force_Field'])
        self.ui.merge_top_file_ff_selt.setCurrentIndex(0)
        self.ui.Box_shape_sele.clear()
        self.ui.Box_shape_sele.addItems(default_setting['Box_shape'])
        self.ui.Box_shape_sele.setCurrentIndex(0)
        self.ui.Box_size_set.setText(str(default_setting['Box_size']))
        self.ui.add_positive_set.clear()
        self.ui.add_positive_set.addItems(default_setting['Neutralize_positive_ions'])
        self.ui.add_positive_set.setCurrentIndex(0)
        self.ui.add_negative_set.clear()
        self.ui.add_negative_set.addItems(default_setting['Neutralize_negative_ions'])
        self.ui.add_negative_set.setCurrentIndex(0)
        self.ui.Add_salt_density.setChecked(False)
        self.ui.Salt_density_set.setText(str(default_setting['Salt_density']))
        self.ui.selt_positive_ion.clear()
        self.ui.selt_positive_ion.addItems(default_setting['positive_ions'])
        self.ui.selt_positive_ion.setCurrentIndex(0)
        self.ui.selt_negatibe_ion.clear()
        self.ui.selt_negatibe_ion.addItems(default_setting['negative_ions'])
        self.ui.selt_negatibe_ion.setCurrentIndex(0)
        self.ui.Ligand_name_set.setText(default_setting['Ligand_Name'])
        self.ui.Ligand_name_set_2.setText(default_setting['Ligand_Name'])
        self.ui.Ligand_name_set_3.setText(default_setting['Ligand_Name'])
        self.ui.EM_steps.setText(str(default_setting['EM_steps']))
        self.ui.EM_rvdw.setText(str(default_setting['EM_rvdw']))
        self.ui.EM_extend_rvdw.setChecked(True)
        self.ui.Check_custom_EM_mdp.setChecked(False)
        self.ui.NVT_step.setText(str(default_setting['NVT_step']))
        self.ui.NVT_rvdw.setText(str(default_setting['NVT_rvdw']))
        self.ui.NVT_extend_rvdw.setChecked(True)
        self.ui.NVT_Tem.setText(str(default_setting['NVT_Tem']))
        self.ui.Check_custum_NVT_file.setChecked(False)
        self.ui.NPT_Setps.setText(str(default_setting['NPT_Setps']))
        self.ui.NPT_rvdw.setText(str(default_setting['NPT_rvdw']))
        self.ui.NPT_extend_rvdw.setChecked(True)
        self.ui.NPT_pres.setText(str(default_setting['NPT_pres']))
        self.ui.Check_NPT_mdp_file.setChecked(False)
        self.ui.SMD_Cycle_numb.setText(str(default_setting['SMD_Cycle_numb']))
        self.ui.Check_rm_xtc_file.setChecked(True)
        self.ui.MD_Time.setText(str(default_setting['MD_Time']))
        self.ui.MD_Time_Step.setText(str(default_setting['MD_Time_Step']))
        self.ui.Trajectory_Recording.setText(str(default_setting['Trajectory_Recording']))
        self.ui.Energy_Recording.setText(str(default_setting['Energy_Recording']))
        self.ui.Frame_Export.setText(str(default_setting['Frame_Export']))
        self.ui.MD_Cutoff_Rafius.setText(str(default_setting['MD_Cutoff_Rafius']))

    def set_user_seting(self):
        """"初始化用户默认设置"""
        self.ui.Sob_top_PATH.setText(user_setting['Sob_top_PATH'])
        self.ui.CGENFF_web_URL.setText(user_setting['CGENFF_web_URL'])
        self.ui.CGENFF_user_name.setText(user_setting['CGENFF_user_name'])
        self.ui.CGENFF_pw.setText(user_setting['CGENFF_pw'])
        if 'Web_Proxy' in user_setting:
            self.ui.IF_use_Proxy.setChecked(True)
            self.ui.Web_Proxy.setText(user_setting['Web_Proxy'])
        self.ui.Custom_EM_mdp.setText(user_setting['Custom_EM_mdp'])
        self.ui.NVT_mdp_file.setText(user_setting['NVT_mdp_file'])
        self.ui.NPT_mdp_file_path.setText(user_setting['NPT_mdp_file_path'])
        self.ui.md_mdp_file_path.setText(user_setting['md_mdp_file_path'])

    def initial_Execute_toolButton(self):
        tool_menu = QMenu(self)
        Clear_Seleck = tool_menu.addAction("Clear All Seleck")
        Seleck_All = tool_menu.addAction("Select All Defaults")
        defualt_seting = tool_menu.addAction("Load Defualt Setting")
        read_user_seting = tool_menu.addAction("Load User Setting")

        Clear_Seleck.triggered.connect(self.Clear_all_Config_Tree)
        Seleck_All.triggered.connect(self.Seleck_all_Config_Tree)
        defualt_seting.triggered.connect(self.initial_default_seting)
        read_user_seting.triggered.connect(self.set_user_seting)

        # 将菜单设置为按钮的下拉菜单
        self.ui.Execute_toolButton.setMenu(tool_menu)
        self.ui.Execute_toolButton.setPopupMode(QToolButton.InstantPopup)  # 设置按钮的弹出模式

    def Clear_all_Config_Tree(self):
        for groupbox in self.set_groupbox_list:
            groupbox.setChecked(False)

    def Seleck_all_Config_Tree(self):
        for groupbox in self.set_groupbox_list:
            groupbox.setChecked(True)

    def open_default_settings(self):
        """创建并显示默认设置窗口"""
        settings_dialog = DefaultSettingsDialog(self)
        settings_dialog.exec()  


    def setup_confige_link_tree(self):
        self.ui.Config_Tree.setColumnCount(2)
        self.ui.Config_Tree.setHeaderLabels(["Parameter", "Value"])
        total_width = self.ui.Config_Tree.width()
        self.ui.Config_Tree.setColumnWidth(0, int(total_width * 1.5))  # 40% 的宽度
        self.ui.Config_Tree.setColumnWidth(1, int(total_width * 0.4))  # 60% 的宽度

        # header = self.ui.Config_Tree.header()
        # header.setSectionResizeMode(0, QHeaderView.Interactive)
        # header.setSectionResizeMode(1, QHeaderView.Interactive)

        self.set_groupbox_list = [self.ui.Auto_Move_File, self.ui.Rename_Ligane, self.ui.Repair_Receptor, self.ui.Gen_ligand_top, self.ui.Gen_Protein_top, self.ui.Morge_complex_gro, self.ui.Gen_Solvation_box, self.ui.Add_ions_to_box, self.ui.Auto_balance, self.ui.Run_SMD, self.ui.Run_MD, self.ui.Server_Seting]
        # self.set_groupbox_list = [self.ui.Config_Move_File, self.ui.Ligand_protein_prep_Seting, self.ui.Ligand_top_Seting, self.ui.Protein_top_Seting, self.ui.Solvation_box_seting, self.ui.EM_NVT_NPT_seting, self.ui.SMD_MD_Seting, self.ui.Server_list_Seting]
        for groupbox in self.set_groupbox_list:
            groupbox.toggled.connect(self.update_confige_tree)
        
        self.connect_toolbox_signals()
        self.ui.Generate_top_by_GAFF.toggled.connect(self.on_gaff_toggled)
        self.ui.Generate_top_by_CGENFF.toggled.connect(self.on_cgenff_toggled)
        self.ui.Check_custom_EM_mdp.stateChanged.connect(self.toggle_em_lineedits)

        # self.ui.Copy_receptor.toggled.connect(self.update_confige_tree)
        # self.ui.Repair_main_chain.toggled.connect(self.update_confige_tree)
        # self.ui.Repair_missing_side_chain.toggled.connect(self.update_confige_tree)
        # self.ui.Generate_top_by_GAFF.toggled.connect(self.update_confige_tree)
        # self.ui.IF_rename_ligand.toggled.connect(self.update_confige_tree)
        # self.ui.Generate_top_by_CGENFF.toggled.connect(self.update_confige_tree)
        # self.ui.IF_use_Proxy.toggled.connect(self.update_confige_tree)

    # 槽函数定义
    def on_gaff_toggled(self, checked):
        if checked:
            self.ui.Generate_top_by_CGENFF.setChecked(False)

    def on_cgenff_toggled(self, checked):
        if checked:
            self.ui.Generate_top_by_GAFF.setChecked(False)

    def connect_toolbox_signals(self):
        # 遍历 QToolBox 的所有子部件
        for i in range(self.ui.Config_list.count()):
            widget = self.ui.Config_list.widget(i)  # 获取每个页的主 widget
            self.connect_child_signals(widget)

    def toggle_em_lineedits(self, state):
        # 判断是否被勾选
        is_checked = state == Qt.Checked
        
        # 设置 LineEdit 的启用状态（取反逻辑：勾选时禁用，未勾选时启用）
        self.ui.EM_rvdw.setEnabled(not is_checked)
        self.ui.EM_steps.setEnabled(not is_checked)


    def connect_child_signals(self, parent_widget):
        # 查找所有子对象
        for child in parent_widget.findChildren(QObject):  
            if isinstance(child, QLineEdit):  # 处理 QLineEdit
                child.textChanged.connect(self.update_confige_tree)
            elif isinstance(child, QComboBox):  # 处理 QComboBox
                child.currentIndexChanged.connect(self.update_confige_tree)
            elif isinstance(child, QCheckBox):  # 处理 QCheckBox
                child.toggled.connect(self.update_confige_tree)
            elif isinstance(child, QGroupBox):  # 处理 QGroupBox
                child.toggled.connect(self.update_confige_tree)


    def update_confige_tree(self):
        self.ui.Config_Tree.clear()
        for groupbox in self.set_groupbox_list:
            if groupbox.isChecked():
                groupbox_obj_name = groupbox.objectName()
                group_item = QTreeWidgetItem(self.ui.Config_Tree)
                group_item.setText(0, groupbox.title())

                if groupbox_obj_name == 'Auto_Move_File':
                    param_item_1 = QTreeWidgetItem(group_item)
                    param_item_1.setText(0, self.ui.Ligand_endswith_label.text())
                    param_item_1.setText(1, self.ui.Ligand_endswith.text())
                    if self.ui.Copy_receptor.isChecked():
                        param_item_2 = QTreeWidgetItem(group_item)
                        param_item_2.setText(0, self.ui.receptor_file_path_label.text())
                        param_item_2.setText(1, self.ui.receptor_file_path.text())
                        self.ui.receptor_file_path.setEnabled(True)
                    else:
                        param_item_2 = QTreeWidgetItem(group_item)
                        param_item_2.setText(0, self.ui.protein_endswith_label.text())
                        param_item_2.setText(1, self.ui.protein_endswith.text())
                        self.ui.receptor_file_path.setEnabled(False)

                if groupbox_obj_name == 'Rename_Ligane':
                    param_item_3 = QTreeWidgetItem(group_item)
                    param_item_3.setText(0, self.ui.Ligand_Name_label.text())
                    param_item_3.setText(1, self.ui.Ligand_Name.text())

                if groupbox_obj_name == 'Repair_Receptor':
                    if self.ui.Repair_main_chain.isChecked():
                        param_item_4 = QTreeWidgetItem(group_item)
                        param_item_4.setText(0, self.ui.Repair_main_chain.text())
                        param_item_4.setText(1, 'True')
                    if self.ui.Repair_missing_side_chain.isChecked():
                        param_item_5 = QTreeWidgetItem(group_item)
                        param_item_5.setText(0, self.ui.Repair_missing_side_chain.text())
                        param_item_5.setText(1, 'True')

                if groupbox_obj_name == 'Gen_ligand_top':
                    if self.ui.Generate_top_by_GAFF.isChecked():
                        param_item_6 = QTreeWidgetItem(group_item)
                        param_item_6.setText(0, self.ui.Sob_top_PATH_label.text())
                        param_item_6.setText(1, self.ui.Sob_top_PATH.text())
                        if self.ui.IF_rename_ligand.isChecked():
                            param_item_7 = QTreeWidgetItem(group_item)
                            param_item_7.setText(0, self.ui.IF_rename_ligand.text())
                            param_item_7.setText(1, self.ui.Rename_ligand_name.text())
                    elif self.ui.Generate_top_by_CGENFF.isChecked():
                        param_item_8 = QTreeWidgetItem(group_item)
                        param_item_8.setText(0, self.ui.CGENFF_user_name_abel.text())
                        param_item_8.setText(1, self.ui.CGENFF_user_name.text())
                        param_item_9 = QTreeWidgetItem(group_item)
                        param_item_9.setText(0, self.ui.CGENFF_pw_label.text())
                        param_item_9.setText(1, self.ui.CGENFF_pw.text())
                        if self.ui.IF_use_Proxy.isChecked():
                            param_item_10 = QTreeWidgetItem(group_item)
                            param_item_10.setText(0, self.ui.IF_use_Proxy.text())
                            param_item_10.setText(1, self.ui.Web_Proxy.text())

                if groupbox_obj_name == 'Gen_Protein_top':
                    param_item_11 = QTreeWidgetItem(group_item)
                    param_item_11.setText(0, self.ui.Force_Field_selt_label.text())
                    param_item_11.setText(1, self.ui.Force_Field_selt.currentText())
                    param_item_12 = QTreeWidgetItem(group_item)
                    param_item_12.setText(0, self.ui.water_model_selt_label.text())
                    param_item_12.setText(1, self.ui.water_model_selt.currentText())
                    param_item_13 = QTreeWidgetItem(group_item)
                    param_item_13.setText(0, self.ui.N_term_selt_label.text())
                    param_item_13.setText(1, self.ui.N_term_selt.currentText())
                    param_item_14 = QTreeWidgetItem(group_item)
                    param_item_14.setText(0, self.ui.C_term_selt_label.text())
                    param_item_14.setText(1, self.ui.C_term_selt.currentText())

                if groupbox_obj_name == 'Morge_complex_gro':
                    param_item_15 = QTreeWidgetItem(group_item)
                    param_item_15.setText(0, self.ui.merge_top_file_ff_selt_label.text())
                    param_item_15.setText(1, self.ui.merge_top_file_ff_selt.currentText())

                if groupbox_obj_name == 'Gen_Solvation_box':
                    param_item_16 = QTreeWidgetItem(group_item)
                    param_item_16.setText(0, self.ui.Box_shape_sele_label.text())
                    param_item_16.setText(1, self.ui.Box_shape_sele.currentText())
                    param_item_17 = QTreeWidgetItem(group_item)
                    param_item_17.setText(0, self.ui.Box_size_set_label.text())
                    param_item_17.setText(1, self.ui.Box_size_set.text())

                if groupbox_obj_name == 'Add_ions_to_box':
                    param_item_18 = QTreeWidgetItem(group_item)
                    param_item_18.setText(0, 'Add positive ions')
                    param_item_18.setText(1, self.ui.add_positive_set.currentText())
                    param_item_19 = QTreeWidgetItem(group_item)
                    param_item_19.setText(0, 'Add negative ions')
                    param_item_19.setText(1, self.ui.add_negative_set.currentText())
                    if self.ui.Add_salt_density.isChecked():
                        param_item_20 = QTreeWidgetItem(group_item)
                        param_item_20.setText(0, self.ui.Add_salt_density.objectName())
                        param_item_21 = QTreeWidgetItem(param_item_20)
                        param_item_21.setText(0, self.ui.Salt_density_set_label.text())
                        param_item_21.setText(1, self.ui.Salt_density_set.text())
                        param_item_22 = QTreeWidgetItem(param_item_20)
                        param_item_22.setText(0, self.ui.selt_positive_ion_label.text())
                        param_item_22.setText(1, self.ui.selt_positive_ion.currentText())
                        param_item_23 = QTreeWidgetItem(param_item_20)
                        param_item_23.setText(0, self.ui.selt_negatibe_ion_label.text())
                        param_item_23.setText(1, self.ui.selt_negatibe_ion.currentText())

                if groupbox_obj_name == 'Auto_balance':
                    param_item_24 = QTreeWidgetItem(group_item)
                    param_item_24.setText(0, self.ui.Ligand_name_set_label.text())
                    param_item_24.setText(1, self.ui.Ligand_name_set.text())

                    if self.ui.EM_Seting.isChecked():
                        param_item_25 = QTreeWidgetItem(group_item)
                        param_item_25.setText(0, self.ui.EM_Seting.objectName())
                        if not self.ui.Check_custom_EM_mdp.isChecked():
                            param_item_26 = QTreeWidgetItem(param_item_25)
                            param_item_26.setText(0, self.ui.EM_steps_label.text())
                            param_item_26.setText(1, self.ui.EM_steps.text())
                            param_item_27 = QTreeWidgetItem(param_item_25)
                            param_item_27.setText(0, self.ui.EM_rvdw_label.text())
                            param_item_27.setText(1, self.ui.EM_rvdw.text())
                            if self.ui.EM_extend_rvdw.isChecked():
                                param_item_28 = QTreeWidgetItem(param_item_25)
                                param_item_28.setText(0, self.ui.EM_extend_rvdw.text())
                                param_item_28.setText(1, 'True')
                        else:
                            param_item_28 = QTreeWidgetItem(param_item_25)
                            param_item_28.setText(0, self.ui.Check_custom_EM_mdp.text())
                            param_item_28.setText(1, self.ui.Custom_EM_mdp.text())
                    
                    if self.ui.NVT_Seting.isChecked():
                        param_item_29 = QTreeWidgetItem(group_item)
                        param_item_29.setText(0, self.ui.NVT_Seting.objectName())
                        if not self.ui.Check_custum_NVT_file.isChecked():
                            param_item_30 = QTreeWidgetItem(param_item_29)
                            param_item_30.setText(0, self.ui.NVT_step_label.text())
                            param_item_30.setText(1, self.ui.NVT_step.text())
                            param_item_31 = QTreeWidgetItem(param_item_29)
                            param_item_31.setText(0, self.ui.NVT_rvdw_label.text())
                            param_item_31.setText(1, self.ui.NVT_rvdw.text())
                            param_item_32 = QTreeWidgetItem(param_item_29)
                            param_item_32.setText(0, self.ui.NVT_Tem_label.text())
                            param_item_32.setText(1, self.ui.NVT_Tem.text())
                            if self.ui.NVT_extend_rvdw.isChecked():
                                param_item_33 = QTreeWidgetItem(param_item_29)
                                param_item_33.setText(0, self.ui.NVT_extend_rvdw.text())
                                param_item_33.setText(1, 'True')
                        else:
                            param_item_34 = QTreeWidgetItem(param_item_29)
                            param_item_34.setText(0, self.ui.Check_custum_NVT_file.text())
                            param_item_34.setText(1, self.ui.NVT_mdp_file.text())

                    if self.ui.NPT_Seting.isChecked():
                        param_item_35 = QTreeWidgetItem(group_item)
                        param_item_35.setText(0, self.ui.NPT_Seting.objectName())
                        if not self.ui.Check_NPT_mdp_file.isChecked():
                            param_item_36 = QTreeWidgetItem(param_item_35)
                            param_item_36.setText(0, self.ui.NPT_Setps_labe.text())
                            param_item_36.setText(1, self.ui.NPT_Setps.text())
                            param_item_37 = QTreeWidgetItem(param_item_35)
                            param_item_37.setText(0, self.ui.NPT_rvdw_label.text())
                            param_item_37.setText(1, self.ui.NPT_rvdw.text())
                            param_item_38 = QTreeWidgetItem(param_item_35)
                            param_item_38.setText(0, self.ui.NPT_pres_label.text())
                            param_item_38.setText(1, self.ui.NPT_pres.text())
                            if self.ui.NPT_extend_rvdw.isChecked():
                                param_item_39 = QTreeWidgetItem(param_item_35)
                                param_item_39.setText(0, self.ui.NPT_extend_rvdw.text())
                                param_item_39.setText(1, 'True')
                        else:
                            param_item_40 = QTreeWidgetItem(param_item_35)
                            param_item_40.setText(0, self.ui.Check_NPT_mdp_file.text())
                            param_item_40.setText(1, self.ui.NPT_mdp_file_path.text())

                if groupbox_obj_name == 'Run_SMD':
                    param_item_41 = QTreeWidgetItem(group_item)
                    param_item_41.setText(0, self.ui.SMD_Cycle_numb_label.text())
                    param_item_41.setText(1, self.ui.SMD_Cycle_numb.text())
                    if self.ui.Check_rm_xtc_file.isChecked():
                        param_item_42 = QTreeWidgetItem(group_item)
                        param_item_42.setText(0, self.ui.Check_rm_xtc_file.text())
                        param_item_42.setText(1, 'True')
                
                if groupbox_obj_name == 'Run_MD':
                    if not self.ui.check_custum_mdp_file.isChecked():
                        param_item_43 = QTreeWidgetItem(group_item)
                        param_item_43.setText(0, self.ui.MD_Time_label.text())
                        param_item_43.setText(1, self.ui.MD_Time.text())
                        param_item_44 = QTreeWidgetItem(group_item)
                        param_item_44.setText(0, self.ui.MD_Time_Step_label.text())
                        param_item_44.setText(1, self.ui.MD_Time_Step.text())
                        param_item_45 = QTreeWidgetItem(group_item)
                        param_item_45.setText(0, self.ui.Recording_interval.text())
                        param_item_46 = QTreeWidgetItem(param_item_45)
                        param_item_46.setText(0, self.ui.Trajectory_label.text())
                        param_item_46.setText(1, self.ui.Trajectory_Recording.text())
                        param_item_47 = QTreeWidgetItem(param_item_45)
                        param_item_47.setText(0, self.ui.Energy_label.text())
                        param_item_47.setText(1, self.ui.Energy_Recording.text())
                        param_item_48 = QTreeWidgetItem(group_item)
                        param_item_48.setText(0, self.ui.Frame_Export_label.text())
                        param_item_48.setText(1, self.ui.Frame_Export.text())
                        param_item_49 = QTreeWidgetItem(group_item)
                        param_item_49.setText(0, self.ui.MD_Cutoff_Rafius_label.text())
                        param_item_49.setText(1, self.ui.MD_Cutoff_Rafius.text())
                    else:
                        param_item_50 = QTreeWidgetItem(group_item)
                        param_item_50.setText(0, self.ui.check_custum_mdp_file.text())
                        param_item_50.setText(1, self.ui.md_mdp_file_path.text())


                if groupbox_obj_name == 'Server_Seting':

                    self.selected_EM_Server = [item.text() for item in self.ui.EM_Server_Slect_List.findItems("", Qt.MatchContains) if item.checkState() == Qt.Checked]
                    self.selected_NVT_Server = [item.text() for item in self.ui.NVT_Server_Slect_List.findItems("", Qt.MatchContains) if item.checkState() == Qt.Checked]
                    self.selected_NPT_Server = [item.text() for item in self.ui.NPT_Server_Slect_List.findItems("", Qt.MatchContains) if item.checkState() == Qt.Checked]
                    self.selected_SMD_Server = [item.text() for item in self.ui.SMD_Server_Slect_List.findItems("", Qt.MatchContains) if item.checkState() == Qt.Checked]
                    self.selected_MD_Server = [item.text() for item in self.ui.MD_Server_Slect_List.findItems("", Qt.MatchContains) if item.checkState() == Qt.Checked]
                    # print(self.selected_EM_Server)
                    
                    # if self.selected_EM_Server or self.selected_NVT_Server or self.selected_NPT_Server or self.selected_SMD_Server or self.selected_MD_Server:
                    # Server_info_item = QTreeWidgetItem(self.ui.Config_Tree)
                    # Server_info_item.setText(0, self.ui.Server_list_Seting.objectName())
                    # Server_info_item.setText(0, 'Caculation Server selection')
                    if self.selected_EM_Server:
                        param_item_50 = QTreeWidgetItem(group_item)
                        param_item_50.setText(0, self.ui.EM_Server_list.objectName())
                        param_item_50.setText(1, str(len(self.selected_EM_Server)))
                        for item in self.selected_EM_Server:
                            param_item_51 = QTreeWidgetItem(param_item_50)
                            param_item_51.setText(1, str(item))
                    if self.selected_NVT_Server:
                        param_item_52 = QTreeWidgetItem(group_item)
                        param_item_52.setText(0, self.ui.NVT_Server_list.objectName())
                        param_item_52.setText(1, str(len(self.selected_NVT_Server)))
                        for item in self.selected_NVT_Server:
                            param_item_53 = QTreeWidgetItem(param_item_52)
                            param_item_53.setText(1, str(item))
                    if self.selected_NPT_Server:
                        param_item_54 = QTreeWidgetItem(group_item)
                        param_item_54.setText(0, self.ui.NPT_Server_list.objectName())
                        param_item_54.setText(1, str(len(self.selected_NPT_Server)))
                        for item in self.selected_NPT_Server:
                            param_item_55 = QTreeWidgetItem(param_item_54)
                            param_item_55.setText(1, str(item))
                    if self.selected_SMD_Server:
                        param_item_56 = QTreeWidgetItem(group_item)
                        param_item_56.setText(0, self.ui.SMD_Server_list.objectName())
                        param_item_56.setText(1, str(len(self.selected_SMD_Server)))
                        for item in self.selected_SMD_Server:
                            param_item_57 = QTreeWidgetItem(param_item_56)
                            param_item_57.setText(1, str(item))
                    if self.selected_MD_Server:
                        param_item_58 = QTreeWidgetItem(group_item)
                        param_item_58.setText(0, self.ui.MD_Server_list.objectName())
                        param_item_58.setText(1, str(len(self.selected_MD_Server)))
                        for item in self.selected_MD_Server:
                            param_item_59 = QTreeWidgetItem(param_item_58)
                            param_item_59.setText(1, str(item))

        self.ui.Config_Tree.expandAll()


    def setup_Server_list_button(self):
        self.ui.Select_all_EM_Server.clicked.connect(lambda: self.select_all_items(self.ui.EM_Server_Slect_List))
        self.ui.Clear_all_EM_Server.clicked.connect(lambda: self.deselect_all_items(self.ui.EM_Server_Slect_List))

        self.ui.Select_all_NVT_Server.clicked.connect(lambda: self.select_all_items(self.ui.NVT_Server_Slect_List))
        self.ui.Clear_all_NVT_Server.clicked.connect(lambda: self.deselect_all_items(self.ui.NVT_Server_Slect_List))

        self.ui.Select_all_NPT_Server_list.clicked.connect(lambda: self.select_all_items(self.ui.NPT_Server_Slect_List))
        self.ui.Clear_all_NPT_Server_list.clicked.connect(lambda: self.deselect_all_items(self.ui.NPT_Server_Slect_List))

        self.ui.Select_all_SMD_Server_list.clicked.connect(lambda: self.select_all_items(self.ui.SMD_Server_Slect_List))
        self.ui.Clear_all_SMD_Server_list.clicked.connect(lambda: self.deselect_all_items(self.ui.SMD_Server_Slect_List))

        self.ui.Select_all_MD_Server_list.clicked.connect(lambda: self.select_all_items(self.ui.MD_Server_Slect_List))
        self.ui.Cler_all_MD_Server_list.clicked.connect(lambda: self.deselect_all_items(self.ui.MD_Server_Slect_List))


    def select_all_items(self, list_widget):
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setCheckState(Qt.Checked)


    def deselect_all_items(self, list_widget):
        for index in range(list_widget.count()):
            item = list_widget.item(index)
            item.setCheckState(Qt.Unchecked)


    def Server_list_select_init(self):
        for list in [self.ui.EM_Server_Slect_List, self.ui.NVT_Server_Slect_List, self.ui.NPT_Server_Slect_List, self.ui.SMD_Server_Slect_List, self.ui.MD_Server_Slect_List]:
            for Server_name in servers_lists.keys():
                item = QListWidgetItem(Server_name)
                item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                item.setCheckState(Qt.Unchecked)
                list.addItem(item)
            if list.count() > 0:  # 确保列表不为空
                first_item = list.item(0)
                first_item.setCheckState(Qt.Checked)
            list.itemChanged.connect(self.update_confige_tree)

    def clear_filter(self):
        self.ui.Filter_line.clear()


    def updata_path_display(self):
        self.ui.path_display.setText(f"Current PATH: {self.current_path}")


    def update_progress(self, progress_value):
        """ 更新进度条 """
        current_value = self.ui.progressBar.value()
        self.ui.progressBar.setValue(current_value + progress_value)


    def display_log(self, message, is_error=False):
        """ 更新日志框 """
        if is_error:
            self.ui.Log_Monitor.append(f"<font color='red'>{message}</font>")
        else:
            self.ui.Log_Monitor.append(message)


    def clear_log(self):
        # 清空 Log_Monitor 中的所有日志内容
        self.ui.Log_Monitor.clear()


    def update_log(self, info, error=False):
        """更新log监视, 如果是错误信息, 设置为红色, 否则是默认颜色"""
        if error:
            info = f'<font color="red">{info}</font>'
            logging.error(info)
        else:
            info = f'<font color="black">{info}</font>'
            logging.info(info)

        self.ui.Log_Monitor.append(info)
        # 保证显示最新日志
        self.ui.Log_Monitor.verticalScrollBar().setValue(self.ui.Log_Monitor.verticalScrollBar().maximum())


    def update_command_completer(self, text):
        # 如果文本框为空，则不进行补全
        if not text:
            return
        # 调用终端命令查找补全选项
        # 这里只是一个简单示例，使用"compgen"命令来列出所有的命令
        result = self.get_command_completions(text)
        # 创建并更新QCompleter的模型
        model = QStringListModel(result)
        self.completer.setModel(model)


    def get_command_completions(self, text):
        # 检查 compgen 是否可用
        if not shutil.which('compgen'):
            logging.error("Error: 'compgen' command not found.")
            return []
        
        try:
            result = subprocess.run(
                ['compgen', '-c', text], 
                capture_output=True, 
                text=True,
                shell=True
            )
            return result.stdout.splitlines()
        except Exception as e:
            logging.error(f"Error: {e}")
            return []

    def show_context_menu(self, point):
        """右键菜单"""
        # 获取右键点击位置的索引
        index = self.ui.folder_tree_view.indexAt(point)
        if index.isValid():
            # 创建右键菜单
            context_menu = QMenu(self)
            delete_action = QAction("Delete", self)
            context_menu.addAction(delete_action)
            # 创建显示文件大小操作
            show_size_action = QAction("Show File Size", self)
            context_menu.addAction(show_size_action)
            # 连接右键点击菜单的删除操作
            delete_action.triggered.connect(lambda: self.delete_selected_folders(index))
            # 连接显示文件大小操作
            show_size_action.triggered.connect(lambda: self.show_file_size(index))
            # 显示菜单
            context_menu.exec(self.ui.folder_tree_view.mapToGlobal(point))

    def show_file_size(self, index):
        # 获取文件或文件夹的路径
        file_path = self.ui.folder_tree_view.model().filePath(index)
        
        # 检查是否是文件夹
        if os.path.isdir(file_path):
            size = self.get_folder_size(file_path)
            size_message = f"Folder Size: {self.format_size(size)}"
        else:
            size = os.path.getsize(file_path)
            size_message = f"File Size: {self.format_size(size)}"
        
        # 显示文件/文件夹大小信息
        QMessageBox.information(self, "File Size", size_message)

    def format_size(self, size_in_bytes):
        # 自动转换文件大小为更易读的单位
        for unit in ['bytes', 'KB', 'MB', 'GB', 'TB']:
            if size_in_bytes < 1024.0:
                return f"{size_in_bytes:.2f} {unit}"
            size_in_bytes /= 1024.0
        return f"{size_in_bytes:.2f} PB"  # 对于超过TB的文件，返回PB

    def get_folder_size(self, folder_path):
        total_size = 0
        for dirpath, dirnames, filenames in os.walk(folder_path):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
        return total_size


    def delete_selected_folders(self, index):
        # 获取选中的文件夹列表
        selected_indexes = self.ui.folder_tree_view.selectionModel().selectedIndexes()
        
        # 获取选中文件夹或文件的路径
        paths_to_delete = [self.ui.folder_tree_view.model().filePath(idx) for idx in selected_indexes]
        
        # 弹出确认对话框
        reply = QMessageBox.question(self, "Delete Folders",
                                     f"Are you sure you want to delete {int(len(paths_to_delete)/3)} folder(s)?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            for path in paths_to_delete:
                try:
                    if os.path.isdir(path):  # 如果是目录
                        shutil.rmtree(path)  # 删除目录及其内容
                        print(f"Deleted folder: {path}")
                    elif os.path.isfile(path):  # 如果是文件
                        os.remove(path)  # 删除文件
                        print(f"Deleted file: {path}")
                except Exception as e:
                    print(f"Failed to delete {path}: {e}")
            # 刷新文件夹树视图，删除后的条目将消失
            self.refrash_folder_list()


    def refrash_folder_list(self):
        model = self.ui.folder_tree_view.model()
        model.layoutChanged.emit()  # 触发布局更新


    def update_folder_tree_view(self, error_folder_path):
        # 获取文件模型和根目录索引
        model = self.ui.folder_tree_view.model()
        root_index = model.index(self.current_path)

        # 提取错误文件夹的父目录路径
        # error_folder_path = os.path.dirname(error_file_path)

        for row in range(model.rowCount(root_index)):
            child_index = model.index(row, 0, root_index)
            folder_path = model.filePath(child_index)
            # 检查当前文件夹是否为错误文件所在的文件夹
            if folder_path == error_folder_path:
                self.model.setInfoData(folder_path,  " Error⚠️ ")
                self.ui.folder_tree_view.viewport().update()
                break  # 找到对应文件夹后退出循环


    def eventFilter(self, obj, event):
        # 检查事件是否发生在 Command_line 上
        if obj == self.ui.Command_line:
            if event.type() == QEvent.KeyPress:
                if event.key() == Qt.Key_Up:
                    # 向上箭头 - 浏览历史记录
                    if self.command_history and self.history_index < len(self.command_history) - 1:
                        self.history_index += 1
                        self.ui.Command_line.setText(self.command_history[-(self.history_index + 1)])
                
                elif event.key() == Qt.Key_Down:
                    # 向下箭头 - 浏览历史记录
                    if self.history_index > 0:
                        self.history_index -= 1
                        self.ui.Command_line.setText(self.command_history[-(self.history_index + 1)])
                    else:
                        self.history_index = -1
                        self.ui.Command_line.clear()

        # 继续处理其他事件
        return super().eventFilter(obj, event)


    def on_run_command_button_click(self):
        # 获取选择的host
        selected_host = self.ui.Host_Select_Combo.currentText()
        # 获取命令行中的命令
        command = self.ui.Command_line.text()
        # 获取文件夹选择的选项
        folder_select_option = self.ui.Folder_Path_Select_Combo.currentText()

        folder_list = []
        if folder_select_option == "Current Path":
            folder_list = [self.current_path]
        elif folder_select_option.startswith("Total"):
            folder_list = [os.path.join(self.current_path, item) for item in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, item)) and '.' not in item]
        elif folder_select_option.startswith("Filtered"):
            folder_list = self.get_filtered_folders()
        elif folder_select_option.startswith("Selected"):
            folder_list = self.get_selected_folders()

        if not self.command_history or self.command_history[-1] != command:
            self.command_history.append(command)
        self.history_index = -1
        self.ui.Command_line.clear()

        # 创建并启动执行命令的线程
        self.execution_thread = CommandExecutionThread(selected_host, command, folder_list, progress_bar=self.ui.progressBar, timeout=14400)
        
        # 连接信号
        self.execution_thread.progress_signal.connect(self.ui.progressBar.setValue)
        self.execution_thread.log_signal.connect(self.update_log)

        # 启动线程
        self.execution_thread.start()

    # def update_log(self, log_message):
    #     self.ui.logTextBrowser.append(log_message)




    def get_filtered_folders(self):
        # 获取 QTreeView 的模型和根索引
        model = self.ui.folder_tree_view.model()
        root_index = self.ui.folder_tree_view.rootIndex()
        
        # 获取当前显示的所有子项（第0列为文件夹名）
        folder_count = model.rowCount(root_index)
        
        # 遍历所有子项，检查是否可见，并拼接成绝对路径
        filtered_folders = []
        for row in range(folder_count):
            child_index = model.index(row, 0, root_index)
            
            # 确保当前项是可见的
            if not self.ui.folder_tree_view.isRowHidden(row, root_index):
                # 获取文件夹的名称并拼接绝对路径
                folder_name = model.data(child_index, Qt.DisplayRole)
                if model.isDir(child_index):  # 确保是文件夹
                    folder_path = os.path.join(self.current_path, folder_name)
                    filtered_folders.append(folder_path)
        return filtered_folders


    def get_selected_folders(self):
        # 返回选中的文件夹列表
        selected_folders = []
        selected_indexes = self.ui.folder_tree_view.selectionModel().selectedIndexes()
        model = self.ui.folder_tree_view.model()
        
        for index in selected_indexes:
            if model.isDir(index):
                item_path = model.filePath(index)  # 获取完整路径
                selected_folders.append(item_path)
        # 移除重复项并保持顺序（如果多列被选中会导致重复）
        return list(set(selected_folders))


    def update_Folder_Path_Select_Combo(self):
        self.ui.Folder_Path_Select_Combo.clear()
        self.ui.Folder_Path_Select_Combo.addItem("Current Path")
        self.ui.Folder_Path_Select_Combo.addItem(f"Total: {self.total_folders}")
        self.ui.Folder_Path_Select_Combo.addItem(f"Filtered: {self.filtered_folders}")
        self.ui.Folder_Path_Select_Combo.addItem(f"Selected: {self.selected_folders}")

        self.sync_folder_select_combobox()

    def clear_selection(self):
        self.ui.folder_tree_view.clearSelection()

    def update_selected_count(self):
        self.update_counts()

    def update_counts(self):
        # 获取当前选中的文件夹数量
        # self.selected_folders = int(len(self.ui.folder_tree_view.selectionModel().selectedIndexes()) /3)
        # self.selected_folders = int(len(item for item in self.ui.folder_tree_view.selectionModel().selectedColumns() if os.path.isdir(os.path.join(self.current_path, item)))/3)
        selected_indexes = self.ui.folder_tree_view.selectionModel().selectedIndexes()
        self.selected_folders = int(sum(1 for index in selected_indexes if os.path.isdir(os.path.join(self.current_path, index.data())))/2)

        # 如果没有传入总文件夹和过滤后的文件夹数，默认从模型中获取
        self.total_folders = len([item for item in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, item))])
        if not self.filtered_folders:
            self.filtered_folders = self.total_folders
        # 更新 QLabel 显示的信息
        self.ui.select_numb_count.setText(f"Total: {self.total_folders} Filtered: {self.filtered_folders} Selected: {self.selected_folders}")
        previous_selection_prefix = self.ui.Folder_Path_Select_Combo.currentText().split(' ')[0]
        self.update_Folder_Path_Select_Combo()
        self.restore_previous_selection(previous_selection_prefix)


    def restore_previous_selection(self, prefix):
        # 遍历 ComboBox 选项，查找以 prefix 开头的选项
        found_index = -1
        for i in range(self.ui.Folder_Path_Select_Combo.count()):
            item_text = self.ui.Folder_Path_Select_Combo.itemText(i)
            if item_text.startswith(prefix):
                found_index = i
                break
        # 如果找到了匹配的选项，则设置为当前选项
        if found_index != -1:
            self.ui.Folder_Path_Select_Combo.setCurrentIndex(found_index)
        else:
            # 如果没有找到匹配项，默认选择第一个选项
            self.ui.Folder_Path_Select_Combo.setCurrentIndex(0)


    def filter_tree(self):
        # 获取 QLineEdit 的输入文本
        filter_text = self.ui.Filter_line.text()
        # 获取当前根目录的 QModelIndex
        root_index = self.model.index(self.current_path)
        # 过滤树视图的文件夹
        self.filter_items(root_index, filter_text)

    def filter_items(self, index, filter_text):
        # 递归地遍历所有文件夹项并进行过滤
        if not index.isValid():
            return
        total_folders = 0
        filtered_folders = 0
        filtered_filder_list = []
        model = self.ui.folder_tree_view.model()
        for row in range(model.rowCount(index)):
            child_index = model.index(row, 0, index)
            item_name = model.data(child_index, Qt.DisplayRole)

            info_index = model.index(row, 1, index)
            item_info = model.data(info_index, Qt.DisplayRole)

            # 判断是否为文件夹
            if model.isDir(child_index):
                total_folders += 1
                # 判断文件夹名称是否包含过滤文本
                if filter_text.lower() in item_name.lower():
                    self.ui.folder_tree_view.setRowHidden(row, index, False)  # 显示匹配的文件夹
                    filtered_folders += 1
                    filtered_filder_list.append(item_name)
                elif filter_text.lower() in item_info.lower():
                    self.ui.folder_tree_view.setRowHidden(row, index, False)  # 显示匹配的文件夹
                    filtered_folders += 1
                else:
                    self.ui.folder_tree_view.setRowHidden(row, index, True)  # 隐藏不匹配的文件夹
        # 更新文件夹数量
        self.filtered_folder_list = filtered_filder_list
        self.filtered_folders = filtered_folders
        self.update_counts()


    def open_file_in_tab(self, index):
        file_path = self.model.filePath(index)
        if not os.path.isfile(file_path):
            model = self.ui.folder_tree_view.model()
            folder_path = model.filePath(index)
            
            # 获取目录中所有符合日期时间格式的日志文件
            error_log_files = [
                f for f in os.listdir(folder_path)
                if f.endswith('_error.log') and f[:15].isdigit()
            ]
            
            # 如果存在多个日志文件，按日期时间排序，打开最新的
            if error_log_files:
                latest_log_file = sorted(error_log_files)[-1]  # 取最新的日志文件
                file_path = os.path.join(folder_path, latest_log_file)
                
                # with open(latest_log_path, 'r') as log_file:
                #     log_content = log_file.read()
                
                # # 在新的标签页中显示日志内容
                # self.ui.tabWidget.addTab(QTextEdit(log_content), os.path.basename(latest_log_file))
        # 检查文件类型是否支持
        supported_extensions = ['.txt', '.py', '.log', '.gro', '.itp', '.top']
        if not any(file_path.endswith(ext) for ext in supported_extensions):
            return
        # 获取相对路径（相对于当前加载的根目录）
        root_path = self.model.rootPath()
        relative_path = os.path.relpath(file_path, self.current_path)
        # 检查文件是否已打开
        for i in range(self.ui.Seting_Tab.count()):
            if self.ui.Seting_Tab.tabText(i) == os.path.basename(file_path):
                self.ui.Seting_Tab.setCurrentIndex(i)
                return
        # 创建新的标签页
        tab = QWidget()
        layout = QVBoxLayout(tab)

        # 创建按钮容器和布局
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)  # 去掉内边距
        # 添加保存按钮
        save_button = QPushButton()
        save_button.setIcon(self.style().standardIcon(QStyle.SP_DialogSaveButton))
        save_button.setFixedSize(220, 20)
        save_button.setStyleSheet("margin-right: 5px;")
        button_layout.addWidget(save_button)
        save_button.clicked.connect(lambda: self.save_file(file_path, text_edit))
        # 添加关闭按钮
        close_button = QPushButton()
        close_button.setIcon(self.style().standardIcon(QStyle.SP_DialogCloseButton))
        close_button.setFixedSize(220, 20)
        close_button.setStyleSheet("margin-left: 5px;")
        close_button.clicked.connect(lambda: self.close_tab(self.ui.Seting_Tab.indexOf(tab)))
        button_layout.addWidget(close_button)
        layout.addWidget(button_container)

        text_edit = QTextEdit()
        layout.addWidget(text_edit)
        # 读取文件内容
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                text_edit.setPlainText(file.read())
        except Exception as e:
            log_info(f"Error reading file: {e}", error=True)
            return
        # 添加新标签到 Tab Widget
        tab_index = self.ui.Seting_Tab.addTab(tab, relative_path)
        self.ui.Seting_Tab.setCurrentIndex(tab_index)

    def save_file(self, file_path, text_edit):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(text_edit.toPlainText())
            log_info(f"File '{file_path}' saved successfully.")
        except Exception as e:
            log_info(f"Error saving file: {e}", error=True)

    def close_tab(self, index):
        if index != self.default_tab_index:
            self.ui.Seting_Tab.removeTab(index)

    def check_folder_file(self):
        for folder in [item for item in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, item))]:
            folder_path = os.path.join(self.current_path, folder)
            status = self.check_prep_status(folder_path)
            self.model.setInfoData(folder_path, status)
        self.ui.folder_tree_view.viewport().update()

    def check_prep_status(self, check_file_path):
        file_check_list = {
            'lig_fix.mol2': 'lack MOL.top',
            'MOL.top': 'lack lig.itp',
            'lig.itp': 'lack lig.gro',
            'lig.gro': 'lack receptor.gro',
            'receptor.gro': 'lack complex.gro',
            'complex.gro': 'lack newbox.gro',
            'newbox.gro': 'lack solv.gro',
            'solv.gro': 'lack ions.tpr',
            'ions.tpr': 'lack index.ndx',
            'index.ndx': 'lack solv_ions.gro',
            'solv_ions.gro': 'lack EM',
            'em.gro': 'lack NVT',
            'nvt.gro':'lack NPT',
            'npt.gro':'npt finished'
        }
        try:
            if os.path.exists(os.path.join(check_file_path, 'npt.gro')):
                smd_task_list = [item.split('.')[0] for item in os.listdir(check_file_path) if item.startswith('pull') and item.endswith('.mdp')]
                finished_task_list = [item.split('.')[0] for item in os.listdir(check_file_path) if item.startswith('pull') and item.endswith('.gro')]
                
                total_tasks = len(smd_task_list)
                unfinished_tasks = [task for task in smd_task_list if task not in finished_task_list]
                finished_count = total_tasks - len(unfinished_tasks)
                return f"Total: {total_tasks}, Finished: {finished_count}"
                # return f"Total: {total_tasks}, Finished: {finished_count}, Unfinished: {len(unfinished_tasks)}"

            # 逆序遍历，找到第一个存在的文件状态
            for filename, status in reversed(file_check_list.items()):
                file_path = os.path.join(check_file_path, filename)
                if os.path.exists(file_path):
                    return status
            return f"Lack: {list(file_check_list.keys())[0]}"  # 如果所有文件都缺失
        except Exception as e:
            return f"Error: {str(e)}"

    def load_folder_list(self, folder_path):
        # 将文件夹路径转换为 QModelIndex，并设置为 QTreeView 的根目录
        index = self.model.index(folder_path)
        self.ui.folder_tree_view.setRootIndex(index)

    def change_working_path(self):
        """更改工作根目录"""
        folder_path = QFileDialog.getExistingDirectory(self, 'Select Folder')
        if folder_path:
            self.load_folder_list(folder_path)
        self.current_path = folder_path
        self.updata_path_display()
        self.update_counts()


    def collapse_folder_tree(self):
        # 获取根索引
        root_index = self.ui.folder_tree_view.rootIndex()
        # 递归折叠所有展开的文件夹
        self._collapse_recursive(root_index)

    def _collapse_recursive(self, index):
        if not index.isValid():
            return
        # 折叠当前索引
        self.ui.folder_tree_view.collapse(index)
        # 遍历子项并递归折叠
        model = self.ui.folder_tree_view.model()
        for row in range(model.rowCount(index)):
            child_index = model.index(row, 0, index)
            self._collapse_recursive(child_index)


def run_command(host_name, command, abs_folder_path_list=[], progress_callback=None, log_callback=None, timeout=7200):
    task_queue = Queue()
    server_info = {'server': servers_lists[host_name]}
    for path in abs_folder_path_list:
        task_command = f'cd {path} && {command}'
        task_queue.put(task_command)
    
    # 调用QProcess执行命令
    execute_command_with_qprocess(server_info, task_queue, progress_callback=progress_callback, log_callback=log_callback, timeout=timeout)

def execute_command_with_qprocess(server_info, task_queue, progress_callback=None, log_callback=None, timeout=7200, qbar_desc="Executing tasks..."):
    server = server_info['server']
    host = server['host']
    username = server['username']

    total_tasks = task_queue.qsize()
    completed_tasks = 0

    while not task_queue.empty():
        command = task_queue.get()

        try:
            if host == "localhost":
                process = QProcess()
                process.setProgram("bash")
                process.setArguments(["-c", command])
                process.start()
                process.waitForFinished(timeout)
                
                output = process.readAllStandardOutput().data().decode()
                error = process.readAllStandardError().data().decode()
            else:
                # 远程执行命令
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(host, username=username)
                
                stdin, stdout, stderr = ssh.exec_command(command)
                output = stdout.read().decode()
                error = stderr.read().decode()
                ssh.close()

            if error:
                if log_callback:
                    log_callback(f"Error from {host} for command '{command}':\n{error}", error=True)
            else:
                if log_callback:
                    log_callback(f"Output from {host} for command '{command}':\n{output}")

            # 更新进度
            completed_tasks += 1
            progress = int((completed_tasks / total_tasks) * 100)
            if progress_callback:
                progress_callback(progress)

        except Exception as e:
            if log_callback:
                log_callback(f"Failed to execute command on {host}: {e}", error=True)


def log_info(info, error=False, error_folder_path=None):
    if not error:
        logging.info(info)
    else:
        logging.error(info)
    if stats:
        stats.update_log(info, error=error)
        if error_folder_path:
            stats.update_folder_tree_view(error_folder_path=error_folder_path)


def run_command_with_multil_Server(task_command, task_folder_list, processer_servers_list, conda_env=False):
    # 创建任务队列
    task_queue = Queue()
    for folder_path in task_folder_list:
        if conda_env:
            Server_Command = f'source ~/.bashrc && source ~/miniconda3/etc/profile.d/conda.sh && conda activate {conda_env} && cd {folder_path} && {task_command}'
        else:
            Server_Command = f'cd {folder_path} && {task_command}'
        task_queue.put(Server_Command)

    # 解析服务器列表
    servers = [servers_lists[processer_servers_list]] if isinstance(processer_servers_list, str) else [servers_lists[item] for item in processer_servers_list]

    # 初始化进度条
    total_tasks = task_queue.qsize()
    with tqdm(total=total_tasks, desc="Task Progress", unit="task") as progress_bar:
        start_time = time.time()
        
        # 使用 ThreadPoolExecutor 执行任务
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
            futures = []
            for server in servers:
                # 提交每个服务器任务执行
                futures.append(executor.submit(execute_command_with_qprocess, {'server': server}, task_queue))
            
            # 等待所有任务完成
            for future in concurrent.futures.as_completed(futures):
                pass  # 在这里可以检查每个任务的结果，如果需要
        end_time = time.time()
    # logging.info(f"Successful execution of {task_command}, total time taken {end_time - start_time} s")
    log_info(f"Successful execution of {task_command}, total time taken {end_time - start_time} s")


def read_seting_json():
    global default_setting, user_setting
    with open(Software_Default_json_path, 'r', encoding='utf-8') as file:
        default_setting = json.load(file)
    with open(User_Seting_json_path, 'r', encoding= 'utf-8') as file:
        user_setting = json.load(file)
    

class Execute_task():
    def __init__(self, server_info, folder_list, current_path, selected_EM_Server, selected_NVT_Server, selected_NPT_Server, selected_SMD_Server, selected_MD_Server) -> None:

        self.servers_lists = server_info
        self.folder_list = folder_list
        self.current_path = current_path

        self.ions_mdp_file_path = os.path.join(script_path, 'mdp_file/ions.mdp')
        self.md_mdp_file_path = os.path.join(script_path, 'mdp_file/md.mdp')
        self.em_mdp_file_path = os.path.join(script_path, 'mdp_file/em.mdp')
        self.nvt_mdp_file_path = os.path.join(script_path, 'mdp_file/nvt.mdp')
        self.npt_mdp_file_path = os.path.join(script_path, 'mdp_file/npt.mdp')
        self.pull_mdp_file_path = os.path.join(script_path, 'mdp_file/pull.mdp')

        if selected_EM_Server:
            self.selected_EM_Server = selected_EM_Server
        else:
            self.selected_EM_Server = ['localhost']

        if selected_NVT_Server:
            self.selected_NVT_Server = selected_NVT_Server
        else:
            self.selected_NVT_Server = ['localhost']

        if selected_NPT_Server:
            self.selected_NPT_Server = selected_NPT_Server
        else:
            self.selected_NPT_Server = ['localhost']

        if selected_SMD_Server:
            self.selected_SMD_Server = selected_SMD_Server
        else:
            self.selected_SMD_Server = ['localhost']

        if selected_MD_Server:
            self.selected_MD_Server = selected_MD_Server
        else:
            self.selected_MD_Server = ['localhost']

    def run_command(self, task_queue, server_info, qbar_desc='Task Progress'):
        server = server_info['server']
        host = server['host']
        username = server['username']
        total_tasks = task_queue.qsize()  # 获取队列中的总任务数

    def move_receptor_pdb_ligand_mol2_makedir(self, folder_name_index, receptor_file_path = None):
        """新建任务文件夹， 复制或移动配体受体文件并检查"""

        mol2_file_list = [item for item in os.listdir(self.current_path) if os.path.isfile(os.path.join(self.current_path, item)) and item.endswith('.mol2')]
        protein_file_list = [item for item in os.listdir(self.current_path) if os.path.isfile(os.path.join(self.current_path, item)) and item.endswith('.pdb')]

        if mol2_file_list or protein_file_list or receptor_file_path:
            log_info('start moving pdb files and mol2 files....')
            if mol2_file_list:
                for mol2_file in mol2_file_list:
                    mol2_file_path = os.path.join(self.current_path, mol2_file)
                    folder_name = mol2_file.split('_')[folder_name_index]
                    folder_path = os.path.join(self.current_path, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(mol2_file_path, os.path.join(folder_path, mol2_file))
                    if receptor_file_path:
                        shutil.copy(receptor_file_path, os.path.join(folder_path, os.path.basename(receptor_file_path)))

            if protein_file_list and not receptor_file_path:
                for protein_file in protein_file_list:
                    protein_file_path = os.path.join(self.current_path, protein_file)
                    folder_name = protein_file.split('_')[folder_name_index]
                    folder_path = os.path.join(self.current_path, folder_name)
                    os.makedirs(folder_path, exist_ok=True)
                    shutil.move(protein_file_path, os.path.join(folder_path, protein_file))

            error_folder = []
            folder_list = [item for item in os.listdir(self.current_path) if os.path.isdir(os.path.join(self.current_path, item)) and '.' not in item]
            for folder in folder_list:
                mol2_file_exist = False
                pdb_file_exist = False
                file_list = os.listdir(os.path.join(self.current_path, folder))
                for file in file_list:
                    if str(file).endswith('.mold'):
                        mol2_file_exist = True
                    elif str(file).endswith('.pdb'):
                        pdb_file_exist = True
                    if not mol2_file_exist or not pdb_file_exist:
                        error_folder.append(folder)
            if error_folder:
                log_info('missing file in %s'%error_folder, error=True)
            else:
                log_info('all mol2 file and pdb file has been process!')

    def process_mol2_edit(self, input_file_name, output_file_name, ligand_name):
        edit_hat = False
        edit_libal = False
        edit_tail = False
        with open(input_file_name, 'r') as input_file, open(output_file_name, 'w') as output_file:
            editing_mode = False  # 用于判断是否在编辑部分
            for line in input_file:
                if line.startswith('@<TRIPOS>MOLECULE'):
                    edit_hat = True
                elif line.startswith('@<TRIPOS>ATOM'):
                    edit_libal = True
                elif line.startswith('@<TRIPOS>BOND'):
                    edit_libal = False
                elif line.startswith('@<TRIPOS>UNITY_ATOM_ATTR'):
                    edit_libal = False
                elif line.startswith('@<TRIPOS>SUBSTRUCTURE'):
                    edit_tail = True
                elif edit_hat:
                    line = f'{ligand_name}\n'
                    edit_hat = False
                elif edit_libal:
                    line = line[:53] + f'  1   {ligand_name}       ' + line[69:]
                elif edit_tail:
                    line = f'     1 {ligand_name}         1 GROUP             0       ****    0 ROOT    \n'
                    edit_tail = False
                    output_file.write(line)
                    break
                else:
                    line = line
                output_file.write(line)
        # print('scussed in process %s ...'%input_file_name)
        log_info(f'scussed in process {input_file_name} ...')

    def edit_mol2_file(self, ligand_name):
        folder_list = [item for item in self.folder_list if not os.path.exists(os.path.join(item, 'lig_fix.mol2'))]
        if folder_list:
            qbar = tqdm(folder_list, desc='Editing mol2 files...')
            for folder_path in qbar:
                mol2_file_path = os.path.join(folder_path, 'LIG.mol2')
                out_put_file_path = os.path.join(folder_path, 'lig_fix.mol2')

                # 检查 LIG.mol2 文件是否存在
                if not os.path.exists(mol2_file_path):
                    try:
                        # 确保目录下存在 mol2 文件
                        mol2_files = [item for item in os.listdir(folder_path) if item.endswith('.mol2')]
                        if mol2_files:
                            origin_mol2_file_path = os.path.join(folder_path, mol2_files[0])
                            shutil.copy(origin_mol2_file_path, mol2_file_path)
                        else:
                            log_info(f'No .mol2 file found in {folder_path}', error=True)
                            continue  # 跳过当前文件夹
                    except Exception as e:
                        log_info(f'Error processing file {folder_path}: {e}', error=True)
                        continue

                # 调用编辑函数并捕获异常
                try:
                    self.process_mol2_edit(input_file_name=mol2_file_path, output_file_name=out_put_file_path, ligand_name=ligand_name)
                except Exception as e:
                    log_info(f'Error editing mol2 file in {folder_path}: {e}', error=True)

    def refile_protein(self):
        folder_list = [item for item in self.folder_list if not os.path.exists(os.path.join(item, 'receptor.gro'))]
        if folder_list:
            task_queue = Queue()
            host_name = 'localhost'
            schrodinger_path = os.environ.get('SCHRODINGER')  # 读取环境变量
            if not schrodinger_path:
                log_info("Error: SCHRODINGER environment variable not set.", error=True)
                return

            for folder_path in folder_list:
                receptor_files = [item for item in os.listdir(folder_path) if item.endswith('.pdb')]
                if not receptor_files:
                    log_info(f"No .pdb file found in {folder_path}", error=True)
                    continue  # 跳过当前文件夹

                receptor_file_name = receptor_files[0]
                command = (f'"{schrodinger_path}/utilities/prepwizard" {receptor_file_name} receptor.pdb '
                        f'-fillsidechains -fillloops -assign_all_residues -rehtreat')
                server_command = f'cd "{folder_path}" && {command}'
                task_queue.put(server_command)

            server_info = {'server': self.servers_lists[host_name]}
            execute_command_with_qprocess(server_info=server_info, task_queue=task_queue, progress_bar=None, timeout=300, qbar_desc='Refine Protein...')

    def gen_ligand_top_by_GAFF(self, Sobtop_PATH, rename_ligand_name, timeout):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'lig_fix.mol2')) and not os.path.exists(os.path.join(item, 'MOL.top'))]
        if folder_list:
            for folder_path in tqdm(folder_list, desc='gen ligand top...'):
                mol2_file_path = os.path.join(folder_path, 'lig_fix.mol2')
                command = './sobtop %s <genGAFF.txt> %s.txt'%(mol2_file_path, str(os.path.basename(mol2_file_path)).split('.')[0])
                content = f"""2
                {os.path.join(folder_path, 'MOL.gro')}
                1
                3
                0
                4
                {os.path.join(folder_path, 'MOL.top')}
                {os.path.join(folder_path, 'MOL.itp')}
                0
                """
                with open(os.path.join(Sobtop_PATH, 'genGAFF.txt'), 'w') as genGAFF_file:
                    genGAFF_file.write(content)
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen top file: {os.path.join(folder_path, 'MOL.top')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)

            if rename_ligand_name:
                folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'topol.top'))]
                if folder_list:
                    for folder_path in tqdm(folder_list, desc='edit ligand top...'):
                        ligand_gro_file_path = os.path.join(folder_path, 'LIG.gro')
                        ligand_itp_file_path = os.path.join(folder_path, 'LIG.itp')

                        if not os.path.exists(ligand_itp_file_path):
                            out_put_content = ''
                            with open(os.path.join(folder_path, 'MOL.itp'), 'r') as itp_file:
                                for line in itp_file:
                                    if 'MOL' in line:
                                        line = line.replace('MOL', rename_ligand_name)
                                        out_put_content += line
                                    elif line.startswith('lig_fix'):
                                        line = line.replace('lig_fix', f'{rename_ligand_name}    ')
                                        out_put_content += line
                                    else:
                                        out_put_content += line
                            with open(ligand_itp_file_path, 'w') as out_put_itp_file:
                                out_put_itp_file.write(out_put_content)
                            log_info(f'Successfully write {ligand_itp_file_path}')

                        if not os.path.exists(ligand_gro_file_path):
                            out_put_content = ''
                            with open(os.path.join(folder_path, 'MOL.gro'), 'r') as gro_file:
                                for line in gro_file:
                                    if 'MOL' in line:
                                        line = line.replace('MOL', rename_ligand_name)
                                        out_put_content += line
                                    else:
                                        out_put_content += line
                            with open(ligand_gro_file_path, 'w') as out_put_gro_file:
                                out_put_gro_file.write(out_put_content)
                            log_info(f'Successfully write {ligand_gro_file_path}')

    def get_cgenff_web_file_auto(self, mol2_file_path, out_put_file_path):

        def click_button(button_Xpath):
            wait = WebDriverWait(driver, 30)
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, button_Xpath)))
            driver.execute_script("arguments[0].click();", next_button)

        options = Options()
        edge_service = Service('/usr/bin/msedgedriver')

        if self.web_proxy:
            options.add_argument(f"--proxy-server={self.web_proxy}")

        edge_options = Options()
        edge_options.binary_location = "/usr/bin/microsoft-edge-stable"
        # edge_options.add_argument("--start-maximized")
        # edge_options.add_argument("--remote-debugging-port=9222")
        # edge_options.add_argument("--no-sandbox")
        # edge_options.add_argument("--disable-dev-shm-usage")
        # edge_options.add_argument("--disable-gpu")
        edge_options.add_argument("--disable-images")
        edge_options.add_argument("--headless=new")
        edge_options.add_argument("window-size=1920,1080")


        driver = webdriver.Edge(service=edge_service, options=edge_options)

        driver.get(self.web_url)
        time.sleep(2)
        # print("Page title:", driver.title)
        driver.find_element(By.XPATH, '//*[@id="email"]').send_keys(self.user_name)
        driver.find_element(By.XPATH,'//*[@id="password"]').send_keys(self.user_pw)
        driver.find_element(By.XPATH,'//*[@id="root"]/main/div/div/div/div/div[5]/button').click()

        click_button('//*[@id="root"]/div/div/div/ul[1]/li[2]/div')
        click_button('//*[@id="root"]/div/main/div/div[2]/div[1]/div[1]/button')

        file_input = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div/div[1]/div[1]/input')
        file_input.send_keys(mol2_file_path)

        click_button('/html/body/div[2]/div[3]/div/div[2]/button[2]')
        click_button('//*[@id="root"]/div/main/div/div[1]/div/div[3]/div[2]/button[2]')
        click_button('//*[@id="root"]/div/main/div/div[2]/button[1]')

        time.sleep(5)
        driver.save_screenshot(os.path.join(os.path.dirname(mol2_file_path), 'cgenff_snap_shot.png'))

        all_elements = driver.find_elements(By.XPATH, "//*")
        with open(out_put_file_path,'w') as out_put_file:
            out_put = ''
            for element in all_elements:
                # print(f"Tag: {element.tag_name}, Attributes: {element.get_attribute('outerHTML')}")
                out_put += element.get_attribute('outerHTML')
            out_put_file.write(out_put)
            print('cgenff output has been writed in  %s'%out_put_file_path)

        driver.quit()

    def read_cgenff_logfile(cgenff_log_file_path):
        out_put = ''
        try:
            with open(cgenff_log_file_path, 'r', encoding='utf-8') as logfile:
                read_contain = False
                for line in logfile:
                    line = str(line)
                    if line.startswith('* CHARMM General Force Field (CGenFF) program version 4.0'):
                        read_contain = True
                    elif line.startswith('RETURN'):
                        read_contain = False
                        out_put += line
                        break
                    if read_contain:
                        out_put += line
            if out_put:
                out_put_str_file_path = os.path.join(os.path.dirname(cgenff_log_file_path), 'lig_fix.str')
                with open(out_put_str_file_path, 'w') as str_file:
                    str_file.write(str(out_put))
                log_info('str file has been write sccuces! %s'%out_put_str_file_path)
        except:
            log_info('fail in reading cgenff logfile  %s'%cgenff_log_file_path, error=True)

    def gen_ligand_top_by_CGENFF(self, web_url, user_name, user_pw, web_proxy=None, timeout = 60):

        self.web_url = web_url
        self.user_name = user_name
        self.user_pw = user_pw
        self.web_proxy = web_proxy

        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'lig_fix.mol2')) and not os.path.exists(os.path.join(item, 'cgenff_output.log'))]
        if folder_list:
            log_info('start in preape str file from cgenff webfile...')
            for folder_path in tqdm(folder_list, desc='gen ligand str from web'):
                mol2_file_path = os.path.join(folder_path, 'lig_fix.mol2')
                try:
                    self.get_cgenff_web_file_auto(mol2_file_path, folder_path)
                except:
                    log_info('fail in processing of  %s'%mol2_file_path, error=True)

        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'cgenff_output.log')) and not os.path.exists(os.path.join(item, 'lig_fix.str'))]
        if folder_list:
            log_info('start in read str file from cgenff webfile info...')
            for folder_path in tqdm(folder_list, desc='read ligand str from info log'):
                cgenff_log_file_path = os.path.join(folder_path, 'cgenff_output.log')
                self.read_cgenff_logfile(cgenff_log_file_path)


        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'lig_fix.str')) and not os.path.exists(os.path.join(item, 'lig_ini.pdb'))]
        if folder_list:
            log_info('start in gen ligand pdb file...')
            try:
                gmx_python_path = user_setting['gmx_python_path']
            except:
                gmx_python_path = 'python'
            try:
                charmm_force_file_folder_path = user_setting['charmm_force_file_folder_path']
            except:
                log_info('please specy charmm force file folder path', error=True)
            for folder_path in tqdm(folder_list, desc='gen ligand pdb file'):
                lig_mol2_file_path = os.path.join(folder_path, 'lig_fix.mol2')
                lig_str_file_path = os.path.join(folder_path, 'lig_fix.str')
                command = '%s %s LIG %s %s %s'%(gmx_python_path, os.path.join(script_path, 'cgenff_charmm2gmx_py3_nx2.py'), lig_mol2_file_path, lig_str_file_path, charmm_force_file_folder_path)
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen lig_ini.pdb file: {os.path.join(folder_path, 'lig_ini.pdb')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)

        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'lig_ini.pdb')) and not os.path.exists(os.path.join(item, 'lig.gro'))]
        if folder_list:
            log_info('start in gen ligand gro file...')
            command = 'gmx editconf -f lig_ini.pdb -o lig.gro'
            for folder_path in tqdm(folder_list, desc='gen ligand gro file'):
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen lig.gro file: {os.path.join(folder_path, 'lig.gro')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)

    def gen_receptor_top(self, force_filed, water_model, N_term, C_term, timeout=120):
        folder_list = [item for item in self.folder_list if not os.path.exists(os.path.join(item, 'receptor.gro'))]
        if folder_list:
            for folder_path in tqdm(folder_list, desc='Gen receptor top and gro...'):
                if os.path.exists(os.path.join(folder_path, 'receptor-prep.pdb')):
                    receptor_file_name = 'receptor-prep.pdb'
                else:
                    receptor_file_name = 'receptor.pdb'

                if force_filed == "AMBER14SB_parmbsc1":
                    command = f'echo -e "3\\n" | gmx pdb2gmx -f {receptor_file_name} -o receptor.gro -ter -ignh -ff amber14sb_parmbsc1'
                elif force_filed == "CHARMM all-atom force field":
                    command = f'echo -e "11\\n1\\n0\\n0" | gmx pdb2gmx -f {receptor_file_name} -o receptor.gro -ter -ignh'

                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen receptor.gro file: {os.path.join(folder_path, 'receptor.gro')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)          

    def filter_top_edited_file(folder_list):
        finished_list = []
        for folder_path in folder_list:
            prm_edited = False
            itp_edited = False
            mol_edited = False
            with open(os.path.join(folder_path, 'topol.top'), 'r') as top_file:
                for line in top_file:
                    if line.startswith('#include "lig.prm"'):
                        prm_edited = True
                    elif line.startswith('#include "lig.itp"'):
                        itp_edited = True
                    elif line.startswith('LIG                 1'):
                        mol_edited = True
            if prm_edited and itp_edited and mol_edited:
                finished_list.append(folder_path)
        return [item for item in folder_list if item not in finished_list]

    def edit_top_file_and_gro_file(self, force_filed):
        if force_filed == "AMBER14SB_parmbsc1":
            folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'topol.top'))]
            if folder_list:
                for folder_path in tqdm(folder_list, desc='check top and gro file'):
                    ligand_gro_file_path = os.path.join(folder_path, 'LIG.gro')
                    receptor_gro_file_path = os.path.join(folder_path, 'receptor.gro')
                    complex_gro_fole_path = os.path.join(folder_path, 'complex.gro')
                    topol_file_path = os.path.join(folder_path, 'topol.top')
                    if not os.path.exists(complex_gro_fole_path) and os.path.exists(ligand_gro_file_path) and os.path.exists(receptor_gro_file_path):
                        with open(complex_gro_fole_path, 'w') as out_file , open(ligand_gro_file_path, 'r') as ligand_file, open(receptor_gro_file_path, 'r') as receptor_file:
                            receptor_file_headel = receptor_file.readline()
                            receptor_file_atom_numb = int(receptor_file.readline().strip())
                            ligand_file_headel = ligand_file.readline()
                            ligand_file_atom_numb = int(ligand_file.readline().strip())

                            out_put_content = ''
                            total_atom_numb = receptor_file_atom_numb + ligand_file_atom_numb

                            # out_file.write(receptor_file_headel)
                            # out_file.write('%s\n'%total_atom_numb)
                            out_put_content += receptor_file_headel
                            out_put_content += '%s\n'%total_atom_numb

                            len_receptor_line = 0
                            for line in receptor_file:
                                if not len_receptor_line:
                                    len_receptor_line = len(line)
                                    out_put_content += line
                                else:
                                    if len(line) == len_receptor_line:
                                        # out_file.write(line)
                                        out_put_content += line
                                    else:
                                        receptor_file_tail = line
                            for line in ligand_file:
                                if '1LIG' in line:
                                    # out_file.write(line)
                                    out_put_content += line
                                else:
                                    break
                            out_put_content += receptor_file_tail
                            out_file.write(out_put_content)
                        log_info(f'complex gro file has been writen in {complex_gro_fole_path}')

                    if os.path.exists(topol_file_path):
                        ligand_itp_included = False
                        ligand_autom_included = False
                        with open(topol_file_path, 'r') as top_file:
                            for line in top_file:
                                if line.startswith('#include "LIG.itp"'):
                                    ligand_itp_included = True
                                elif line.startswith('LIG            '):
                                    ligand_autom_included = True
                        
                        if ligand_itp_included and ligand_autom_included:
                            pass
                        else:
                            out_file_path = os.path.join(folder_path, 'top.top')
                            with open(topol_file_path, 'r') as top_file:
                                out_put_content = ''
                                for line in top_file:
                                    if line.startswith('[ moleculetype ]'):
                                        if not ligand_itp_included:
                                            line = '#include "LIG.itp"\n\n[ moleculetype ]\n'
                                            ligand_itp_included = True
                                    elif line.startswith('; Include chain topologies'):
                                        if not ligand_itp_included:
                                            line = '#include "LIG.itp"\n\n; Include chain topologies\n'
                                    out_put_content += line
                                if not ligand_autom_included:
                                    out_put_content += 'LIG                 1\n'
                            with open(out_file_path, 'w') as out_put_file:
                                out_put_file.write(out_put_content)
                            shutil.move(topol_file_path, os.path.join(folder_path, '_topol.top_'))
                            shutil.move(out_file_path, topol_file_path)
                            log_info(f'topol.top file has been edited of {topol_file_path}')

        elif force_filed == "CHARMM all-atom force field":
            folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'topol.top'))]
            folder_list = self.filter_top_edited_file(folder_list)
            for folder_path in tqdm(folder_list, desc='edit topol.top file...'):
                top_file_path = os.path.join(folder_path, 'topol.top')
                out_put_file_path = os.path.join(folder_path, 'topol_edit.top')
                prm_term = '; Include ligand parameters\n#include "lig.prm"\n\n'
                itp_term = '; Include ligand topology\n#include "lig.itp"\n\n'
                try:

                    prcess_prm_edit = True
                    prcess_itp_edit = True
                    prcess_mol_edit = True

                    with open(top_file_path, 'r') as top_file:
                        for line in top_file:
                            if line.startswith('#include "lig.prm"'):
                                prcess_prm_edit = False
                            elif line.startswith('#include "lig.itp"'):
                                prcess_itp_edit = False
                            elif line.startswith('LIG                 1'):
                                prcess_mol_edit = False

                    if prcess_prm_edit or prcess_itp_edit or prcess_mol_edit:
                        with open(top_file_path, 'r') as input_file, open(out_put_file_path, 'w') as output_file:
                            for line in input_file:
                                if line.startswith('[ moleculetype ]'):
                                    if prcess_prm_edit:
                                        line = prm_term + line
                                elif line.startswith('; Include water topology'):
                                    if prcess_itp_edit:
                                        line = itp_term + line
                                elif line.startswith('Protein_chain_A     1'):
                                    if prcess_mol_edit:
                                        line = line + 'LIG                 1\n'
                                else:
                                    line = line
                                output_file.write(line)
                        shutil.move(top_file_path, os.path.join(os.path.dirname(top_file_path), '_topol.top_'))
                        shutil.move(out_put_file_path, top_file_path)
                    else:
                        pass

                    log_info('scucess in edit top file %s'%top_file_path)
                except:
                    log_info('fail in process top file in %s'%folder_path, error=True)

            folder_list  = [item for item in self.folder_list if not os.path.exists(os.path.join(item, 'complex.gro'))]
            if folder_list:
                for folder_path in tqdm(folder_list, desc="gen complex.gro file..."):
                    ligand_gro_file_path = os.path.join(folder_path, 'lig.gro')
                    receptor_gro_file_path = os.path.join(folder_path, 'receptor.gro')
                    complex_gro_fole_path = os.path.join(folder_path, 'complex.gro')
                    if os.path.exists(ligand_gro_file_path) and os.path.exists(receptor_gro_file_path):
                        with open(ligand_gro_file_path, 'r') as lig_file:
                            lig_lines = lig_file.readlines()
                            lig_autom_num = int(lig_lines[1].strip())
                            end_line_num = lig_autom_num + 2
                            lig_autom_list = lig_lines[2: end_line_num]
                            # print(lig_autom_list)

                        with open(receptor_gro_file_path, 'r') as receptor_file:
                            receptor_lines = receptor_file.readlines()
                            receptor_heat = receptor_lines[0]
                            receptor_autom_num = int(receptor_lines[1].strip())
                            end_line_num = receptor_autom_num + 2
                            receptor_autom_list = receptor_lines[2: end_line_num]
                            # print(receptor_autom_list)
                            end_line = receptor_lines[end_line_num]
                            # print(end_line)

                        with open(complex_gro_fole_path, 'w') as output_file:
                            output_file.write(receptor_heat)
                            output_file.write(' ')
                            output_file.write(str(lig_autom_num + receptor_autom_num))
                            output_file.write('\n')
                            for line in receptor_autom_list:
                                output_file.write(line)
                            for line in lig_autom_list:
                                output_file.write(line)
                            output_file.write(end_line)
                            log_info('complex gro file has been writen : %s'%complex_gro_fole_path)
        else:
            log_info(f'error on force filed select : {force_filed}, pleace check!', error=True)

    def gen_new_box_gro_file(self, box_sharp, box_size, timeout=120):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'complex.gro')) and not os.path.exists(os.path.join(item, 'newbox.gro'))]
        if folder_list:
            log_info('start in gen gro box file...')
            command = f'gmx editconf -f complex.gro -o newbox.gro -bt {box_sharp} -d {box_size/10}'
            for folder_path in tqdm(folder_list, desc='gen newbox.gro file...'):
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen newbox.gro file: {os.path.join(folder_path, 'newbox.gro')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)     

        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'newbox.gro')) and not os.path.exists(os.path.join(item, 'solv.gro'))]
        if folder_list:
            log_info('start in gen solv gro box file....')
            command = 'gmx solvate -cp newbox.gro -cs tip4p.gro -p topol.top -o solv.gro'
            for folder_path in tqdm(folder_list, desc='gen solv.gro file...'):
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen solv.gro file: {os.path.join(folder_path, 'solv.gro')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)    

        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'solv.gro')) and not os.path.exists(os.path.join(item, 'index_solv.ndx'))]
        if folder_list:
            log_info('start in gen solv index file...')
            command = 'echo -e "q\n" | gmx make_ndx -f solv.gro -o index_solv.ndx'
            for folder_path in tqdm(folder_list, desc='gen index_solv.ndx file...'):
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen index_solv.ndx file: {os.path.join(folder_path, 'index_solv.ndx')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)    

    def GET_SOL_index(folder_path):
        index_file_path = os.path.join(folder_path, 'index_solv.ndx')
        SOL_index = 0
        with open(index_file_path, 'r') as index:
            for line in index:
                if line.startswith('[ ') and ' ]' in line:
                    if 'SOL' in line:
                        # print(SOL_index)
                        return SOL_index
                    else:
                        SOL_index +=1 

    def Add_ions_to_box(self, Salt_density_set=None, timeout=120):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'solv.gro')) and not os.path.exists(os.path.join(item, 'solv_ions.gro'))]
        if folder_list:
            log_info('start in add ions to box....')
            for folder_path in tqdm(folder_list, desc='add ions...'):
                command = f'gmx grompp -f {self.ions_mdp_file_path} -c solv.gro -p topol.top -o ions.tpr -maxwarn 99 -n index_solv.ndx'
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen ions.tpr file: {os.path.join(folder_path, 'ions.tpr')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)    
            
                SOL_index = self.GET_SOL_index(folder_path)

                if Salt_density_set:
                    command = f'echo -e "{SOL_index}" | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral -conc {Salt_density_set}'
                else:
                    command = f'echo -e "{SOL_index}" | gmx genion -s ions.tpr -o solv_ions.gro -p topol.top -pname NA -nname CL -neutral'
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen solv_ions.gro file: {os.path.join(folder_path, 'solv_ions.gro')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)    

    def GET_LIG_index(folder_path, ligand_name):
        index_file_path = os.path.join(folder_path, 'index_solv.ndx')
        Lig_index = 0
        with open(index_file_path, 'r') as index:
            for line in index:
                if line.startswith('[ '):
                    if line.startswith(f'[ {ligand_name} ]'):
                        return Lig_index
                    else:
                        Lig_index +=1 
                else:
                    pass

    def GET_protein_index(folder_path):
        index_file_path = os.path.join(folder_path, 'index_solv.ndx')
        protein_index = 0
        with open(index_file_path, 'r') as index:
            for line in index:
                if line.startswith('[ '):
                    if line.startswith('[ Protein ]'):
                        return protein_index
                    else:
                        protein_index +=1 
                else:
                    pass

    def gen_complex_index(self, ligand_name, timeout=120):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'solv_ions.gro')) and not os.path.exists(os.path.join(item, 'index.ndx'))]
        if folder_list:
            log_info('start in gen index file ....')
            for folder_path in tqdm(folder_list, desc='gen index...'):
                ligand_index = self.GET_LIG_index(folder_path, ligand_name=ligand_name)
                protein_index = self.GET_protein_index(folder_path)
                command = f'echo -e "{protein_index} | {ligand_index}\\nq\\n" | gmx make_ndx -f solv_ions.gro -o index.ndx'
                try:
                    subprocess.run(command, shell=True, cwd=folder_path, check=True, timeout=timeout)
                    log_info(f"Successfull gen index.ndx file: {os.path.join(folder_path, 'index.ndx')}")
                except subprocess.TimeoutExpired:
                    log_info(f"Command exceeded the timeout of {timeout} seconds and was skipped.", error=True)
                except subprocess.CalledProcessError as e:
                    log_info(f"Command '{command}' failed in {folder_path}: {e}", error=True)    

    def execute_command(self, server_info, task_queue, progress_bar):
        server = server_info['server']
        host = server['host']
        username = server['username']

        while not task_queue.empty():
            command = task_queue.get()  # 从队列获取下一个任务
            
            try:
                if host == 'localhost':
                    # 如果是 localhost，直接本地执行
                    logging.info(f'Localhost process: {command}')
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    output, error = result.stdout, result.stderr
                else:
                    # 对于远程服务器，创建 SSH 客户端并执行命令
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(host, username=username)
                    stdin, stdout, stderr = ssh.exec_command(command)
                    logging.info(f'Form {host} process command: {command}')
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    ssh.close()

                # 处理输出和错误
                if error:
                    logging.error(f"Error from {host} for command '{command}':\n{error}")
                else:
                    logging.info(f"Output from {host} for command '{command}':\n{output}")

            except Exception as e:
                logging.error(f"Failed to execute command on {host}: {e}")
            finally:
                task_queue.task_done()  # 标记任务完成
                progress_bar.update(1)  # 每完成一个任务，更新进度条

    def run_EM(self, Custom_EM_mdp, EM_rvdw, EM_steps, EM_extend_rvdw):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'solv_ions.gro')) and not os.path.exists(os.path.join(item, 'em.gro'))]
        if folder_list:
            if not Custom_EM_mdp:
                command = f'gmx grompp -f {self.em_mdp_file_path} -c solv_ions.gro -p topol.top -o em.tpr -maxwarn 99 && gmx mdrun -deffnm em'
            else:
                command = f'gmx grompp -f {Custom_EM_mdp} -c solv_ions.gro -p topol.top -o em.tpr -maxwarn 99 && gmx mdrun -deffnm em'

            task_queue = Queue()
            for folder_path in folder_list:
                Server_Command = f'cd {folder_path} && {command}'
                task_queue.put(Server_Command)

            servers = [servers_lists[self.selected_EM_Server]] if isinstance(self.selected_EM_Server, str) else [servers_lists[item] for item in self.selected_EM_Server]
            total_tasks = task_queue.qsize()
        
            with tqdm(total=total_tasks, desc="process em...", unit="task") as progress_bar:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
                    futures = [executor.submit(self.execute_command, {'server': server}, task_queue, progress_bar) for server in servers]
                    concurrent.futures.wait(futures)  # 等待所有任务完成

    def gen_nvt_npt_mdp_file(self, folder_path, mdp_file_path, ligand_name, electrostatic_cutoff_range):
        index_file_path = os.path.join(folder_path, 'index.ndx')
        ions_system = False
        with open(index_file_path, 'r') as index:
            for line in index:
                if line.startswith('[ Water_and_ions ]'):
                    ions_system = True
        out_put = ''
        with open(mdp_file_path, 'r') as mdp_file:
            for line in mdp_file:
                if line.startswith('rlist'):
                    line = f'rlist                   = {electrostatic_cutoff_range}\n'
                elif line.startswith('rvdw       '):
                    line = f'rvdw                    = {electrostatic_cutoff_range}\n'
                elif line.startswith('rcoulomb'):
                    line = f'rcoulomb                = {electrostatic_cutoff_range}\n'
                elif line.startswith('tc-grps'):
                    if ions_system:
                        line = f'tc-grps                 = Protein_{ligand_name} Water_and_ions\n'
                    else:
                        line = f'tc-grps                 = non-Water Water\n'
                else:
                    line = line
                out_put += line
        with open(os.path.join(folder_path, os.path.basename(mdp_file_path)), 'w') as output_file:
            output_file.write(out_put)

    def run_nvt(self, ligand_name, NVT_mdp_file, NVT_step, NVT_rvdw, NVT_Tem, NVT_extend_rvdw):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'em.gro')) and not os.path.exists(os.path.join(item, 'nvt.gro'))]
        if folder_list:
            if not NVT_mdp_file:
                command = 'gmx grompp -f nvt.mdp -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 99 && gmx mdrun -deffnm nvt'
            else:
                command = f'gmx grompp -f {NVT_mdp_file} -c em.gro -r em.gro -p topol.top -n index.ndx -o nvt.tpr -maxwarn 99 && gmx mdrun -deffnm nvt'

            task_queue = Queue()
            for folder_path in folder_list:
                if not NVT_mdp_file:
                    self.gen_nvt_npt_mdp_file(folder_path=folder_path, mdp_file_path=self.nvt_mdp_file_path, ligand_name=ligand_name, electrostatic_cutoff_range=NVT_rvdw)
                Server_Command = f'cd {folder_path} && {command}'
                task_queue.put(Server_Command)

            servers = [servers_lists[self.selected_NVT_Server]] if isinstance(self.selected_NVT_Server, str) else [servers_lists[item] for item in self.selected_NVT_Server]
            total_tasks = task_queue.qsize()

            with tqdm(total=total_tasks, desc="process NVT...", unit="task") as progress_bar:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
                    futures = [executor.submit(self.execute_command, {'server': server}, task_queue, progress_bar) for server in servers]
                    concurrent.futures.wait(futures)  # 等待所有任务完成

    def run_npt(self, ligand_name, NPT_mdp_file_path, NPT_Setps, NPT_rvdw, NPT_pres, NPT_extend_rvdw):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'nvt.gro')) and not os.path.exists(os.path.join(item, 'npt.gro'))]
        if folder_list:
            if not NPT_mdp_file_path:
                command = 'gmx grompp -f npt.mdp -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 99 && gmx mdrun -deffnm npt'
            else:
                command = f'gmx grompp -f {NPT_mdp_file_path} -c nvt.gro -t nvt.cpt -r nvt.gro -p topol.top -n index.ndx -o npt.tpr -maxwarn 99 && gmx mdrun -deffnm npt'

            task_queue = Queue()
            for folder_path in folder_list:
                if not NPT_mdp_file_path:
                    self.gen_nvt_npt_mdp_file(folder_path=folder_path, mdp_file_path=self.npt_mdp_file_path, ligand_name=ligand_name, electrostatic_cutoff_range=NPT_rvdw)
                Server_Command = f'cd {folder_path} && {command}'
                task_queue.put(Server_Command)
            
            servers = [servers_lists[self.selected_NPT_Server]] if isinstance(self.selected_NPT_Server, str) else [servers_lists[item] for item in self.selected_NPT_Server]
            total_tasks = task_queue.qsize()

            with tqdm(total=total_tasks, desc="process NPT...", unit="task") as progress_bar:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
                    futures = [executor.submit(self.execute_command, {'server': server}, task_queue, progress_bar) for server in servers]
                    concurrent.futures.wait(futures)  # 等待所有任务完成

    def GET_Protein_LIG_index(self, folder_path):
        index_file_path = os.path.join(folder_path, 'index.ndx')
        Protein_LIG_index = 0
        with open(index_file_path, 'r') as index:
            for line in index:
                if line.startswith('[ ') and ' ]' in line:
                    if 'Protein_' in line:
                        # print(SOL_index)
                        return Protein_LIG_index
                    else:
                        Protein_LIG_index +=1 

    def run_SMD(self, SMD_Cycle_numb, rm_xtc_file, ligand_name, timeout=120):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'npt.gro'))]
        gen_npt_pdb_list = [item for item in folder_list if not os.path.exists(os.path.join(item, 'npt.pdb'))]

        if gen_npt_pdb_list:
            log_info('start in gen npt.pdb....')
            for folder_path in tqdm(gen_npt_pdb_list, desc='gen npt.pdb...'):
                Protein_LIG_index = self.GET_Protein_LIG_index(folder_path)
                command = f'echo -e "{Protein_LIG_index}\\n1\\n0\\n" | gmx trjconv -s npt.tpr -f npt.xtc -o npt_cluster.xtc -n index.ndx -pbc cluster -center && echo -e "{Protein_LIG_index}\\n" |gmx trjconv -s npt.tpr -f npt_cluster.xtc -o npt.pdb -dump 1000000 -n index.ndx'

        gen_pull_mdp_folder_list = [item for item in folder_list if os.path.exists(os.path.join(item, 'npt.pdb'))]
        if gen_pull_mdp_folder_list:
            log_info('start in gen pull.mdp....')
            pbar = tqdm(total=len(gen_pull_mdp_folder_list) * SMD_Cycle_numb, desc='gen pull.mdp...')
            with ProcessPoolExecutor() as executor:
                for folder_path in gen_pull_mdp_folder_list:

                    # 确定从哪个编号开始生成文件
                    continue_numb = next(
                        (i for i in range(100) if not os.path.exists(os.path.join(folder_path, f'pull_{i}.mdp'))),
                        100  # 如果所有 pull 文件都存在，则默认设置为 100
                    )

                    for i in range(SMD_Cycle_numb):
                        numb = i + continue_numb

                        # 检查是否超过最大任务数
                        if  numb < SMD_Cycle_numb:
                            # 提交任务并设置超时时间
                            future = executor.submit(
                                caculate_pull_direciton,
                                mdp_template_file_path=self.pull_mdp_file_path,
                                complex_file_path=os.path.join(folder_path, 'npt.pdb'),
                                ligand_res_name=ligand_name,
                                mdp_file_numb=numb
                            )

                            try:
                                future.result(timeout=timeout)  # 设置超时时间
                            except TimeoutError:
                                print(f"Task timed out for pull_{numb}. Skipping...")

                        pbar.update(1)  # 更新进度条
            pbar.close()

        task_queue = Queue()
        for folder_path in folder_list:
            for i in range(100):
                if os.path.exists(os.path.join(folder_path, f'pull_{i}.mdp')) and not os.path.exists(os.path.join(folder_path, f'pull_{i}.gro')):
                    task_command = f'gmx grompp -f pull_{i}.mdp -p topol.top -c npt.gro -o pull_{i}.tpr -maxwarn 99 -n index.ndx && gmx mdrun -deffnm pull_{i}'
                    if rm_xtc_file:
                        Server_Command = f'cd {folder_path} && {task_command} && rm pull_{i}.xtc'
                    else:
                        Server_Command = f'cd {folder_path} && {task_command}'
                    task_queue.put(Server_Command)

        servers = [servers_lists[self.selected_SMD_Server]] if isinstance(self.selected_SMD_Server, str) else [servers_lists[item] for item in self.selected_SMD_Server]
        total_tasks = task_queue.qsize()

        with tqdm(total=total_tasks, desc="process SMD...", unit="task") as progress_bar:
            with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
                futures = [executor.submit(self.execute_command, {'server': server}, task_queue, progress_bar) for server in servers]
                concurrent.futures.wait(futures)  # 等待所有任务完成

    def run_MD(self, ligand_name, md_mdp_file_path, md_time, MD_Time_Step, Trajectory_Recording, Energy_Recording, MD_Cutoff_Rafius):
        folder_list = [item for item in self.folder_list if os.path.exists(os.path.join(item, 'npt.gro'))]
        if folder_list:
            if not md_mdp_file_path:
                run_seting = ''

                with open(md_mdp_file_path, 'r') as template_file:
                    for line in template_file:
                        if line.startswith('nsteps'):
                            line = 'nsteps                  = %s\n'%int(md_time*500000)
                            run_seting += line
                        else:
                            run_seting += line
                
                for folder_path in folder_list:
                    with open(os.path.join(folder_path, 'md.mdp'), 'w') as mdp_file:
                        mdp_file.write(run_seting)

                command = f'gmx grompp -f md.mdp -c npt.gro -t npt.cpt -p topol.top -o md_0_{md_time}.tpr -n index.ndx && gmx mdrun -deffnm md_0_{md_time}'
            else:
                command = f'gmx grompp -f {md_mdp_file_path} -c npt.gro -t npt.cpt -p topol.top -o md_0_{md_time}.tpr -n index.ndx && gmx mdrun -deffnm md_0_{md_time}'

            task_queue = Queue()
            for folder_path in folder_list:
                Server_Command = f'cd {folder_path} && {command}'
                task_queue.put(Server_Command)
            
            servers = [servers_lists[self.selected_NPT_Server]] if isinstance(self.selected_NPT_Server, str) else [servers_lists[item] for item in self.selected_NPT_Server]
            total_tasks = task_queue.qsize()

            with tqdm(total=total_tasks, desc="process MD...", unit="task") as progress_bar:
                with concurrent.futures.ThreadPoolExecutor(max_workers=len(servers)) as executor:
                    futures = [executor.submit(self.execute_command, {'server': server}, task_queue, progress_bar) for server in servers]
                    concurrent.futures.wait(futures)  # 等待所有任务完成


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    servers_lists = {                                                                                                                       #
        'localhost': {'host': 'localhost', 'username': 'sxc'},                                                                              #
        '2698v3':{'host': '2698v3', 'username': 'sxc'},                                                                                     #
        '2697v3-1':{'host': '2697v3-1', 'username': 'sxc'},                                                                                 #
        '2697v3-2':{'host': '2697v3-2', 'username': 'sxc'},                                                                                 #
        '2680v4-1':{'host': '2680v4-1', 'username': 'sxc'},                                                                                 #
        '2680v4-2':{'host': '2680v4-2', 'username': 'sxc'},                                                                                 #
    }   

    # 获取当前工作目录
    script_path = os.path.dirname(os.path.abspath(__file__))
    User_Seting_json_path = os.path.join(script_path, 'User_Defined.json')
    Software_Default_json_path = os.path.join(script_path, 'Software_Default.json')
    default_setting = {}
    user_setting = {}
    read_seting_json()

    # 创建应用程序实例
    app = QApplication([])

    # 创建主窗口
    stats = MainWindow(script_path, servers_lists)
    stats.show()

    # 进入应用程序主循环
    app.exec()


# 生成受体力场选择部分，charmm还没有完善
# NPT NVT MD 的自定义参数没有生效
