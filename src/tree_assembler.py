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
    for i in G.nodes:
        if not G.nodes[i]['parent']:
            for j in G.nodes:
                if i != j and set(i).issubset(set(j)):
                    G.add_edge(i, j)
                    G.nodes[i]['parent'] = True

# ------------------------------
# run "dot -Tpng test.dot >test.png"

# noinspection PyTypeChecker
G = nx.relabel_nodes(G, lambda x: get_line_numbers_concat(x))
write_dot(G, 'test.dot')

plt.title('K Modes Alpha H Tree Diagram')
plt.figure(figsize=(25, 15))
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos, with_labels=True, arrows=False, node_color='None', node_size=15,
        font_size=9, width=.5, edge_color='red')
plt.savefig('nx_test.jpg', optimize=True, dpi=300)


'''
# -------------Window Render---------------------
fig = plt.figure(figsize=(11, 6))
ax = fig.add_subplot(1, 1, 1)
pos = graphviz_layout(G, prog='dot')
nx.draw(G, pos=pos, ax=ax, with_labels=True, arrows=True, node_color='None', node_size=15,
        font_size=10, width=.5, edge_color='red')
ax.set_ylabel('Order \n (n)', rotation=-0, fontsize=8, weight='bold')

ax.yaxis.set_label_coords(0, 1.02)
ax.axes.get_xaxis().set_visible(False)
ax.patch.set_linewidth('0')
plt.ylim(max_len, 2)
tick_list = list(range(2, (max_len + 1)))
ax.set_yticks(tick_list)
ax.axes.grid(color='black', linestyle='-', linewidth=1)
ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)
plt.show()
plt.savefig('nx_test.jpg')
'''


