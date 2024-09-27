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