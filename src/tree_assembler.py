import csv
import networkx as nx
import matplotlib.pyplot as plt
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

G = nx.Graph()

with open('output.csv') as f:
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
    # G.add_nodes_from(next_set)
    for i in next_set:
        G.add_node(i, parent=False)

    # Draw edges between nodes
    # Supersets get priority followed by 80% of attributes
    for i in G.nodes:

        # First pass checks for supersets
        if not G.nodes[i]['parent']:
            for j in G.nodes:
                if i != j and set(i).issubset(set(j)):
                    G.add_edge(i, j)
                    G.nodes[i]['parent'] = True

        # Second pass checks for 80% rule
        if not G.nodes[i]['parent']:
            for j in G.nodes:
                if i != j and len(i) < len(j):
                    count_elements = 0
                    for each in i:
                        count_elements += j.count(each)
                    rule_eighty = count_elements / len(i)
                    if rule_eighty >= .80:
                        G.add_edge(i, j)
                        G.nodes[i]['parent'] = True

# ---Node Positioning Calculator----------

pos = dict()
x_pos = 0
y_pos = 1000
n_order = 1
x_indent = 0
y_indent = 0
tick_list = list()
tick_labels = list()
max_node_len = max([len(s) for s in G.nodes])
while n_order < max_node_len:
    n_order += 1
    next_set = [s for s in G.nodes if len(s) == n_order]
    if len(next_set) != 0:
        tick_labels.append(str(n_order))
        y_pos -= (100 + (y_indent * .5))
        tick_list.append(y_pos)
        for each in next_set:
            pos[get_line_numbers_concat(each)] = (x_pos, y_pos)
            x_pos += (150 + x_indent / 2)
        x_indent += 200
        x_pos = x_indent
        y_indent += 20

# noinspection PyTypeChecker
G = nx.relabel_nodes(G, lambda x: get_line_numbers_concat(x))

write_dot(G, 'test.dot')

# plt.title('K Modes Alpha H Tree Diagram')
fig = plt.figure(figsize=(25, 15))
ax = fig.add_subplot(1, 1, 1)

ax.set_ylabel('Order \n (n)', rotation=-0, fontsize=8, weight='bold')
ax.yaxis.set_label_coords(0, 1.02)

# Todo Fix Tick structure
print(tick_list)
print(tick_labels)
nx.draw_networkx_nodes(G, pos=pos, ax=ax, node_color='None')
nx.draw_networkx_labels(G, pos=pos, ax=ax, font_weight='bold', font_size=6)
nx.draw_networkx_edges(G, pos=pos, ax=ax, edge_color='red', alpha=.3)
plt.grid(True, axis='y')
# plt.yticks(tick_list)
ax.yaxis.set_ticks(tick_list)
ax.yaxis.set_ticklabels(tick_labels, visible=True)

plt.savefig('nx_test.jpg', optimize=True, dpi=150)
plt.show()

