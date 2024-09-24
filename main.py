from NFA import *
from DFA import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# TODO 画图
def show(FA):
    graph = nx.MultiDiGraph()

    graph.add_nodes_from(FA.status)


    color_map = []
    edge_labels = {}
    loop_edges = {}
    for n in graph.nodes():
        if n in FA.end:
            color_map.append('black')
        else:
            color_map.append('blue')

    for edge in FA.edges:
        if edge.start == edge.end:
            loop_edges[(edge.start, edge.end)] = edge.symbol
        graph.add_edge(edge.start, edge.end)
        edge_labels[(edge.start, edge.end)] = edge.symbol

    # 添加s指向开始节点的边
    graph.add_edge("s", FA.start )
    edge_labels[("s" , FA.start)] = "start"
    # 设置s节点的颜色
    color_map.append("red")

    pos = nx.spectral_layout(graph)
    nx.draw(graph , pos , with_labels=True , node_color = color_map , font_color = "white")
    nx.draw_networkx_edge_labels(graph, pos ,edge_labels=edge_labels)


    nx.draw_networkx_edges(graph, pos, edgelist=loop_edges, connectionstyle='arc3, rad = 0.2', arrows=True)

    # 添加自环上的标签
    for edge in loop_edges:
        n1, n2 = edge
        label = loop_edges[(n1, n2)]
        # 计算自环弧线的中心位置
        arc_center = pos[n1] + 0.5 * (pos[n1] - pos[n1]) + 0.1 * (pos[n1] - pos[n1])
        arc_radius = 0.2  # 自环弧线的半径
        arc_angle = 90  # 标签放置的角度

        # 计算标签位置
        label_pos = (arc_center[0] + arc_radius * np.cos(np.radians(arc_angle)),
                     arc_center[1] + arc_radius * np.sin(np.radians(arc_angle)))

        plt.text(label_pos[0], label_pos[1], label, ha='center', va='center', fontsize=10)

    plt.show()

if __name__ == '__main__':
    regex = "(ab)*(a*|b*)(ba)*"
    nfa = NFA(regex)
    dfa = DFA(nfa)
    show(dfa)
