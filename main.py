# -*- coding: utf-8 -*-
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QMainWindow

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QTimer, QThread, pyqtSignal

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QIcon
import numpy as np
import networkx as nx
import csv
import os
from matplotlib import pyplot as plt
from matplotlib import patches as mpatches

from matplotlib.backends.qt_compat import QtCore, QtWidgets
if QtCore.qVersion() >= "5.":
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


import re
import gc
import math
import pandas as pd
import kmodesalpha
from kmodesalpha import kmodes


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
        kmodes_instance = kmodes.KmodesAlpha()
        kmodes_instance.map_clusters(cluster_list, k)

        while k != 2:
            k -= 1
            self.progressBar_handler(increment)
            kmodes_instance.kmodes(cluster_list, k)

        kmodes_instance.export_to_tree()
        app = ApplicationWindow()
        app.show()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self._main = QtWidgets.QWidget()
        self.setCentralWidget(self._main)
        self.tabs = QtWidgets.QTabWidget()
        layout = QtWidgets.QVBoxLayout(self._main)
        self.font_size = 6
        figure = self.draw_tree(0, 0)
        static_canvas = FigureCanvas(figure)
        self.table = ClusterData()
        self.tabs.addTab(static_canvas, "Tree View")
        self.tabs.addTab(self.table, "Cluster Data")
        layout.addWidget(self.tabs)
        self.nav_bar = self.addToolBar(NavigationToolbar(static_canvas, self))
        #save_file_action = QAction(QIcon('assets/csv.png'), 'Save CSV', self)
        #save_file_action.triggered.connect(self.table.save_sheet)
        self.toolbar = self.addToolBar('Data')
        #self.toolbar.addAction(save_file_action)

    def draw_tree(self, cutoff, prime_cluster):
        """
        This is the main tree drawing method
        """
        G = nx.Graph()

        self.path = 'tree_input.csv'

        with open(self.path) as f:
            lines = list(csv.reader(f))

        # TODO: Refactor this area
        data = lines[1:]  # ignores header
        # TODO fix this using split or other method
        data = [e for e in data if len(e) != 0]
        values = [entry for entry in data if float(entry[2]) >= cutoff]  # modified variable
        tree_list = [(entry[0].strip('()'), entry[2]) for entry in values]
        tree_list = [(i[0].split(','), i[1]) for i in tree_list]
        tree_list = [(list(map(int, i[0])), float(i[1])) for i in tree_list]
        max_len = max([len(s[0]) for s in tree_list])

        # reformat sequence of numbers with hyphens
        def get_line_numbers_concat(line_nums):
            seq = []
            final = []
            last = 0

            for index, val in enumerate(line_nums):

                if last + 1 == val or index == 0:
                    seq.append(val)
                    last = val
                else:
                    if len(seq) > 1:
                        final.append(str(seq[0]) + '-' + str(seq[len(seq) - 1]))
                    else:
                        final.append(str(seq[0]))
                    seq = list()
                    seq.append(val)
                    last = val

                if index == len(line_nums) - 1:
                    if len(seq) > 1:
                        final.append(str(seq[0]) + '-' + str(seq[len(seq) - 1]))
                    else:
                        final.append(str(seq[0]))

            final_str = ', '.join(map(str, final))
            final_str = ''.join(('(', final_str, ')'))
            return final_str

        # set default attributes for nodes
        for i in G.nodes:
            G.nodes[i]['parent'] = False
            G.nodes[i]['split'] = False
            G.nodes[i]['split_full'] = False  # Prevents nodes from splitting into more than two clusters
            G.nodes[i]['color'] = None
            G.nodes[i]['sr_mode'] = None
            G.nodes[i]['prime_cluster'] = False

        n_order = 1
        while n_order < max_len:

            n_order += 1
            next_set = [(s[0], s[1]) for s in tree_list if len(s[0]) == n_order]

            for i in next_set:
                for ix, j in enumerate(next_set):
                    # removes cases of non disjoint sets of same n_order
                    if i[0] != j[0] and not set(i[0]).isdisjoint(set(j[0])):
                        next_set.remove(next_set[ix])
            next_set = [(tuple(t[0]), t[1]) for t in next_set]
            next_set = sorted(list(set(next_set)))

            # G.add_nodes_from(next_set)
            for i in next_set:
                G.add_node(i[0], color=None, parent=False, split=False, split_full=False, sr_mode=i[1],
                           prime_cluster=False)

            # Draw edges between nodes
            # Supersets get priority followed by 80% of attributes
            for i in G.nodes:
                if G.nodes[i]['sr_mode'] >= prime_cluster:  # set prime cluster value
                    G.nodes[i]['prime_cluster'] = True
                    G.nodes[i]['color'] = '#be0000'
                else:
                    G.nodes[i]['color'] = '#00000000'  # everything else is a clear color

                # First pass checks for supersets
                if G.nodes[i]['parent'] is not True:
                    for j in G.nodes:
                        if i != j and set(i).issubset(set(j)):
                            G.add_edge(i, j)
                            G.nodes[i]['parent'] = True

                # TODO Fix getitem. Likely just needs an instance method
                # Second pass checks for cluster splits
                if G.nodes[i]['split_full'] is not True and G.nodes[i]['parent'] is not True:
                    for j in G.nodes:
                        if i != j and len(i) < len(j):
                            count_elements = 0
                            for each in i:
                                count_elements += j.count(each)
                            percent_in_child = count_elements / len(i)
                            if percent_in_child >= .33:
                                if G.degree[i] < 2:
                                    G.add_edge(i, j)
                                    G.nodes[i]['split'] = True
                                    if G.degree[i] == 2:
                                        G.nodes[i]['split_full'] = True
        for v, w in G.edges:
            if G.nodes[v]["parent"] is True and G.nodes[v]["split"] is False:
                G.edges[v, w]["subset"] = True
            else:
                G.edges[v, w]["subset"] = False
        # -------Node Positioning Calculator----------

        pos = dict()
        x_pos = 0
        y_pos = 1000
        n_order = 1
        ytick_list = list()
        xtick_list = list()
        xtick_labels = list()
        ytick_labels = list()
        max_node_len = max([len(s) for s in G.nodes])
        max_node_val = max([i for s in G.nodes for i in s])
        spacing_set_len = len([s for s in G.nodes if len(s) == 2])
        x_increment = max_node_val / spacing_set_len

        while n_order < max_node_len:

            n_order += 1
            next_set = [s for s in G.nodes if len(s) == n_order]

            # Set x tick labels to identify pairwise cluster locations
            if n_order == 2:
                xtick_labels = [(next_set.index(x) + 1) for x in next_set]

            if len(next_set) != 0:
                ytick_labels.append(str(n_order))
                y_pos -= 100
                ytick_list.append(y_pos)

                for each in next_set:
                    if len(each) == 2:
                        x_pos += x_increment
                    else:
                        x_pos = sum(each) / len(each)

                    pos[each] = (x_pos, (y_pos + 10))  # y offset label from x axis
                    xtick_list.append(x_pos)

        n_order = 2
        while n_order < max_node_len:
            n_order += 1
            value_list = list()
            temp_dict = {each: values for (each, values) in pos.items() if len(each) == n_order}
            for v, v1 in temp_dict.values():
                value_list.append(v)

            if len(value_list) > 1:
                max_value_list = max(value_list)
                min_value_list = min(value_list)
                if min_value_list > 99:
                    min_value_list /= 2
                # Create an evenly spaced vector of x_pos values
                lin_vector = np.linspace(min_value_list, max_value_list, num=len(value_list))
                ind = 0
                for k, v in temp_dict.items():
                    u, m = v
                    temp_dict[k] = (lin_vector[ind], m)
                    ind += 1

            pos.update(temp_dict)

        pos = {get_line_numbers_concat(k): v for k, v in pos.items()}
        # noinspection PyTypeChecker
        G = nx.relabel_nodes(G, lambda x: get_line_numbers_concat(x))

        # write_dot(G, 'test.dot')

        """
        All of the custom graph drawing 
        """
        self.fig = plt.figure(figsize=(5, 5))
        ax = self.fig.add_subplot(1, 1, 1)
        ax.set_ylabel('Order \n (n)', rotation=-0, fontsize=8, weight='bold')
        ax.yaxis.set_label_coords(0, 1.02)
        ax.set_xlabel('Site location in the Multiple Sequence Alignment', fontsize=8, weight='bold')
        ax.xaxis.set_label_coords(0.5, 1.12)
        node_colors = [G.nodes[i]['color'] for i in G.nodes]

        # Draw nodes
        rx, ry = .6, .25
        area = rx * ry * np.pi
        theta = np.arange(0, 2 * np.pi + 0.01, 0.1)
        verts = np.column_stack([rx / area * np.cos(theta), ry / area * np.sin(theta)])
        nx.draw_networkx_nodes(G, pos=pos, ax=ax, node_color='#00000000', edgecolors=node_colors, node_shape=verts,
                               node_size=1000)
        nx.draw_networkx_labels(G, pos=pos, ax=ax, font_color='k', font_weight='bold', font_size=self.font_size)

        # Draw edges
        edges_p = [e for e in G.edges if G.edges[e]["subset"]]
        edges_s = [e for e in G.edges if not G.edges[e]["subset"]]
        nx.draw_networkx_edges(G, pos=pos, ax=ax, style='solid', edgelist=edges_p, edge_color='k', alpha=.5)
        nx.draw_networkx_edges(G, pos=pos, ax=ax, style='dashed', edge_color='#DB7093', edgelist=edges_s, width=1.5,
                               alpha=.5)

        plt.grid(True, axis='y')
        ax.yaxis.set_ticks(ytick_list)
        ax.yaxis.set_ticklabels(ytick_labels, visible=True)
        ax.xaxis.set_ticks(xtick_list)
        ax.xaxis.set_ticklabels(xtick_labels, visible=True)
        split_patch = mpatches.Patch(color='pink', label='cluster split')
        perfect_patch = mpatches.Patch(color='black', label='perfect superset')
        ax.legend(handles=([perfect_patch, split_patch]), loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=2)
        for i, k in enumerate(ax.xaxis.get_ticklabels()):
            label = ax.xaxis.get_ticklabels()[i]
            label.set_bbox(dict(facecolor='white', edgecolor='black'))
        ax.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=False, bottom=False,
                       top=False, left=False, right=False)

        return self.fig


class ClusterData(QtWidgets.QTableWidget):
    def __init__(self):
        super().__init__()
        self.setRowCount(0)
        self.setColumnCount(3)
        data = open('output.csv')
        file = csv.reader(data)

        for row_data in file:
            row = self.rowCount()
            self.insertRow(row)
            for col, each in enumerate(row_data):
                entry = row_data[col]
                item = QtWidgets.QTableWidgetItem(entry)
                self.setItem(row, col, item)

    def save_sheet(self):
        path = QtWidgets.QFileDialog.getSaveFileName(self, "Save CSV", os.getenv('HOME'), 'CSV (*.csv)')
        if path[0] != '':
            with open(path, "w") as csv_file:
                writer = csv.writer(csv_file)
                for row in range(self.rowCount()):
                    row_data = []
                    for column in range(self.columnCount()):
                        item = self.item(row, column)
                        if item is not None:
                            row_data.append(item.text())
                        else:
                            row_data.append('')
                    writer.writerow(row_data)


if __name__ == "__main__":
    import sys
    appctxt = ApplicationContext()  # 1. Instantiate ApplicationContext
    window = QMainWindow()
    app = QtWidgets.QApplication(sys.argv)
    ui = Ui_MainWindow()
    ui.setupUi(window)
    window.show()
    exit_code = appctxt.app.exec_()  # 2. Invoke appctxt.app.exec_()

