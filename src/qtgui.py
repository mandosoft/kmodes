# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

import re
import gc
import math
import pandas as pd
from src.kmodes_lib import KmodesAlpha
from src.tree_gui import KmodesApp


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(960, 639)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setMinimumSize(QtCore.QSize(345, 599))
        self.widget_2.setMaximumSize(QtCore.QSize(345, 599))
        self.widget_2.setObjectName("widget_2")

        self.filename = str()
        self.df = pd.DataFrame()
        self.is_modified = False

        self.pushButton = QtWidgets.QPushButton(self.widget_2)
        self.pushButton.setGeometry(QtCore.QRect(20, 40, 181, 31))
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 140, 191, 31))
        self.pushButton_2.setObjectName("pushButton_2")

        self.checkBox = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 190, 301, 41))
        self.checkBox.setObjectName("checkBox")

        self.horizontalSlider = QtWidgets.QSlider(self.widget_2)
        self.horizontalSlider.setGeometry(QtCore.QRect(30, 420, 181, 20))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")

        self.label_2 = QtWidgets.QLabel(self.widget_2)
        self.label_2.setGeometry(QtCore.QRect(100, 230, 21, 16))
        self.label_2.setObjectName("label_2")

        self.spinBox = QtWidgets.QSpinBox(self.widget_2)
        self.spinBox.setGeometry(QtCore.QRect(90, 320, 42, 22))
        self.spinBox.setObjectName("spinBox")

        self.label_3 = QtWidgets.QLabel(self.widget_2)
        self.label_3.setGeometry(QtCore.QRect(20, 260, 331, 31))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.widget_2)
        self.label_4.setGeometry(QtCore.QRect(50, 290, 191, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.widget_2)
        self.label_5.setGeometry(QtCore.QRect(30, 370, 291, 16))
        self.label_5.setObjectName("label_5")

        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 90, 301, 21))
        self.lineEdit.setObjectName("lineEdit")

        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 480, 151, 31))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_4.setGeometry(QtCore.QRect(180, 480, 151, 31))
        self.pushButton_4.setObjectName("pushButton_4")

        self.label_6 = QtWidgets.QLabel(self.widget_2)
        self.label_6.setGeometry(QtCore.QRect(100, 440, 16, 21))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self.widget_2)
        self.label_7.setGeometry(QtCore.QRect(120, 440, 31, 21))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self.widget_2)
        self.label_8.setGeometry(QtCore.QRect(60, 390, 141, 16))
        self.label_8.setObjectName("label_8")

        self.horizontalLayout.addWidget(self.widget_2)
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setMinimumSize(QtCore.QSize(591, 599))
        self.widget.setMaximumSize(QtCore.QSize(591, 599))
        self.widget.setObjectName("widget")
        self.textBrowser = QtWidgets.QTextBrowser(self.widget)
        self.textBrowser.setGeometry(QtCore.QRect(0, 80, 571, 381))
        self.textBrowser.setObjectName("textBrowser")

        self.progressBar = QtWidgets.QProgressBar(self.widget)
        self.progressBar.setGeometry(QtCore.QRect(30, 480, 501, 21))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.progressBar.setMaximum(1000)
        self.progressBar.setValue(0)

        self.lcdNumber = QtWidgets.QLCDNumber(self.widget)
        self.lcdNumber.setGeometry(QtCore.QRect(500, 50, 64, 23))
        self.lcdNumber.setObjectName("lcdNumber")

        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(380, 50, 111, 20))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.widget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.progressBar_handler)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))

        self.pushButton.setText(_translate("MainWindow", "Select File for Upload"))
        self.pushButton.clicked.connect(self.select_file_for_upload)
        self.pushButton_2.setText(_translate("MainWindow", "Load Cluster Data"))
        self.pushButton_2.clicked.connect(self.load_cluster_data)

        self.checkBox.setText(_translate("MainWindow", "Label Using First Row Mapping"))
        self.checkBox.stateChanged.connect(self.if_button_checked)

        self.spinBox.valueChanged.connect(self.spinBox_handler)
        self.horizontalSlider.valueChanged.connect(self.horizontalSlider_handler)
        self.horizontalSlider.sliderReleased.connect(self.horizontalSlider_handler_2)
        self.label_2.setText(_translate("MainWindow", "OR"))
        self.label_3.setText(_translate("MainWindow", "Enter label number of actual location"))
        self.label_4.setText(_translate("MainWindow", "of first column in MSA"))
        self.label_5.setText(_translate("MainWindow", "Percentage of non-insertion data"))

        self.pushButton_3.setText(_translate("MainWindow", "Export to CSV"))
        self.pushButton_3.clicked.connect(self.export_to_csv)

        self.pushButton_4.setText(_translate("MainWindow", "Submit and Run"))
        self.pushButton_4.clicked.connect(self.submit_and_run)

        self.label_6.setText(_translate("MainWindow", "0"))
        self.label_7.setText(_translate("MainWindow", "%"))
        self.label_8.setText(_translate("MainWindow", "that must be present"))
        self.label.setText(_translate("MainWindow", "Current K Value"))

    def pushButton_handler(self):
        self.open_dialog_box()

    def progressBar_handler(self, increment):
        self.progressBar.setValue(self.progressBar.value() + increment)

    def spinBox_handler(self):
        if not self.checkBox.isChecked():
            self.df = self.durston_schema(self.df, self.spinBox.value())
            self.insert_to_window(self.df)
            self.is_modified = True
        else:
            self.textBrowser.clear()
            self.textBrowser.insertPlainText("Error: Cannot change label number while box is checked.")

    def horizontalSlider_handler(self):
        self.label_6.setText(str(self.horizontalSlider.value()))
        self.insert_to_window("Loading...")

    def horizontalSlider_handler_2(self):
        self.df = self.remove_insertion_data(self.df, self.horizontalSlider.value())
        self.insert_to_window(self.df)

    def remove_insertion_data(self, df: pd.DataFrame, value):
        """must return 'None' inserts to '-' str in order to run"""
        try:
            df = df.replace({'-': None})
            index_len = len(df.index)
            null_val = float(value) / 100

            for label, column in df.items():
                non_nulls = column.count()
                info_amount = non_nulls / index_len
                if info_amount < null_val:
                    df = df.drop(columns=[label])
            df = df.replace({None: '-'})

        except IndexError or KeyError:
            self.insert_to_window("Not enough columns.")

        return df

    def durston_schema(self, df: pd.DataFrame, value: int) -> pd.DataFrame:
        df.columns = range(len(df.columns))
        label_val = value
        df = df.rename(columns=lambda x: int(x) + label_val)

        return df

    def open_dialog_box(self):
        self.filename = QFileDialog.getOpenFileName()[0]
        self.lineEdit.insert(self.filename)
        return self.filename

    def read_txt_file_format(self, file) -> pd.DataFrame:

        nucs_dict = dict()
        with open(file, "r") as a_file:
            string_without_line_breaks = ""
            for line in a_file:
                stripped_line = line.rstrip()
                string_without_line_breaks += stripped_line
            a_file.close()

        vals = string_without_line_breaks.split('>')
        for line in vals:
            line = re.split('(\w+/\d*-?\d*)', line)
            line.remove('')
            for i in enumerate(line):
                g = list(line[1])
                nucs_dict.update({line[0]: g})

        self.df = pd.DataFrame.from_dict(nucs_dict, orient='index')
        self.df = self.df.replace({'.': '-'})
        self.df.index.name = 'SEQUENCE_ID'

        return self.df

    def import_data(self):
        file = open(self.filename)
        if str(self.filename).endswith(".txt"):
            self.read_txt_file_format(self.filename)
        else:
            self.df = pd.read_csv(file, encoding='utf-8', engine='c', header=None)
            self.df = self.df.rename(columns={self.df.columns[0]: 'SEQUENCE_ID'})
            self.df = self.df.set_index('SEQUENCE_ID', drop=True)

        self.insert_to_window(self.df)

    def insert_to_window(self, args):
        self.textBrowser.clear()
        if isinstance(args, pd.DataFrame):
            try:
                self.textBrowser.insertPlainText("Columns:  " + str(len(self.df.columns)) + "\n" +
                                                 "Sequences: " + str(len(self.df.index)) + "\n" +
                                                 "Label Numbers: "
                                                 + str(args.columns[0]) + "..." + str(args.columns[-1]))
            except IndexError:
                self.insert_to_window("Not enough columns to use.")
        elif isinstance(args, str):
            self.textBrowser.insertPlainText(args)

    def select_file_for_upload(self):
        self.pushButton_handler()
        self.import_data()

    def load_cluster_data(self):
        self.pushButton_handler()

    def deweese_schema(self, df: pd.DataFrame) -> pd.DataFrame:
        try:
            df = df.rename(columns=lambda x: x - 1)
            first_row_ix = df.index[0]
            ix_label = first_row_ix.rsplit('/', 1)
            ix_label = ix_label[1]
            ix_label = ix_label.rsplit('-', 1)
            df_label = int(ix_label[0])
            column_lab_dict = dict()

            pattern = '^-'

            # TODO Catch weird insertion detection bug
            for i in df:
                if not re.search(pattern, df[i].iloc[0]):
                    column_lab_dict[df.columns[i]] = df_label
                    df_label += 1
                else:
                    column_lab_dict[df.columns[i]] = ''
            df = df.rename(columns=column_lab_dict)
            df = df.drop(columns=[''])
            df = df.rename(columns=lambda x: int(x))
        except IndexError or KeyError:
            self.insert_to_window("Index is incorrect. Please check MSA.")

        return df

    def garbage_collect(self, df: pd.DataFrame):
        del df
        gc.collect()
        self.import_data()

    def if_button_checked(self):
        if self.checkBox.isChecked():
            if self.is_modified:
                self.garbage_collect(self.df)
            self.df = self.deweese_schema(self.df)
            self.insert_to_window(self.df)
        if not self.checkBox.isChecked():
            self.garbage_collect(self.df)

    def export_to_csv(self):
        save_file = QFileDialog.getSaveFileName()
        self.df.to_csv(save_file, index=True, header=True)

    # noinspection PyCallByClass
    def submit_and_run(self):

        cluster_list = [pd.DataFrame(self.df[i]) for i in self.df]
        k = len(cluster_list)
        increment = int(10 * (100 / len(cluster_list)))
        kmodes_alpha = KmodesAlpha()
        kmodes_alpha.map_clusters(cluster_list, k)

        while k != 2:
            k -= 1
            print(increment)
            self.progressBar_handler(increment)
            kmodes_alpha.kmodes(cluster_list, k)

        kmodes_alpha.export_to_tree()
        app = KmodesApp()
        app.protocol("WM_DELETE_WINDOW", app.on_closing)
        app.mainloop()
        return sys.exit()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
