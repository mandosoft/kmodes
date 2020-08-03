import sys
import time

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
        save_file_action = QAction(QIcon('assets/csv.png'), 'Save CSV', self)
        save_file_action.triggered.connect(self.table.save_sheet)
        self.toolbar = self.addToolBar('Data')
        self.toolbar.addAction(save_file_action)

    def draw_tree(self, cutoff, prime_cluster):
        """
        This is the main tree drawing method
        """
        G = nx.Graph()

        self.path = '../data/tree_input.csv'

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
        data = open('../data/output.csv')
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
    # Check whether there is already a running QApplication (e.g., if running
    # from an IDE).
    qapp = QtWidgets.QApplication.instance()
    if not qapp:
        qapp = QtWidgets.QApplication(sys.argv)

    app = ApplicationWindow()
    app.show()
    app.activateWindow()
    app.raise_()
    qapp.exec_()