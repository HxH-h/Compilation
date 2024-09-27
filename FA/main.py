from NFA import *
from DFA import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


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

    pos = nx.spring_layout(graph)
    nx.draw(graph , pos , with_labels=True , node_color = color_map , font_color = "white")
    nx.draw_networkx_edge_labels(graph, pos ,edge_labels=edge_labels)


    nx.draw_networkx_edges(graph, pos, edgelist=loop_edges, connectionstyle='arc3, rad = 0.2', arrows=True)

    # 添加自环上的标签
    for edge in loop_edges:
        n1, n2 = edge
        label = loop_edges[(n1, n2)]
        # 计算自环弧线的中心位置
        (x, y) = pos[n1]
        radius = 0.15  # 自环半径
        angle = np.pi / 4  # 自环角度

        # 计算自环路径上的两个点
        x1 = x + radius * np.cos(angle)
        y1 = y + radius * np.sin(angle)
        x2 = x - radius * np.cos(angle)
        y2 = y - radius * np.sin(angle)

        # 在自环路径上找到中间位置
        x_mid = (x1 + x2) / 2
        y_mid = (y1 + y2) / 2

        # 确保标签不与节点重合
        label_offset = 0.1  # 标签偏移量
        x_label = x_mid
        y_label = y_mid + label_offset * np.sin(angle)

        # 绘制自环标签
        plt.text(x_label, y_label, label, fontsize=12, ha='center', va='center', color='black')

    plt.axis('off')  # 不显示坐标轴
    plt.show()



if __name__ == '__main__':
    regex = "a|b"
    nfa = NFA(regex)
    dfa = DFA(nfa)
    show(dfa)
