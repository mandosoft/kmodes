from src.tree_viz.tree_assembler import *

from tkinter import *
from tkinter import ttk, messagebox
from tkdatacanvas import *

import networkx as nx
import io
import csv

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
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

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Are you sure want to quit?"):
            self.destroy()


class TreeTab(Frame):
    def __init__(self, name, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
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
        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=True)


class CsvTab(Frame):

    def __init__(self, name, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.name = name
        self.canvas = DataCanvas(self)
        self.write_data()
        self.canvas.pack(side=TOP, fill=BOTH)

    def write_data(self):
        with io.open("outfiles/output.csv", "r", newline="") as csv_file:
            reader = csv.reader(csv_file)
            parsed_rows = 0
            for row in reader:
                if parsed_rows == 0:
                    # Display the first row as a header
                    self.canvas.add_header(*row)
                else:
                    self.canvas.add_row(*row)
                parsed_rows += 1
        self.canvas.display()


app = KmodesApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.mainloop()
