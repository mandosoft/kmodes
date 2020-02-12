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
max_len = max([len(s) for s in tree_list])

# -------- Loop ----------------

n_order = 1
while n_order < max_len:

    n_order += 1
    next_set = [s for s in tree_list if len(s) == n_order]
    for i in next_set:
        for ix, j in enumerate(next_set):
            if i != j and not set(i).isdisjoint(set(j)):
                next_set.remove(next_set[ix])
    next_set = [tuple(t) for t in next_set]
    next_set = sorted(list(set(next_set)))
    G.add_nodes_from(next_set)

    for i in G.nodes:
        for j in G.nodes:
            if i != j and set(i).issubset(set(j)):
                G.add_edge(i, j)

    print(G.nodes)

# ------------------------------
# run "dot -Tpng test.dot >test.png"
write_dot(G, 'test.dot')

plt.title('K Modes Alpha H Tree Diagram')
plt.ylabel('n order')
plt.figure(figsize=(10, 10))
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=False, node_color='None', node_size=15,
        font_size=5, width=.5, edge_color='red')
plt.savefig('nx_test.png')
