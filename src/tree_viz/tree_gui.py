from tkinter import *
from tkinter import ttk, messagebox, filedialog
from tkdatacanvas import *

import networkx as nx
from networkx.drawing.nx_agraph import write_dot
import numpy as np
import io
import os
import csv
import glob

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


class KmodesApp(Tk):
    """
    Window for model view controller
    """
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "K Modes Alpha")
        self.notebook = ttk.Notebook()
        self.control_panel = ControlPanel(self, padx=25)
        self.add_features()
        self.notebook.pack(side=LEFT, fill=BOTH, expand=True)
        self.control_panel.pack(side=RIGHT, fill=BOTH, expand=False)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure want to quit?"):
            exit()

    def add_features(self):
        tab = TreeTab(self.notebook)
        tab2 = CsvTab(self.notebook, tab.prime_cluster)

        def get_val():
            tab.val = self.control_panel.spinbox.get()
            tab.font_size = self.control_panel.font_spinbox.get()
            tab.pc_val = self.control_panel.pc_entry.get()
            tab.update_tree()

        def onselect(evt):
            # Note here that Tkinter passes an event object to onselect()
            w = evt.widget
            index = w.curselection()[0]
            value = w.get(index)
            print(value)

        # SR Mode zoom
        self.control_panel.label = Label(self.control_panel, text="Zoom by Sr Mode Value", anchor=W, justify=LEFT,
                                         font=("Helvetica", 6))
        self.control_panel.label.pack(side=TOP, fill=NONE, expand=False, pady=(50, 5))
        self.control_panel.spinbox = Spinbox(self.control_panel, from_=0, to=100, command=get_val)
        self.control_panel.spinbox.pack(side=TOP, fill=NONE, expand=False)

        # Font selector
        self.control_panel.label = Label(self.control_panel, text="Select Font Size", anchor=W, justify=LEFT,
                                         font=("Helvetica", 6))
        self.control_panel.label.pack(side=TOP, fill=NONE, expand=False, pady=(20, 5))
        self.control_panel.font_spinbox = Spinbox(self.control_panel, from_=1, to=100, command=get_val)
        self.control_panel.font_spinbox.pack(side=TOP, fill=NONE, expand=False)

        # Prime cluster value selector
        self.control_panel.label = Label(self.control_panel, text="Set Prime Cluster Value", anchor=W, justify=LEFT,
                                         font=("Helvetica", 6))
        self.control_panel.label.pack(side=TOP, fill=NONE, expand=False, pady=(20, 5))
        self.control_panel.pc_entry = Entry(self.control_panel, textvariable=tab.pc_val)
        self.control_panel.pc_entry.pack(side=TOP, fill=NONE, expand=False)

        self.control_panel.directory = Listbox(self.control_panel, highlightcolor='purple', selectbackground='#c38bd9')
        self.control_panel.directory.bind('<<ListboxSelect>>', onselect)
        files_names = map(os.path.basename, glob.glob("outfiles/*.csv"))
        for i, j in enumerate(files_names):
            self.control_panel.directory.insert(i, j)
        self.control_panel.directory.pack(side=TOP, fill=None, expand=False, pady=(100, 5))

        self.notebook.add(tab, text="Tree View")
        self.notebook.add(tab2, text="Cluster Data")




class ControlPanel(Frame):
    def __init__(self, spinbox, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.spinbox = spinbox
        self.font_spinbox = None
        self.pc_entry = None
        self.label = None
        self.directory = None


class TreeTab(Frame):
    """Tree canvas. Note instance is refreshed when tree is updated."""

    def __init__(self, canvas, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        Frame.config(self, bg="white")
        self.canvas = canvas
        self.val = 0
        self.font_size = 5
        self.pc_val = DoubleVar()
        self.prime_cluster = 0
        self.pc_val.set(.33)
        self.draw_tree(0, .33)  # set cutoff to zero by default

    def update_tree(self):  # val changes as spinbox is moved
        cutoff = float(self.val) / 100
        self.prime_cluster = float(self.pc_val)
        self.fig.clf()  # memory manage figures
        self.canvas.get_tk_widget().pack_forget()
        self.toolbar.destroy()
        return self.draw_tree(cutoff, self.prime_cluster)

    def draw_tree(self, cutoff, prime_cluster):
        """
        This is the main tree drawing method
        """
        G = nx.Graph()
        tree_path = os.path.abspath('tree_viz/tree_input.csv')
        with open(tree_path) as f:
            lines = list(csv.reader(f))
        # TODO: Refactor this area
        data = lines[1:]  # ignores header
        #TODO fix this using split or other method
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
                G.add_node(i[0], color=None, parent=False, split=False, split_full=False, sr_mode=i[1], prime_cluster=False)

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

                    pos[each] = (x_pos, (y_pos+10))  # y offset label from x axis
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

        write_dot(G, 'test.dot')

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
        nx.draw_networkx_nodes(G, pos=pos, ax=ax, node_color='#00000000', edgecolors=node_colors, node_shape=verts, node_size=1000)
        nx.draw_networkx_labels(G, pos=pos, ax=ax, font_color='k', font_weight='bold', font_size=self.font_size)

        # Draw edges
        edges_p = [e for e in G.edges if G.edges[e]["subset"]]
        edges_s = [e for e in G.edges if not G.edges[e]["subset"]]
        nx.draw_networkx_edges(G, pos=pos, ax=ax, style='solid', edgelist=edges_p, edge_color='k', alpha=.5)
        nx.draw_networkx_edges(G, pos=pos, ax=ax, style='dashed', edge_color='#DB7093', edgelist=edges_s, width=1.5, alpha=.5)

        plt.grid(True, axis='y')
        ax.yaxis.set_ticks(ytick_list)
        ax.yaxis.set_ticklabels(ytick_labels, visible=True)
        ax.xaxis.set_ticks(xtick_list)
        ax.xaxis.set_ticklabels(xtick_labels, visible=True)
        split_patch = mpatches.Patch(color='red', label='cluster split')
        perfect_patch = mpatches.Patch(color='black', label='perfect superset')
        ax.legend(handles=([perfect_patch, split_patch]), loc='upper center', bbox_to_anchor=(0.5, -0.05),
                  fancybox=True, shadow=True, ncol=2)
        for i, k in enumerate(ax.xaxis.get_ticklabels()):
            label = ax.xaxis.get_ticklabels()[i]
            label.set_bbox(dict(facecolor='white', edgecolor='black'))
        ax.tick_params(labelbottom=False, labeltop=True, labelleft=True, labelright=False, bottom=False,
                       top=False, left=False, right=False)

        # Canvas settings

        self.canvas = FigureCanvasTkAgg(self.fig, self)

        # self.canvas.mpl_connect('pick_event', onpick)
        self.canvas.draw()
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


class CsvTab(Frame):

    def __init__(self, prime_cluster, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.prime_cluster = prime_cluster
        self.canvas = DataCanvas(self)
        self.write_data()
        self.canvas.pack(side=TOP, fill=BOTH, expand=True)

    def write_data(self):
        print(os.getcwd())
        path = os.path.abspath("outfiles/output.csv")
        with io.open(path, "r", newline="") as csv_file:
            reader = csv.reader(csv_file)
            parsed_rows = 0
            for row in reader:
                if parsed_rows == 0:
                    # Display the first row as a header
                    self.canvas.add_header(*row[::-1])
                elif float(row[2]) > .33:
                    self.canvas.add_row(*row[::-1], fg="#be0000")
                else:
                    self.canvas.add_row(*row[::-1], fg="#000000")
                parsed_rows += 1

        self.canvas.display()


app = KmodesApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
