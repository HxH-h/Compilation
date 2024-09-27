from NFA import NFA
from Edge import Edge
from collections import deque
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

        self.status , self.edges , self.end = self.NFAtoDFA()

        # DFA最简化
        self.Minimize()



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

    # 获取终点
    def getEnd(self,start , symbol):
        for edge in self.edges:
            if edge.start == start and edge.symbol == symbol:
                return edge.end
        return None

    # 判断状态属于哪个组
    def belong(self, status, symbol, group: dict):
        end = self.getEnd(status, symbol)
        if end is None:
            return -1
        for k, g in group.items():
            if end in g:
                return k

    # 分组
    def seperate(self, group, symbol, groupId):
            # 组 队列
            q = deque()
            q.extend(group.values())
            # 划分新的组
            retGroup = {}

            # 划分到最小停止
            while q:
                g = q.popleft()
                # 存储状态的临时分组
                newDict = {}
                for status in g:
                    # 按原分组区分 ， 获取组号
                    bel = self.belong(status, symbol, group)

                    if bel not in newDict.keys():
                        newDict[bel] = set()
                    # 加入对应分组
                    newDict[bel].add(status)

                if len(newDict.keys()) > 1:
                    # 从原分组中去除
                    for k, v in group.items():
                        if v == g:
                            del group[k]
                            break

                    for g in newDict.values():
                        group[groupId] = g
                        groupId += 1
                        q.append(g)
                else:
                    if len(retGroup) == 0:
                        retGroup[0] = newDict.get(next(iter(newDict)))
                    else:
                        retGroup[max(retGroup.keys()) + 1] = newDict.get(next(iter(newDict)))

            # 返回新分组和当前最新组号
            return retGroup, groupId

    # DFA 最简化
    def Minimize(self):
            groupID = 0
            # 分终结和非终结两组
            end = self.end
            noend = set()
            for edge in self.edges:
                if edge.start not in self.end:
                    noend.add(edge.start)
                if edge.end not in self.end:
                    noend.add(edge.end)
            # 如果只有一个组
            if len(end) == 0 or len(noend) == 0:
                return
            # 使用字典存储不同的组
            group = {0: end, 1: noend}
            groupID = 2
            for c in self.symbols:
                group, groupID = self.seperate(group, c, groupID)
                print(c, group)

            # 更新start
            for k, v in group.items():
                if self.start in v:
                    self.start = k
            # 更新end
            newEnd = set()
            for k,v in group.items():
                if self.end.intersection(set(v)):
                    newEnd.add(k)
            self.end = newEnd
            # 更新status
            self.status = group.keys()

            # 更新边
            newEdges = set()
            for edge in self.edges:
                start = edge.start
                end = edge.end
                for k, v in group.items():
                    if start in v:
                        edge.start = k
                    if end in v:
                        edge.end = k
                newEdges.add(edge)
            self.edges = newEdges

            for edge in self.edges:
                print(edge)
            return group

    def __str__(self):
        ret = ""
        for edge in self.edges:
            ret += edge.__str__() + "\n"
        return ret