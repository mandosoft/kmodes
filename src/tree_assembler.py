import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
G = nx.DiGraph()

with open('output.csv') as f:
    lines = list(csv.reader(f))
values = lines[1:]
tree_list = [entry[0].strip('()') for entry in values]
tree_list = [i.split(',') for i in tree_list]
tree_list = [list(map(int, i)) for i in tree_list]

# -------- Loop ----------------
n_order = 2
n_order_list = [s for s in tree_list if len(s) == n_order]

# !Fix with map()
for i in n_order_list:
    for ix, j in enumerate(n_order_list):
        if i != j:
            for each in i:
                for each2 in j:
                    if each == each2:
                        n_order_list.remove(n_order_list[ix])
n_order_list = [tuple(s) for s in n_order_list]
n_order_list = sorted(list(set(n_order_list)))


G.add_nodes_from(n_order_list)
# ------------------------------

# run "dot -Tpng test.dot >test.png"
write_dot(G, 'test.dot')

plt.title('K Modes Alpha H Tree Diagram')
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=True, node_color='None')
plt.savefig('nx_test.png')
