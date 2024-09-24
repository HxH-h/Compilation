from NFA import NFA
from Edge import Edge
class DFA:
    def __init__(self , nfa: NFA):
        # 定义五元组
        self.status = nfa.status
        self.symbols = nfa.symbol.copy()
        self.symbols.discard('#')
        self.edges = nfa.edges
        self.start = nfa.start
        # 由于NFA的终点集只有一个元素，所以直接pop
        self.end = nfa.end.pop()
        print(self.end)
        self.status , self.edges , self.end = self.NFAtoDFA()


    # 状态转移函数
    def StatusMove(self , status: set, symbol) -> set:
        nextStatus = set()
        # 遍历状态集
        for s in status:
            for edge in self.edges:
                if edge.start == s and edge.symbol == symbol:
                    nextStatus.add(edge.end)

        return nextStatus

    # 闭包函数
    def Closure(self , status: set) -> set:
        closure = set()
        stack = list(status)

        #加入状态本身
        for s in status:
            closure.add(s)
        #求空闭包
        while stack:
            top = stack.pop()
            for edge in self.edges:
                if edge.start == top and edge.symbol == '#':
                    if edge.end not in closure:
                        closure.add(edge.end)
                        stack.append(edge.end)
        return closure

    # NFA 转 DFA
    def NFAtoDFA(self) :
        stausNum = 0
        # DFA状态集
        dfaStatus = {}
        # DFA映射集
        dfaEdges = []

        #DFA 终点集
        dfaEnd = set()

        # 求初始状态的闭包集
        startStatus = self.Closure({self.start})
        dfaStatus[tuple(startStatus)] = stausNum
        self.start = stausNum
        # 判断是否为终止状态
        if self.end in startStatus:
            dfaEnd.add(stausNum)
        stausNum += 1

        # 未处理的状态集
        stack = [startStatus]

        # 外层对所有状态集进行遍历
        while stack:
            status = stack.pop()
            # 内层对所有状态转移符号集进行遍历

            for symbol in self.symbols:
                #  求目标状态集
                nextStatus = self.StatusMove(status , symbol)

                # 求目标状态集的闭包集
                nextStatus = self.Closure(nextStatus)


                # 看目标状态集是否为空 且 是否在所有状态集中，不在 且 不为空则加入
                if nextStatus and tuple(nextStatus) not in dfaStatus:
                    stack.append(nextStatus)
                    dfaStatus[tuple(nextStatus)] = stausNum
                    # 判断是否为终止状态
                    if self.end in nextStatus:
                        dfaEnd.add(stausNum)
                    # 添加边
                    dfaEdges.append(Edge(dfaStatus[tuple(status)], stausNum, symbol))
                    stausNum += 1
                elif nextStatus:
                    dfaEdges.append(Edge(dfaStatus[tuple(status)] , dfaStatus[tuple(nextStatus)] , symbol))
        # 构建DFA
        print(dfaEnd)
        return dfaStatus.values(),dfaEdges,dfaEnd
    def __str__(self):
        ret = ""
        for edge in self.edges:
            ret += edge.__str__() + "\n"
        return ret