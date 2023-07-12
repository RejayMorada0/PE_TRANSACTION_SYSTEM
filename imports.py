import re
from typing import Counter, Text
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFrame, QLCDNumber, QMessageBox, QTableView, QProgressBar
from PyQt5.QtCore import QTimer, QTime, QPropertyAnimation, QSortFilterProxyModel, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QStandardItem, QStandardItemModel, QStandardItemModel
import sys
from datetime import datetime
import time
from PyQt5.uic.uiparser import ButtonGroup
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import mysql.connector
from mysql.connector import errorcode
from PyQt5.QtSql import QSqlTableModel, QSqlDatabase


#import reportlab for printing receipt
from reportlab.platypus import SimpleDocTemplate, Table, Paragraph, TableStyle 
from reportlab.lib import colors 
from reportlab.lib.pagesizes import A4 
from reportlab.lib.styles import getSampleStyleSheet 

from prettytable import from_db_cursor


list = [ ]

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('design.ui', self)
        self.setWindowTitle("Physical Education Department")
        self.setWindowIcon(QtGui.QIcon('icons/soccer-ball.png'))
        self.show()
        self.stackedWidget.setCurrentIndex(0)
        self.textBrowser.setText("-----------RECEIPT------------")

    #database (connection part)
        self.mydb = mysql.connector.connect(  
            host = "localhost",
            user = "root",
            password = "",
            database = "seconddb")

    #TIME WITH TIMER
        timer = QTimer(self)
        timer.timeout.connect(self.timedisplay)
        timer.start(1000)
        self.timedisplay()
        
    #LOGIN PAGE
        self.label_4.setText("")
        self.pushButton.clicked.connect(self.logins)
        self.lineEdit.returnPressed.connect(self.logins)
        self.pushButton_3.clicked.connect(self.closeEvent1)
    #SHOW PASSWORD/HIDE PASSWORD
        self.pushButton_2.clicked.connect(self.showpassword)
        self.pushButton_9.clicked.connect(self.showpassword1)
        self.pushButton_12.clicked.connect(self.showpassword2)
        self.pushButton_13.clicked.connect(self.showpassword3)

    #CHANGE PASSWORD BUTTONS
        self.label_6.setText("")
        self.pushButton_11.clicked.connect(self.cancel0)
        self.pushButton_10.clicked.connect(self.changepass)
        self.lineEdit_2.returnPressed.connect(self.changepass)
        self.lineEdit_3.returnPressed.connect(self.changepass)
        self.lineEdit_4.returnPressed.connect(self.changepass)

    #NAVBAR BUTTONS
        self.pushButton_4.clicked.connect(self.home)
        self.pushButton_5.clicked.connect(self.uniform)
        self.pushButton_6.clicked.connect(self.equipment)
        self.pushButton_7.clicked.connect(self.facility)
        self.pushButton_8.clicked.connect(self.closeEvent1)

    #HOME PAGE BUTTONS
        self.pushButton_14.clicked.connect(self.changepasswordpage)  

    #UNIFORM PAGE BUTTONS
        self.pushButton_28.clicked.connect(self.changepricespage)
        
    #CHANGE PRICES BUTTONS
        self.pushButton_36.clicked.connect(self.cancel1)

    ###################################

        self.priceTab()
        self.orderTab()
        self.borrowTab()
        self.reserveTab()
        self.receipt = [ ]

        self.lineEdit_6.textChanged.connect(self.searchorderTab)
        self.spinBox_4.valueChanged.connect(self.searchorderTab_2)
        self.pushButton_35.clicked.connect(self.updatePrice)
        self.lineEdit_5.textChanged.connect(self.searchBorrowTab)

        self.comboBox_3.currentTextChanged.connect(self.totalStatus)
        self.comboBox_4.currentTextChanged.connect(self.totalStatus_2)
        self.spinBox.valueChanged.connect(self.totalStatus_3)
        self.spinBox_2.valueChanged.connect(self.totalStatus_4)


        self.pushButton_27.clicked.connect(self.pay)
        self.pushButton_29.clicked.connect(self.generate)
        self.pushButton_26.clicked.connect(self.received)
        #self.pushButton_56.clicked.connect(self.printReceipt)

        self.pushButton_15.clicked.connect(self.borrow)
        self.pushButton_17.clicked.connect(self.returned)

        self.pushButton_32.clicked.connect(self.schedule)
        self.pushButton_30.clicked.connect(self.success)
        self.pushButton_31.clicked.connect(self.cancel)

    ##########################################################################################################



    def executedatabase(self):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM password")
    
    #CLOCK TIMER
    def timedisplay(self):
        now = datetime.now()
        text = now.strftime('%I:%M %p')
        self.label_8.setText(text)
        
    #DEF LOGIN FUNCTIONS
    def logins(self):
        self.executedatabase()
        result = self.mycursor.fetchone()
        a = str(self.lineEdit.text())
        empty = ''
        if a == empty:
            self.label_4.setText("PASSWORD IS REQUIRED!")
            self.label_4.show()
            self.lineEdit.setStyleSheet("QLineEdit {background: transparent;\n"
                                                "border: transparent;\n"
                                                "border-bottom: 1px solid red;\n"
                                                "border-radius: 0px;\n"
                                                "color: rgb(184, 107, 87);\n"
                                                "font: 75 15pt \"MS Shell Dlg 2\";}\n"
                                                "\n"
                                                "QLineEdit::focus {\n"
                                                "    border: none;\n"
                                                "    border-bottom: 1px solid qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                                "}")
            
    
        else:
            for i in result:
                if a!= i:
                    self.label_4.setText("WRONG PASSWORD!")
                    self.label_4.show()
                    self.lineEdit.setStyleSheet("QLineEdit {background: transparent;\n"
                                                "border: transparent;\n"
                                                "border-radius: 0px;\n"
                                                "border-bottom: 1px solid red;\n"
                                                "color: rgb(184, 107, 87);\n"
                                                "font: 75 15pt \"MS Shell Dlg 2\";}\n"
                                                "\n"
                                                "QLineEdit::focus {\n"
                                                "    border: none;\n"
                                                "    border-bottom: 1px solid qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                                "}")
                    
                else:
                    self.label_4.setText("")
                    self.stackedWidget.setCurrentIndex(1)
                    self.stackedWidget_2.setCurrentIndex(0)
                    self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
                    self.lineEdit.setStyleSheet("QLineEdit {background: transparent;\n"
                                                "border: none;\n"
                                                "border-radius: 0px;\n"
                                                "color: rgb(184, 107, 87);\n"
                                                "font: 75 15pt \"MS Shell Dlg 2\";}\n"
                                                "\n"
                                                "QLineEdit::focus {\n"
                                                "    border: none;\n"
                                                "    border-bottom: 1px solid qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                                "}")
                    self.lineEdit.clear()
                    self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
                    icon = QtGui.QIcon()
                    icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                    self.pushButton_2.setIcon(icon)
                    self.pushButton_2.setIconSize(QtCore.QSize(50, 30))
                    self.label_9.setText("")

    #SHOW PASSWORD/HIDE PASSWORD BUTTON FUNCTION
    def showpassword(self):
        hide = QtWidgets.QLineEdit.Password
        shown = QtWidgets.QLineEdit.Normal
        empty = ''

        

        if self.lineEdit.echoMode()==hide and self.lineEdit.text() is not empty:
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/hide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_2.setIcon(icon)
            self.pushButton_2.setIconSize(QtCore.QSize(50, 30))
            self.label_4.setText("")

        elif self.lineEdit.echoMode()==shown and self.lineEdit.text() is not empty:
            self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_2.setIcon(icon)
            self.pushButton_2.setIconSize(QtCore.QSize(50, 30))
            self.label_4.setText("")

        else:
            pass
        
    def showpassword1(self):
        hide = QtWidgets.QLineEdit.Password
        shown = QtWidgets.QLineEdit.Normal
        empty = ''
        
        

        if self.lineEdit_2.echoMode()==hide and self.lineEdit_2.text() is not empty:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/hide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_9.setIcon(icon)
            self.pushButton_9.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        elif self.lineEdit_2.echoMode()==shown and self.lineEdit_2.text() is not empty:
            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_9.setIcon(icon)
            self.pushButton_9.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        else:
            pass
    
    def showpassword2(self):
        hide = QtWidgets.QLineEdit.Password
        shown = QtWidgets.QLineEdit.Normal
        empty = ''
        
        

        if self.lineEdit_3.echoMode()==hide and self.lineEdit_3.text() is not empty:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/hide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_12.setIcon(icon)
            self.pushButton_12.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        elif self.lineEdit_3.echoMode()==shown and self.lineEdit_3.text() is not empty:
            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_12.setIcon(icon)
            self.pushButton_12.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        else:
            pass

    def showpassword3(self):
        hide = QtWidgets.QLineEdit.Password
        shown = QtWidgets.QLineEdit.Normal
        empty = ''
        
        

        if self.lineEdit_4.echoMode()==hide and self.lineEdit_4.text() is not empty:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/hide.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_13.setIcon(icon)
            self.pushButton_13.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        elif self.lineEdit_4.echoMode()==shown and self.lineEdit_4.text() is not empty:
            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
            icon = QtGui.QIcon()
            icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
            self.pushButton_13.setIcon(icon)
            self.pushButton_13.setIconSize(QtCore.QSize(50, 30))
            self.label_6.setText("")

        else:
            pass
              
    #NAVBAR LIPAT PAGE FUNCTIONS
    def home(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(0)
        self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_5.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_6.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_7.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.label_9.setText("")

    def uniform(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(1)
        self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_5.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_6.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_7.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.label_9.setText("PE UNIFORM | ORDERING")

    def equipment(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(2)
        self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_5.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_6.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_7.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
    
        self.label_9.setText("EQUIPMENT CATALOG")

    def facility(self):
        self.stackedWidget.setCurrentIndex(1)
        self.stackedWidget_2.setCurrentIndex(3)
        self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_5.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_6.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.pushButton_7.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
        self.label_9.setText("FACILITY RESERVATION")
    #CHANGE PASSWORD FUNCTIONS
    def changepass(self):
        self.executedatabase()
        empty = ''
        a = str(self.lineEdit_2.text()) #default
        b = str(self.lineEdit_3.text()) #new
        c = str(self.lineEdit_4.text()) #confirm
        result = self.mycursor.fetchone() #password from database

        if a==empty and b==empty and c==empty:
            self.label_6.setText("NO INPUT FOUND")
        

        elif a!=empty and b!=empty and c==empty:
            self.label_6.setText("CONFIRM YOUR PASSWORD!")
            
        
        elif a!=empty and b==empty and c!=empty:
            self.label_6.setText("INPUT YOUR NEW PASSWORD!")
            

        elif a==empty and b!=empty and c!=empty:
            self.label_6.setText("DEFAULT PASSWORD IS REQUIRED TO COMPLETE ACTION.")
            
        elif a!=empty and b==empty and c==empty:
            self.label_6.setText("PLEASE COMPLETE YOUR PROGRESS")
            

        elif a==empty and b!=empty and c==empty:
            self.label_6.setText("DEFAULT PASSWORD IS REQUIRED TO COMPLETE ACTION.")
            

        elif a==empty and b==empty and c!=empty:
            self.label_6.setText("DEFAULT PASSWORD AND NEW PASSWORD IS REQUIRED TO COMPLETE ACTION.")
            
        
        else:
            for i in result:
                if a!= i:
                    self.label_6.setText("PLEASE INPUT DEFAULT PASSWORD!")

                elif a==b:
                    self.label_6.setText("IT WAS YOUR OLD PASSWORD. TRY A NEW ONE!")

                elif b!=c:
                    self.label_6.setText("PASSWORDS DON'T MATCH!")

                elif a!=i and a!=b and b==c:
                    self.label_6.setText("PLEASE INPUT DEFAULT PASSWORD!")

                elif a==i and a==b and b==c:
                    self.label_6.setText("IT WAS YOUR OLD PASSWORD. TRY A NEW ONE!")

                elif a==i and a!=b and b!=c:
                    self.label_6.setText("PASSWORDS DON'T MATCH!")


                else:
                    d = Counter(c)
                    e = sum(d.values())
                    if b!=c:
                        self.label_6.setText("PASSWORDS DON'T MATCH!")
                        

                    elif e<=7:
                        self.label_6.setText("PASSWORDS MUST BE 8 LETTERS LONG!")

                    else:
                        try:
                            sql = "UPDATE password SET idpassword = %s WHERE idpassword = %s"
                            val = (c, i)
                            self.mycursor.execute(sql, val)
                            self.mydb.commit()
                            self.changenotification()
                            self.stackedWidget.setCurrentIndex(0)
                            self.lineEdit_2.clear()
                            self.lineEdit_3.clear()
                            self.lineEdit_4.clear()
                            self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
                            self.lineEdit_3.setEchoMode(QtWidgets.QLineEdit.Password)
                            self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Password)
                            icon = QtGui.QIcon()
                            icon.addPixmap(QtGui.QPixmap("icons/vision.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
                            self.pushButton_9.setIcon(icon)
                            self.pushButton_9.setIconSize(QtCore.QSize(50, 30))
                            self.pushButton_12.setIcon(icon)
                            self.pushButton_12.setIconSize(QtCore.QSize(50, 30))
                            self.pushButton_13.setIcon(icon)
                            self.pushButton_13.setIconSize(QtCore.QSize(50, 30))
                        except mysql.connector.Error as err:
                            print(err)
                    
    def changepasswordpage(self):
        self.stackedWidget.setCurrentIndex(2)

    def changepricespage(self):
        self.stackedWidget.setCurrentIndex(3)

    #MESSAGE BOXES
    def closeWin(self):
        self.closeEvent()
        
    def closeEvent(self, event):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                                "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "QPushButton {border: none;\n"
                                "border-radius: 5px;\n"
                                "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "font: 75 12pt \"MS Shell Dlg 2\";\n"
                                "color: white;\n"
                                "width: 140px;\n"
                                "height: 40px;\n}"
                                "\n"
                                "QPushButton::hover {\n"
                                "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                                "}\n"
                                "\n"
                                "QPushButton::pressed {\n"
                                "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("Quit now?")
        self.msg.setWindowTitle("Logout attempt")
        returnValue = self.msg.exec()
        

        if returnValue == QtWidgets.QMessageBox.Yes:
            app.exit()
        
        else:
            event.ignore()

    def closeEvent1(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                                "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "QPushButton {border: none;\n"
                                "border-radius: 5px;\n"
                                "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "font: 75 12pt \"MS Shell Dlg 2\";\n"
                                "color: white;\n"
                                "width: 140px;\n"
                                "height: 40px;\n}"
                                "\n"
                                "QPushButton::hover {\n"
                                "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                                "}\n"
                                "\n"
                                "QPushButton::pressed {\n"
                                "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("Are you sure you want to exit?")
        self.msg.setWindowTitle("Logout attempt")
        returnValue = self.msg.exec()
        
        if returnValue == QtWidgets.QMessageBox.Yes:
            app.exit()
        
        else:
            return

    def cancel0(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                                "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "QPushButton {border: none;\n"
                                "border-radius: 5px;\n"
                                "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "font: 75 12pt \"MS Shell Dlg 2\";\n"
                                "color: white;\n"
                                "width: 140px;\n"
                                "height: 40px;\n}"
                                "\n"
                                "QPushButton::hover {\n"
                                "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                                "}\n"
                                "\n"
                                "QPushButton::pressed {\n"
                                "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("You haven't finished your process yet. Do you want to leave without finishing?")
        self.msg.setWindowTitle("cancel attempt")
        returnValue = self.msg.exec()
        
        if returnValue == QtWidgets.QMessageBox.Yes:
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_2.setCurrentIndex(0)
            self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_5.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "color: rgb(244, 241, 244);"
                                            "font: 75 12pt 'MS Shell Dlg 2';}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_6.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "color: rgb(244, 241, 244);"
                                            "font: 75 12pt 'MS Shell Dlg 2';}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_7.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "color: rgb(244, 241, 244);"
                                            "font: 75 12pt 'MS Shell Dlg 2';}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.label_9.setText("WELCOME HOME!")
        
        else:
            pass

    def cancel1(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                                "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "QPushButton {border: none;\n"
                                "border-radius: 5px;\n"
                                "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "font: 75 12pt \"MS Shell Dlg 2\";\n"
                                "color: white;\n"
                                "width: 140px;\n"
                                "height: 40px;\n}"
                                "\n"
                                "QPushButton::hover {\n"
                                "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                                "}\n"
                                "\n"
                                "QPushButton::pressed {\n"
                                "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Question)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.Cancel)
        self.msg.setText("You haven't finished your process yet. Do you want to leave without finishing?")
        self.msg.setWindowTitle("cancel attempt")
        returnValue = self.msg.exec()
        
        if returnValue == QtWidgets.QMessageBox.Yes:
            self.stackedWidget.setCurrentIndex(1)
            self.stackedWidget_2.setCurrentIndex(1)
            self.pushButton_4.setStyleSheet("QPushButton {"
                                        "background-color: transparent;"
                                        "color: rgb(244, 241, 244);"
                                        "font: 75 12pt 'MS Shell Dlg 2';}"

                                        "QPushButton::hover {"
                                            "border: 1px solid rgb(244, 241, 244);"
                                            "border-radius: 10px;}"

                                        "QPushButton::pressed {"
                                            "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_5.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_6.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "color: rgb(244, 241, 244);"
                                            "font: 75 12pt 'MS Shell Dlg 2';}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.pushButton_7.setStyleSheet("QPushButton {"
                                            "background-color: transparent;"
                                            "color: rgb(244, 241, 244);"
                                            "font: 75 12pt 'MS Shell Dlg 2';}"

                                            "QPushButton::hover {"
                                                "border: 1px solid rgb(244, 241, 244);"
                                                "border-radius: 10px;}"

                                            "QPushButton::pressed {"
                                                "background-color: rgba(244, 241, 244, 20);}")
            self.label_9.setText("PE UNIFORM | ORDERING")
        
        else:
            return
    
    def changenotification(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                                "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                                "\n"
                                "QPushButton {border: none;\n"
                                "border-radius: 5px;\n"
                                "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "font: 75 12pt \"MS Shell Dlg 2\";\n"
                                "color: white;\n"
                                "width: 140px;\n"
                                "height: 40px;\n}"
                                "\n"
                                "QPushButton::hover {\n"
                                "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                                "}\n"
                                "\n"
                                "QPushButton::pressed {\n"
                                "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                                "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("YOUR PASSWORD HAS BEEN CHANGE. YOU MUST NOW LOG IN FIRST")
        self.msg.setWindowTitle("Notifications")
        self.msg.exec()
    
    def successful(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                    "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                    "\n"
                    "QPushButton {border: none;\n"
                    "border-radius: 5px;\n"
                    "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                    "font: 75 12pt \"MS Shell Dlg 2\";\n"
                    "color: white;\n"
                    "width: 140px;\n"
                    "height: 40px;\n}"
                    "\n"
                    "QPushButton::hover {\n"
                    "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                    "}\n"
                    "\n"
                    "QPushButton::pressed {\n"
                    "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                    "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Information)
        self.msg.setText("PROCESS SUCCESSFULL")
        self.msg.setWindowTitle("INFORMATION")
        self.msg.exec_()

    def nodata(self):
        self.msg = QtWidgets.QMessageBox(self.centralwidget)
        self.msg.setStyleSheet("QFrame {background-color: rgb(244, 241, 244);}\n"
                    "QLabel {color: rgb(157, 92, 101); font: 75 12pt \"MS Shell Dlg 2\";}\n"
                    "\n"
                    "QPushButton {border: none;\n"
                    "border-radius: 5px;\n"
                    "background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                    "font: 75 12pt \"MS Shell Dlg 2\";\n"
                    "color: white;\n"
                    "width: 140px;\n"
                    "height: 40px;\n}"
                    "\n"
                    "QPushButton::hover {\n"
                    "    background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:0, y2:0, stop:0 rgba(120, 62, 115, 255), stop:0.931818 rgba(254, 163, 17, 255));\n"
                    "}\n"
                    "\n"
                    "QPushButton::pressed {\n"
                    "    background-color: qlineargradient(spread:pad, x1:0.051, y1:0, x2:1, y2:1, stop:0 rgba(120, 72, 120, 255), stop:0.931818 rgba(254, 145, 50, 255));\n"
                    "}")
        self.msg.setIcon(QtWidgets.QMessageBox.Warning)
        self.msg.setText("DATA NOT FOUND")
        self.msg.setWindowTitle("INFORMATION")
        self.msg.exec_()

###################################################################

    def priceTab(self):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM pricetab")
        result = self.mycursor.fetchall()
        self.tableWidget_6.clearContents()
        self.tableWidget_6.setRowCount(len(result) - 1)
        row = 0
        for y in range(1,len(result)):
            n = 0
            for x in result[int(y)]:
                if n==0:
                    self.tableWidget_6.setItem(row, 0, QtWidgets.QTableWidgetItem(str(x)))
                else:
                    self.tableWidget_6.setItem(row, 1, QtWidgets.QTableWidgetItem(str(x)))
                n+=1
            row +=1

    def updatePrice(self):
        changeItem = self.comboBox_7.currentText()
        changePrice = self.doubleSpinBox_2.value()
        try:
            self.mycursor = self.mydb.cursor()
            sql = "UPDATE pricetab SET prices = %s WHERE tshirt_size_and_pants_size = %s"
            val = (changePrice, changeItem)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.priceTab()
        except mysql.connector.Error as err:
            print(err)

    def orderTab(self):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM ordertab")
        result = self.mycursor.fetchall()
        self.tableWidget_2.clearContents()
        row = 0  
        self.tableWidget_2.setRowCount(len(result))      
        for i in result:
            self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
            self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i[4])))
            self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i[5])))
            self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i[6])))
            self.tableWidget_2.setItem(row, 7, QtWidgets.QTableWidgetItem(str(i[7])))
            row = row + 1

    def searchorderTab(self):
        a = self.lineEdit_6.text()
        if len(a) != 0:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT * FROM ordertab WHERE studentdetails = %s", (a, ))
            result = self.mycursor.fetchall()
            self.tableWidget_2.clearContents()
            row = 0  
            self.tableWidget_2.setRowCount(len(result))      
            for i in result:
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i[4])))
                self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i[5])))
                self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i[6])))
                self.tableWidget_2.setItem(row, 7, QtWidgets.QTableWidgetItem(str(i[7])))
                row = row + 1

        else:
            self.orderTab()

    def searchorderTab_2(self):
        a = self.spinBox_4.value()
        if (int(a) != 0):
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT * FROM ordertab WHERE ID = %s", (a, ))
            result = self.mycursor.fetchall()
            self.tableWidget_2.clearContents()
            row = 0  
            self.tableWidget_2.setRowCount(len(result))      
            for i in result:
                self.tableWidget_2.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.tableWidget_2.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tableWidget_2.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tableWidget_2.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
                self.tableWidget_2.setItem(row, 4, QtWidgets.QTableWidgetItem(str(i[4])))
                self.tableWidget_2.setItem(row, 5, QtWidgets.QTableWidgetItem(str(i[5])))
                self.tableWidget_2.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i[6])))
                self.tableWidget_2.setItem(row, 7, QtWidgets.QTableWidgetItem(str(i[7])))
                row = row + 1


        else:
            self.orderTab()
        
    def pay(self):
        #preorder details to get to the students
        studentDetail = self.lineEdit_6.text().upper()
        uniCombo = self.comboBox_3.currentText()
        uniSpin = self.spinBox.value()
        pantsCombo = self.comboBox_4.currentText()
        pantsSpin = self.spinBox_2.value()
        stat = "PRE-ORDER"

        if len(studentDetail) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE FILL OUT THE STUDENT DETAILS OR SCAN ID.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif (str(uniCombo)  == "NOT AVAIL") and (str(pantsCombo) == "NOT AVAIL"):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("BOTH NOT AVAIL UNIFORM AND PANTS CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif (float(uniSpin) or float(pantsSpin)) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("AVAIL ATLEAT ONE, BUT 0 QUANTITY CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        
        elif (float(uniSpin) == 0) and (str(uniCombo) != "NOT AVAIL"):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("AVAIL ATLEAT ONE, BUT 0 QUANTITY CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (float(uniSpin) != 0) and (str(uniCombo) == "NOT AVAIL"):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("NOT AVAIL UNIFORM CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (float(pantsSpin) == 0) and (str(pantsCombo) != "NOT AVAIL"):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("AVAIL ATLEAT ONE, BUT 0 QUANTITY CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()

        elif (float(pantsSpin) != 0) and (str(pantsCombo) == "NOT AVAIL"):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("NOT AVAIL PANTS CAN'T PROCEED.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
                         


        else:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT prices FROM pricetab WHERE tshirt_size_and_pants_size = %s", (uniCombo,))
            result = self.mycursor.fetchone()
            res = float(''.join(map(str, result)))
            z = res * uniSpin
            print(z)

            self.mycursor.execute("SELECT prices FROM pricetab WHERE tshirt_size_and_pants_size = %s", (pantsCombo,))
            result_2 = self.mycursor.fetchone()
            res_2 = float(''.join(map(str, result_2)))
            y = res_2 * pantsSpin
            print(y)

            #total price computation
            tp = str(z+y)
            #payment and change computation
            studentCash = self.doubleSpinBox.value()            
            if (studentCash < float(tp)) :
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("ENTER AMOUNT OF MONEY EXACT OR GREATER THAN TO THE TOTAL PRICE.")
                self.msg.setWindowTitle("WARNING!!!")
                self.msg.exec_()
   
            else:
                change = studentCash - (float(tp))
                try:
                    self.textBrowser.setText(
                         "STUDENT DETAILS: " +  str(studentDetail) + "\n" +
                         "TSHIRT - SIZE: " +  str(uniCombo) + "\n" +
                         "TSHIRT - QNTY: " +  str(uniSpin) + "\n" +
                         "PANTS - SIZE: " +  str(pantsCombo) + "\n" +
                         "PANTS - QNTY: " +  str(pantsSpin) + "\n" +
                         "TOTAL PRICE: " +  str(tp) + "\n"  
                         "CHANGE: " + str(change))

                
                    self.receipt.append([ "Date" , "Name", "Quantity", "Price" ])
                    self.receipt.append([str('date'), str(studentDetail), " ", " ", ])
                    self.receipt.append([ " ", str(uniCombo) , str(uniSpin), str(res)]) 
                    self.receipt.append([ " ", str(pantsCombo), str(pantsSpin), str(res_2)]) 
                    self.receipt.append([ "Total", "", "", str(tp)])

                    self.mycursor = self.mydb.cursor()
                    sql = "INSERT INTO ordertab(studentdetails, tssize, tsquantity, pantssize,\
                            pantsquantity, totalprice, status) VALUES(%s,%s,%s,%s,%s,%s,%s);"
                    qwe = (studentDetail, uniCombo, uniSpin, pantsCombo, pantsSpin, tp, stat)
                    self.mycursor.execute(sql,qwe)
                    self.mydb.commit()
                    self.orderTab()
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Information)
                    self.msg.setText("PRE-ORDER SUCCESUL")
                    self.msg.setWindowTitle("INFORMATION")
                    self.msg.exec_()

                except mysql.connector.Error as err:
                    print(err)

    def generate(self):
        stat = "PRE-ORDER"
        stat_2 = "PENDING ORDER"
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Question)
        
        msgBox.setText("ARE YOU REALLY SURE TO RESET AND GENERATE ORDER SUMMARY? \
                        EVERY LIST ON THIS TABLE WILL BE TRANSFER IN PENDING ORDER BATCH.")
        msgBox.setWindowTitle("QUESTION")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)

        returnValue = msgBox.exec()
        if returnValue == QtWidgets.QMessageBox.Ok:
            try:
                fileName, selectedFilter = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', "~", ".txt")
                if fileName:
                    with open(fileName, "w") as file:
                        self.mycursor = self.mydb.cursor()
                        self.mycursor.execute("SELECT ID, studentdetails, tssize, tsquantity, pantssize, pantsquantity, totalprice, status FROM ordertab WHERE status = %s",(stat,))
                        mytable = from_db_cursor(self.mycursor)
                        table_txt = mytable.get_string()
                        file.write(table_txt)

                        self.mycursor = self.mydb.cursor()
                        sql = "UPDATE ordertab SET status = %s WHERE status = %s"
                        val = (stat_2, stat)
                        self.mycursor.execute(sql, val)
                        self.mydb.commit()
                        self.orderTab()
                        self.msg = QtWidgets.QMessageBox(self.centralwidget)
                        self.msg.setIcon(QtWidgets.QMessageBox.Information)
                        self.msg.setText("GENERATE SUMMERY SUCCESSFUL")
                        self.msg.setWindowTitle("INFORMATION")
                        self.msg.exec_()
                else: 
                    pass
                

            except mysql.connector.Error as e:
                print(e)
        else:
            pass

    def received(self):
        a = self.spinBox_4.value()
        statusRec = "RECIEVED ORDER"
        try:
            self.mycursor.execute("SELECT ID, studentdetails FROM ordertab WHERE ID = %s",(a, ))
            result = self.mycursor.fetchall()
            res_2 = str(''.join(map(str, result)))
            if str(a) not in res_2: 
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("UNSUCCESSFULLY RECEIVED THE ORDER.")
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            else:
                self.mycursor = self.mydb.cursor()
                sql = "UPDATE ordertab SET status = %s WHERE ID = %s"
                val = (statusRec, a)
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                self.orderTab() 
                self.spinBox_4.clear() 
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SUCCESSFULLY RECEIVED THE ORDER.")
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()

        except mysql.connector.Error as err:
            print(err)

    def printReceipt(self):
        if len(self.receipt) == 0:
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("SORRY, BUT RECIEPT IS EMPTY")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        else:
            pdf = SimpleDocTemplate( "receipt.pdf" , pagesize = A4 )
            styles = getSampleStyleSheet()
            title_style = styles[ "Heading1" ]
            title_style.alignment = 1
            title = Paragraph( "TUPC PE DEPARTMENT" , title_style )
            style = TableStyle([
                                        ( "BOX" , ( 0, 0 ), ( -1, -1 ), 1 , colors.black ), 
                                        ( "GRID" , ( 0, 0 ), ( 4 , 4 ), 1 , colors.black ), 
                                        ( "BACKGROUND" , ( 0, 0 ), ( 3, 0 ), colors.red ), 
                                        ( "TEXTCOLOR" , ( 0, 0 ), ( -1, 0 ), colors.whitesmoke ), 
                                        ( "ALIGN" , ( 0, 0 ), ( -1, -1 ), "CENTER" ), 
                                        ( "BACKGROUND" , ( 0 , 1 ) , ( -1 , -1 ), colors.beige ),]) 
            table = Table( self.receipt , style = style)
            pdf.build([ title , table ])
            self.receipt.clear()
            self.textBrowser.setText("None")
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("PRINT RECEIPT IS IN THE receipt.pdf.")
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

    def deleteReceived(self):
        statusRec = "RECIEVED ORDER"
        try:
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM ordertab WHERE status = %s "
            adr = (statusRec, )
            self.mycursor.execute(sql, adr)
            self.mydb.commit()
            self.orderTab()
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("SUCCESSFULLY DELETED RECEIVED ORDER.")
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

        except mysql.connector.Error as err:
            print(err)


    def totalStatus(self):
        studentDetail = self.lineEdit_6.text().upper()
        uniCombo = self.comboBox_3.currentText()
        uniSpin = self.spinBox.value()
        pantsCombo = self.comboBox_4.currentText()
        pantsSpin = self.spinBox_2.value()

        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT prices FROM pricetab WHERE tshirt_size_and_pants_size = %s", (uniCombo,))
        result = self.mycursor.fetchone()
        res = float(''.join(map(str, result)))
        z = res * uniSpin
        print(z)

        self.mycursor.execute("SELECT prices FROM pricetab WHERE tshirt_size_and_pants_size = %s", (pantsCombo,))
        result_2 = self.mycursor.fetchone()
        res_2 = float(''.join(map(str, result_2)))
        y = res_2 * pantsSpin
        print(y)

        #total price computation
        tp = str(z+y)
        self.textBrowser.setText(
                         "STUDENT DETAILS: " +  str(studentDetail) + "\n" +
                         "TSHIRT - SIZE: " +  str(uniCombo) + "\n" +
                         "TSHIRT - QNTY: " +  str(uniSpin) + "\n" +
                         "PANTS - SIZE: " +  str(pantsCombo) + "\n" +
                         "PANTS - QNTY: " +  str(pantsSpin) + "\n" +
                         "TOTAL PRICE: " +  str(tp) + "\n"  )
      
    def totalStatus_2(self):
        self.totalStatus()

    def totalStatus_3(self):
        self.totalStatus()

    def totalStatus_4(self):
        self.totalStatus()


    ##############################################################################################################

    def borrowTab(self): 
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM borrowtab")
        self.result = self.mycursor.fetchall()
        self.tableWidget.clearContents()
        row = 0  
        self.tableWidget.setRowCount(len(self.result))      
        for i in self.result:
            self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
            
            aaa = i[4]
            self.mycursor.execute("SELECT DATE_FORMAT (time_start, '%D %M %Y %r') \
                FROM borrowtab WHERE time_start = %s", (aaa, ))
            times = self.mycursor.fetchall()
            form_time = str(times)[3:-4]
            self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem((form_time)))


            aaa = i[5]
            self.mycursor.execute("SELECT DATE_FORMAT (time_end, '%D %M %Y %r') \
                FROM borrowtab WHERE time_end = %s OR NOT NULL", (aaa, ))
            times = self.mycursor.fetchall()
            form_time = str(times)[3:-4]        
            self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem((form_time)))

            row = row + 1

    def searchBorrowTab(self):
        a = self.lineEdit_5.text()
        if len(a) != 0:
            self.mycursor = self.mydb.cursor()
            self.mycursor.execute("SELECT * FROM borrowtab WHERE studentdetails = %s", (a, ))
            self.result = self.mycursor.fetchall()
            self.tableWidget.clearContents()
            row = 0  
            self.tableWidget.setRowCount(len(self.result))      
            for i in self.result:
                self.tableWidget.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
                self.tableWidget.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
                self.tableWidget.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
                self.tableWidget.setItem(row, 3, QtWidgets.QTableWidgetItem(str(i[3])))
                
                aaa = i[4]
                self.mycursor.execute("SELECT DATE_FORMAT (time_start, '%D %M %Y %r') \
                    FROM borrowtab WHERE time_start = %s", (aaa, ))
                times = self.mycursor.fetchall()
                form_time = str(times)[3:-4]
                self.tableWidget.setItem(row, 4, QtWidgets.QTableWidgetItem((form_time)))


                aaa = i[5]
                self.mycursor.execute("SELECT DATE_FORMAT (time_end, '%D %M %Y %r') \
                    FROM borrowtab WHERE time_end = %s OR NOT NULL", (aaa, ))
                times = self.mycursor.fetchall()
                form_time = str(times)[3:-4]        
                self.tableWidget.setItem(row, 5, QtWidgets.QTableWidgetItem((form_time)))

                row = row + 1
        else:
            self.borrowTab()

    def borrow(self):
        a = self.lineEdit_5.text().upper()
        b = self.comboBox_2.currentText()
        c = 'BORROW'
        d = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
       
        try:
            self.mycursor.execute("SELECT studentdetails, status FROM borrowtab \
                 WHERE studentdetails =%s AND status = %s",(a, c))
            result = self.mycursor.fetchall()
            res_2 = str(''.join(map(str, result)))
            if (a or c) in res_2:
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("STUDENT HAS PREVIOUS BORROW EQUIPMENT THAT IS STILL NOT RETURNED.")
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()

            elif (a) == '':
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("PLEASE FILL OUT THE STUDENT DETAILS FEILD.")
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()

            else:
                self.mycursor = self.mydb.cursor()
                sql = "INSERT INTO borrowtab(studentdetails, equipment, status, time_start) \
                    VALUES(%s,%s,%s,%s);"
                qwe = (a, b, c, d)
                self.mycursor.execute(sql,qwe)
                self.mydb.commit()
                self.borrowTab()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SUCCESSFULLY ENLIST BORROW TRANSACTION.")
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
                
        except mysql.connector.Error as err:
          print(err)

    def returned(self):
        a = self.lineEdit_5.text().upper()
        b = self.comboBox_2.currentText()
        d = "RETURNED"
        ts = time.time()
        e = datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        try:
            self.mycursor.execute("SELECT borrowno, studentdetails, equipment FROM borrowtab \
                WHERE  studentdetails= %s AND equipment = %s",( a, b))
            result = self.mycursor.fetchall()
            res_2 = str(''.join(map(str, result)))
            if str(a or b ) not in res_2: 
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                self.msg.setText("STUDENT HAS NO EQUIPMENT STILL BORROWING.")
                self.msg.setWindowTitle("WARNING")
                self.msg.exec_()
            else:
                self.mycursor = self.mydb.cursor()
                sql = "UPDATE borrowtab SET status = %s, time_end = %s \
                    WHERE studentdetails = %s AND equipment = %s"
                val = (d, e, a, b)
                self.mycursor.execute(sql, val)
                self.mydb.commit()
                self.borrowTab()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SUCCESSFULLY RETURNED THE EQUIPMENT.")
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()

        except mysql.connector.Error as err:
          print(err)

    
    #######################################################################################################

    def reserveTab(self):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("SELECT * FROM reservetab")
        result = self.mycursor.fetchall()
        self.tableWidget_5.clearContents()
        row = 0  
        self.tableWidget_5.setRowCount(len(result))      
        for i in result:
            self.tableWidget_5.setItem(row, 0, QtWidgets.QTableWidgetItem(str(i[0])))
            self.tableWidget_5.setItem(row, 1, QtWidgets.QTableWidgetItem(str(i[1])))
            self.tableWidget_5.setItem(row, 2, QtWidgets.QTableWidgetItem(str(i[2])))
            self.tableWidget_5.setItem(row, 6, QtWidgets.QTableWidgetItem(str(i[6])))

            aaa = i[3]
            self.mycursor.execute("SELECT DATE_FORMAT (date,'%b %d, %Y') \
                FROM reservetab WHERE date = %s", (aaa, ))
            dates = self.mycursor.fetchall()
            for j in dates:
                form_time = str(j)[2:-3]
            self.tableWidget_5.setItem(row, 3, QtWidgets.QTableWidgetItem((form_time)))

            aaa = i[4]
            self.mycursor.execute("SELECT TIME_FORMAT(time_start, '%r') FROM reservetab \
                        WHERE time_start = %s", (aaa, ))
            times = self.mycursor.fetchall()
            for j in times:
                form_time = str(j)[2:-3]
            self.tableWidget_5.setItem(row, 4, QtWidgets.QTableWidgetItem(str(form_time)))

            aaa = i[5]
            self.mycursor.execute("SELECT TIME_FORMAT(time_end, '%r') FROM reservetab \
                        WHERE time_end = %s", (aaa, ))
            times = self.mycursor.fetchall()
            for j in times:
                form_time = str(j)[2:-3]
            self.tableWidget_5.setItem(row, 5, QtWidgets.QTableWidgetItem(str(form_time)))

            row = row + 1

    def schedule(self):
        eventName = self.lineEdit_9.text().upper()
        orgName = self.lineEdit_11.text().upper()
        date = self.dateEdit.date().toPyDate()
        timeStart = self.timeEdit.time().toPyTime()
        timeEnd = self.timeEdit_2.time().toPyTime()
        status = "ON GOING"

        self.mycursor.execute("SELECT TIME_FORMAT (time_start, '%T'), TIME_FORMAT (time_end, '%T') \
            FROM reservetab WHERE date = %s", (date, ))
        dateResult = self.mycursor.fetchall() 
        print(dateResult)
        if (len(eventName) == 0) or (len(orgName) == 0):
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Warning)
            self.msg.setText("PLEASE FILL OUT BOTH EVENT NAME AND ORG NAME FIELD.")
            self.msg.setWindowTitle("WARNING")
            self.msg.exec_()
        elif len(dateResult) == 0:
            try:
                self.mycursor = self.mydb.cursor()
                sql = "INSERT INTO reservetab(event_name, org_name, date, time_start, time_end, status) \
                    VALUES(%s, %s, %s, %s, %s, %s);"
                qwe = (eventName, orgName, date, timeStart, timeEnd, status)
                self.mycursor.execute(sql,qwe)
                self.mydb.commit()
                self.reserveTab()
                self.msg = QtWidgets.QMessageBox(self.centralwidget)
                self.msg.setIcon(QtWidgets.QMessageBox.Information)
                self.msg.setText("SUCCESSFULLY SCHEDULE A RESERVATION.")
                self.msg.setWindowTitle("INFORMATION")
                self.msg.exec_()
            except mysql.connector.Error as err:
                print(err)
        else:
            for i in dateResult:
                if str(timeStart) <= i[1] and str(timeEnd) >= i[0] :
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Warning)
                    self.msg.setText("THERE ARE TIME OVERLAP IN " + str(date) + " and " +"\n" + \
                        "THE FOLLOWING TIME IS ALREADY FILLED" + "\n" + \
                       str(dateResult)  )
                    self.msg.setWindowTitle("WARNING")
                    self.msg.exec_()
                    break
            else:
                try:
                    self.mycursor = self.mydb.cursor()
                    sql = "INSERT INTO reservetab(event_name, org_name, date, time_start, time_end, status) \
                        VALUES(%s, %s, %s, %s, %s, %s);"
                    qwe = (eventName, orgName, date, timeStart, timeEnd, status)
                    self.mycursor.execute(sql,qwe)
                    self.mydb.commit()
                    self.reserveTab()
                    self.msg = QtWidgets.QMessageBox(self.centralwidget)
                    self.msg.setIcon(QtWidgets.QMessageBox.Information)
                    self.msg.setText("SUCCESSFULLY SCHEDULE A RESERVATION.")
                    self.msg.setWindowTitle("INFORMATION")
                    self.msg.exec_()
                except mysql.connector.Error as err:
                    print(err)

    def success(self):
        reserveNo = self.spinBox_5.value()
        changeStatus = "SUCCESSFUL"
        self.mycursor.execute("SELECT reserve_no FROM reservetab WHERE reserve_no = %s",(reserveNo, ))
        result = self.mycursor.fetchall()
        res_2 = str(''.join(map(str, result)))

        if str(reserveNo) not in res_2: 
            print ("error handling")
        else:
            self.mycursor = self.mydb.cursor()
            sql = "UPDATE reservetab SET status = %s WHERE reserve_no = %s"
            val = (changeStatus, reserveNo)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.reserveTab()
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("EVENT RESERVATION IS SUCCESSFUL.")
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()

    def cancel(self):
        reserveNo = self.spinBox_5.value()
        status = "CANCEL"
        self.mycursor.execute("SELECT reserve_no FROM reservetab WHERE reserve_no = %s",(reserveNo, ))
        result = self.mycursor.fetchall()
        res_2 = str(''.join(map(str, result)))
        if str(reserveNo) not in res_2: 
            print ("error handling")
        else:
            self.mycursor = self.mydb.cursor()
            sql = "UPDATE reservetab SET status = %s WHERE reserve_no = %s"
            val = (status, reserveNo)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            self.reserveTab()
            self.msg = QtWidgets.QMessageBox(self.centralwidget)
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
            self.msg.setText("EVENT RESERVATION IS CANCELLED.")
            self.msg.setWindowTitle("INFORMATION")
            self.msg.exec_()
          





app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()