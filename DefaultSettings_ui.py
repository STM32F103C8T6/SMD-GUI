# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'DefaultSettings.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFrame, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QScrollArea,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)

class Ui_Default_Settings(object):
    def setupUi(self, Default_Settings):
        if not Default_Settings.objectName():
            Default_Settings.setObjectName(u"Default_Settings")
        Default_Settings.resize(908, 547)
        self.verticalLayout = QVBoxLayout(Default_Settings)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tabWidget = QTabWidget(Default_Settings)
        self.tabWidget.setObjectName(u"tabWidget")
        self.Parameter_Setting = QWidget()
        self.Parameter_Setting.setObjectName(u"Parameter_Setting")
        self.tabWidget.addTab(self.Parameter_Setting, "")
        self.PATH_Edit = QWidget()
        self.PATH_Edit.setObjectName(u"PATH_Edit")
        self.verticalLayout_2 = QVBoxLayout(self.PATH_Edit)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.scrollArea = QScrollArea(self.PATH_Edit)
        self.scrollArea.setObjectName(u"scrollArea")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QWidget()
        self.scrollAreaWidgetContents.setObjectName(u"scrollAreaWidgetContents")
        self.scrollAreaWidgetContents.setGeometry(QRect(0, 0, 866, 444))
        self.verticalLayout_3 = QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.Sobtop_PATH_label = QLabel(self.scrollAreaWidgetContents)
        self.Sobtop_PATH_label.setObjectName(u"Sobtop_PATH_label")

        self.horizontalLayout_2.addWidget(self.Sobtop_PATH_label)

        self.Sobtop_PATH = QLineEdit(self.scrollAreaWidgetContents)
        self.Sobtop_PATH.setObjectName(u"Sobtop_PATH")

        self.horizontalLayout_2.addWidget(self.Sobtop_PATH)


        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.CGENFF_Web_URL_label = QLabel(self.scrollAreaWidgetContents)
        self.CGENFF_Web_URL_label.setObjectName(u"CGENFF_Web_URL_label")

        self.horizontalLayout_3.addWidget(self.CGENFF_Web_URL_label)

        self.CGENFF_Web_URL = QLineEdit(self.scrollAreaWidgetContents)
        self.CGENFF_Web_URL.setObjectName(u"CGENFF_Web_URL")

        self.horizontalLayout_3.addWidget(self.CGENFF_Web_URL)


        self.verticalLayout_3.addLayout(self.horizontalLayout_3)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.CGENFF_User_Name_label = QLabel(self.scrollAreaWidgetContents)
        self.CGENFF_User_Name_label.setObjectName(u"CGENFF_User_Name_label")

        self.horizontalLayout_4.addWidget(self.CGENFF_User_Name_label)

        self.CGENFF_User_Name = QLineEdit(self.scrollAreaWidgetContents)
        self.CGENFF_User_Name.setObjectName(u"CGENFF_User_Name")

        self.horizontalLayout_4.addWidget(self.CGENFF_User_Name)


        self.verticalLayout_3.addLayout(self.horizontalLayout_4)

        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.CGENFF_Password_label = QLabel(self.scrollAreaWidgetContents)
        self.CGENFF_Password_label.setObjectName(u"CGENFF_Password_label")

        self.horizontalLayout_5.addWidget(self.CGENFF_Password_label)

        self.CGENFF_Password = QLineEdit(self.scrollAreaWidgetContents)
        self.CGENFF_Password.setObjectName(u"CGENFF_Password")

        self.horizontalLayout_5.addWidget(self.CGENFF_Password)


        self.verticalLayout_3.addLayout(self.horizontalLayout_5)

        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.CGENFF_Proxy_label = QLabel(self.scrollAreaWidgetContents)
        self.CGENFF_Proxy_label.setObjectName(u"CGENFF_Proxy_label")

        self.horizontalLayout_6.addWidget(self.CGENFF_Proxy_label)

        self.CGENFF_Proxy = QLineEdit(self.scrollAreaWidgetContents)
        self.CGENFF_Proxy.setObjectName(u"CGENFF_Proxy")

        self.horizontalLayout_6.addWidget(self.CGENFF_Proxy)


        self.verticalLayout_3.addLayout(self.horizontalLayout_6)

        self.line = QFrame(self.scrollAreaWidgetContents)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.verticalLayout_3.addWidget(self.line)

        self.horizontalLayout_7 = QHBoxLayout()
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.EM_default_mdp_file_path_label = QLabel(self.scrollAreaWidgetContents)
        self.EM_default_mdp_file_path_label.setObjectName(u"EM_default_mdp_file_path_label")

        self.horizontalLayout_7.addWidget(self.EM_default_mdp_file_path_label)

        self.EM_default_mdp_file_path = QLineEdit(self.scrollAreaWidgetContents)
        self.EM_default_mdp_file_path.setObjectName(u"EM_default_mdp_file_path")

        self.horizontalLayout_7.addWidget(self.EM_default_mdp_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_7)

        self.horizontalLayout_8 = QHBoxLayout()
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.NVT_default_mdp_file_path_label = QLabel(self.scrollAreaWidgetContents)
        self.NVT_default_mdp_file_path_label.setObjectName(u"NVT_default_mdp_file_path_label")

        self.horizontalLayout_8.addWidget(self.NVT_default_mdp_file_path_label)

        self.NVT_default_mdp_file_path = QLineEdit(self.scrollAreaWidgetContents)
        self.NVT_default_mdp_file_path.setObjectName(u"NVT_default_mdp_file_path")

        self.horizontalLayout_8.addWidget(self.NVT_default_mdp_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_8)

        self.horizontalLayout_9 = QHBoxLayout()
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.NPT_default_mdp_file_path_label = QLabel(self.scrollAreaWidgetContents)
        self.NPT_default_mdp_file_path_label.setObjectName(u"NPT_default_mdp_file_path_label")

        self.horizontalLayout_9.addWidget(self.NPT_default_mdp_file_path_label)

        self.NPT_default_mdp_file_path = QLineEdit(self.scrollAreaWidgetContents)
        self.NPT_default_mdp_file_path.setObjectName(u"NPT_default_mdp_file_path")

        self.horizontalLayout_9.addWidget(self.NPT_default_mdp_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_9)

        self.horizontalLayout_10 = QHBoxLayout()
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.MD_default_mdp_file_path_label = QLabel(self.scrollAreaWidgetContents)
        self.MD_default_mdp_file_path_label.setObjectName(u"MD_default_mdp_file_path_label")

        self.horizontalLayout_10.addWidget(self.MD_default_mdp_file_path_label)

        self.MD_default_mdp_file_path = QLineEdit(self.scrollAreaWidgetContents)
        self.MD_default_mdp_file_path.setObjectName(u"MD_default_mdp_file_path")

        self.horizontalLayout_10.addWidget(self.MD_default_mdp_file_path)


        self.verticalLayout_3.addLayout(self.horizontalLayout_10)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)

        self.verticalLayout_2.addWidget(self.scrollArea)

        self.tabWidget.addTab(self.PATH_Edit, "")
        self.Server_Setting = QWidget()
        self.Server_Setting.setObjectName(u"Server_Setting")
        self.tabWidget.addTab(self.Server_Setting, "")

        self.verticalLayout.addWidget(self.tabWidget)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setSpacing(9)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(9, 0, 9, 0)
        self.Save_Button = QPushButton(Default_Settings)
        self.Save_Button.setObjectName(u"Save_Button")

        self.horizontalLayout.addWidget(self.Save_Button)

        self.Exit_Button = QPushButton(Default_Settings)
        self.Exit_Button.setObjectName(u"Exit_Button")

        self.horizontalLayout.addWidget(self.Exit_Button)

        self.Return_Button = QPushButton(Default_Settings)
        self.Return_Button.setObjectName(u"Return_Button")

        self.horizontalLayout.addWidget(self.Return_Button)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(Default_Settings)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(Default_Settings)
    # setupUi

    def retranslateUi(self, Default_Settings):
        Default_Settings.setWindowTitle(QCoreApplication.translate("Default_Settings", u"Dialog", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Parameter_Setting), QCoreApplication.translate("Default_Settings", u"GMX Parameter Settings", None))
        self.Sobtop_PATH_label.setText(QCoreApplication.translate("Default_Settings", u"Sobtop PATH:", None))
        self.CGENFF_Web_URL_label.setText(QCoreApplication.translate("Default_Settings", u"CGENFF Web:", None))
        self.CGENFF_User_Name_label.setText(QCoreApplication.translate("Default_Settings", u"CGENFF User Name:", None))
        self.CGENFF_Password_label.setText(QCoreApplication.translate("Default_Settings", u"CGENFF Password:", None))
        self.CGENFF_Proxy_label.setText(QCoreApplication.translate("Default_Settings", u"CGENFF Proxy:", None))
        self.EM_default_mdp_file_path_label.setText(QCoreApplication.translate("Default_Settings", u"EM mdp File PATH:", None))
        self.NVT_default_mdp_file_path_label.setText(QCoreApplication.translate("Default_Settings", u"NVT mdp File PATH:", None))
        self.NPT_default_mdp_file_path_label.setText(QCoreApplication.translate("Default_Settings", u"NPT mdp File PATH:", None))
        self.MD_default_mdp_file_path_label.setText(QCoreApplication.translate("Default_Settings", u"MD mdp File PATH:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.PATH_Edit), QCoreApplication.translate("Default_Settings", u"PATH Settings", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Server_Setting), QCoreApplication.translate("Default_Settings", u"Server Configuration", None))
        self.Save_Button.setText(QCoreApplication.translate("Default_Settings", u"Save", None))
        self.Exit_Button.setText(QCoreApplication.translate("Default_Settings", u"Exit", None))
        self.Return_Button.setText(QCoreApplication.translate("Default_Settings", u"Restore Defaults", None))
    # retranslateUi

