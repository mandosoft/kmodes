import csv
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from networkx.drawing.nx_agraph import write_dot, graphviz_layout
import math

G = nx.Graph()

with open('tree_viz/tree_input.csv') as f:
    lines = list(csv.reader(f))
values = lines[1:]
tree_list = [entry[0].strip('()') for entry in values]
tree_list = [i.split(',') for i in tree_list]
tree_list = [list(map(int, i)) for i in tree_list]
max_len = max([len(s) for s in tree_list])


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


# -------- Loop ----------------
# parent = False
for i in G.nodes:
    G.nodes[i]['parent'] = False
    G.nodes[i]['split'] = False

n_order = 1
while n_order < max_len:

    n_order += 1
    next_set = [s for s in tree_list if len(s) == n_order]
    for i in next_set:
        for ix, j in enumerate(next_set):
            # removes cases of non disjoint sets of same n_order
            if i != j and not set(i).isdisjoint(set(j)):
                next_set.remove(next_set[ix])
    next_set = [tuple(t) for t in next_set]
    next_set = sorted(list(set(next_set)))
    # G.add_nodes_from(next_set)
    for i in next_set:
        G.add_node(i, parent=False, split=False)

    # Draw edges between nodes
    # Supersets get priority followed by 80% of attributes
    for i in G.nodes:

        # First pass checks for supersets
        if not G.nodes[i]['parent']:
            for j in G.nodes:
                if i != j and set(i).issubset(set(j)):
                    G.add_edge(i, j, color='r')
                    G.nodes[i]['parent'] = True

        # Second pass checks for 80% rule
        if not G.nodes[i]['parent']:
            for j in G.nodes:
                if i != j and len(i) < len(j):
                    count_elements = 0
                    for each in i:
                        count_elements += j.count(each)
                    percent_in_child = count_elements / len(i)
                    if percent_in_child >= .33:
                        if G.degree[i] < 2:
                            G.add_edge(i, j, color='purple')
                            G.nodes[i]['split'] = True
                            if G.degree[i] == 2:
                                G.nodes[i]['parent'] = True


# ---Node Positioning Calculator----------

pos = dict()
x_pos = 0
y_pos = 1000
n_order = 1
x_indent = 0
y_indent = 0
ytick_list = list()
xtick_list = list()
xtick_labels = list()
ytick_labels = list()
max_node_len = max([len(s) for s in G.nodes])
max_node_val = max([i for s in G.nodes for i in s])
spacing_set_len = len([s for s in G.nodes if len(s) == 2])
x_increment = max_node_val/spacing_set_len

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
                x_pos = sum(each)/len(each)

            pos[each] = (x_pos, y_pos)
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

# plt.title('K Modes Alpha H Tree Diagram')
fig = plt.figure(figsize=(25, 15))
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

plt.savefig('nx_test.jpg', optimize=True, dpi=150)
plt.show()