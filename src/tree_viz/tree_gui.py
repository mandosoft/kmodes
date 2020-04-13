from src.tree_viz.tree_assembler import *

from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import networkx as nx
import csv

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

import matplotlib.pyplot as plt


class KmodesApp(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        Tk.wm_title(self, "K Modes Alpha")
        self.notebook = ttk.Notebook()
        self.add_tab()
        self.notebook.pack(side=TOP, fill=BOTH, expand=True)

    def add_tab(self):
        tab = TreeTab(self.notebook)
        tab2 = CsvTab(self.notebook)
        self.notebook.add(tab, text="Tree View")
        self.notebook.add(tab2, text="Cluster Data")


class TreeTab(Frame):
    def __init__(self, name, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        # self.label = Label(self, text="Tree View")
        # self.label.grid(row=1, column=0, padx=10, pady=10)
        self.name = name
        fig = plt.figure(figsize=(5, 5))

        ax = fig.add_subplot(1, 1, 1)
        ax.set_ylabel('Order \n (n)', rotation=-0, fontsize=8, weight='bold')
        ax.yaxis.set_label_coords(0, 1.02)
        ax.set_xlabel('Site location in the Multiple Sequence Alignment', fontsize=4, weight='bold')
        ax.xaxis.set_label_coords(0.50, 1.02)

        nx.draw_networkx_nodes(G, pos=pos, ax=ax, node_color='#4ede71', node_size=60, alpha=.2)
        nx.draw_networkx_labels(G, pos=pos, ax=ax, font_weight='bold', font_size=5)
        colors = [G[u][v]['color'] for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos=pos, ax=ax, edge_color=colors, alpha=.6)
        plt.grid(True, axis='y')
        ax.yaxis.set_ticks(ytick_list)
        ax.yaxis.set_ticklabels(ytick_labels, visible=True)
        ax.xaxis.set_ticks(xtick_list)
        ax.xaxis.set_ticklabels(xtick_labels, visible=True)
        canvas = FigureCanvasTkAgg(fig, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


class CsvTab(Frame):
    def __init__(self, name, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.label = Label(self, text="CSV Data")
        self.label.grid(row=1, column=0, padx=10, pady=10)
        self.name = name


app = KmodesApp()
app.mainloop()
