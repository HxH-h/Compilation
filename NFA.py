class Edge:
    # 起点，终点和转换符
    def __init__(self, start , end , symbol):
        self.start = start
        self.end = end
        self.symbol = symbol
    def getStart(self):
        return self.start
    def getEnd(self):
        return self.end
    def getSymbol(self):
        return self.symbol
    def setStart(self, start):
        self.start = start
    def setEnd(self, end):
        self.end = end
    def __str__(self):
        return str(self.start) + '->' + str(self.end) + ':' + self.symbol

class Element:
    # NFA的起始状态和结束状态
    def __init__(self, edge):
        self.edges = [edge]
        self.start = edge.getStart()
        self.end = edge.getEnd()
    # 添加边
    def addEdge(self, edge):
        self.edges.append(edge)
    # 更改起始状态
    def setStart(self, start):
        self.start = start
    # 更改结束状态
    def setEnd(self, end):
        self.end = end
