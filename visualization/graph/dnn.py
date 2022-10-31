import matplotlib.pyplot as plt
import networkx as nx


def visualize_dnn_graph(G):
    pos = {}
    y = 0
    for i_node, node in enumerate(G.nodes()):
        pos[node] = (i_node, y)
        y -= 3
    fig = plt.figure(figsize=(15, 10))
    rad = 0.8
    ax = plt.gca()
    edges = G.edges()
    for edge in edges:
        source, target = edge
        edge_rad = 0 if pos[target][0] - pos[source][0] == 1 else rad
        ax.annotate("",
                    xy=pos[source],
                    xytext=pos[target],
                    arrowprops=dict(arrowstyle="-", color="red",
                                    connectionstyle=f"arc3,rad={edge_rad}",
                                    alpha=0.7,
                                    linewidth=2))
    nx.draw_networkx_nodes(G, pos=pos, node_size=100, node_color='black')
    nx.draw_networkx_labels(G, pos=pos, font_color='red')
    plt.box(False)
    fig.tight_layout()
    plt.show()
