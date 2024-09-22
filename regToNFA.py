from NFA import *
from pyecharts import options as opt
from pyecharts.charts import Graph
import webbrowser


# 预处理输入的正则表达式
# 1.将隐式的连接符号 显式拼接上
# 2.将中缀表达式转换为后缀表达式

# TODO 允许多个终止态

def preprocess(regex):
    # 添加连接符号
    regex = add_Union_Symbol(regex)
    # 转换为后缀表达式
    return InfixToPostfix(regex)


# 添加连接符号
def add_Union_Symbol(regex):
    # 字符串长度小于2，不需要处理
    if len(regex) < 2:
        return regex
    ret = ""
    for i in range(0, len(regex) - 1):
        first = regex[i]
        second = regex[i + 1]

        ret += first
        # 两个字符之间需要加连接符号
        if (second.isalpha() and first != '(' and first != '|'):
            ret += '+'
        if (second == '(' and first != '(' and first != '|'):
            ret += '+'
    # 最后一个字符
    ret += second
    return ret


# 中缀表达式转后缀表达式
def InfixToPostfix(regex):
    # 优先级 括号栈内优先级最低
    priority = {'|': 1, '+': 2, '*': 3, '(': 0}
    stack = []
    postfix = ""
    for i in range(0, len(regex)):
        if regex[i].isalpha():
            postfix += regex[i]
        # 遇到左括号直接入栈
        elif regex[i] == '(':
            stack.append(regex[i])
        elif regex[i] == ')':
            while stack[-1] != '(':
                postfix += stack.pop()
            stack.pop()
        else:
            while stack and priority[regex[i]] <= priority[stack[-1]]:
                postfix += stack.pop()
            stack.append(regex[i])
    while stack:
        postfix += stack.pop()
    return postfix


def ToNFA(regex):
    stack = []
    statusNum = 0
    for i in range(0, len(regex)):
        if regex[i].isalpha():
            # 构建出一个新的NFA状态 并 压栈
            stack.append(Element(Edge(statusNum, statusNum + 1, regex[i])))
            # 更新状态数量
            statusNum += 2
        elif regex[i] == '+':
            # 连接区分先后顺序
            # 从栈中弹出两个NFA状态
            second = stack.pop()
            first = stack.pop()

            # 构建新的NFA状态
            for i in range(0, len(second.edges)):
                if second.edges[i].getStart() == second.start:
                    second.edges[i].setStart(first.end)
                elif second.edges[i].getEnd() == second.start:
                    second.edges[i].setEnd(first.end)
            first.end = second.end
            first.edges.extend(second.edges)
            stack.append(first)
        elif regex[i] == '|':
            second = stack.pop()
            first = stack.pop()

            # 创建新的四条边,并更新first和second的start和end
            Edge_sf = Edge(statusNum, first.start, '#')
            Edge_se = Edge(statusNum, second.start, '#')
            first.start = statusNum
            second.start = statusNum
            statusNum += 1

            Edge_ef = Edge(first.end, statusNum, '#')
            Edge_es = Edge(second.end, statusNum, '#')
            first.end = statusNum
            second.end = statusNum
            statusNum += 1

            # 形成新的NFA状态
            first.edges.append(Edge_sf)
            first.edges.append(Edge_se)
            first.edges.append(Edge_ef)
            first.edges.append(Edge_es)
            first.edges.extend(second.edges)

            # 入栈
            stack.append(first)

        elif regex[i] == '*':
            status = stack.pop()
            # 先将旧状态闭环
            Edge_se = Edge(status.end, status.start, '#')
            status.edges.append(Edge_se)
            # 创建新的start和end状态 形成闭包

            # 保存之前的start和end状态
            old_start = status.start
            old_end = status.end
            # 更新start和end状态
            status.start = statusNum
            status.end = statusNum + 1

            # 创建新的两条边
            Edge_ss = Edge(status.start, old_start, '#')
            Edge_ee = Edge(old_end, status.end, '#')

            Edge_newse = Edge(status.start, status.end, '#')
            status.edges.append(Edge_newse)
            status.edges.append(Edge_ss)
            status.edges.append(Edge_ee)

            stack.append(status)
            statusNum += 2
        else:
            print("Invalid character")
            return

    return stack.pop()


def show(NFA):
    # 集合存储节点，节点不重复
    nodeset = set()
    links = []
    for i in range(0, len(NFA.edges)):
        edge = NFA.edges[i]
        nodeset.add(edge.getStart())
        nodeset.add(edge.getEnd())
        # 添加边
        links.append({"source": str(edge.getStart()),
                      "target": str(edge.getEnd()),
                      "label": {"show": True, "formatter": edge.getSymbol()},
                      "lineStyle": {"curveness": 0.3}
                      })

    # 节点集转换为list
    nodes = []
    for node in nodeset:
        if node == NFA.end:
            nodes.append({
                "name": str(node),
                "symbolSize": 25,
                "x": 1500,
                "y": 250,
                "fixed": "true",
                "itemStyle": {
                    "color": "#2f4554",
                    "borderColor": "#000",
                    "borderWidth": 4,
                    "borderType": "solid",
                    "shadowBlur": 10,
                    "shadowColor": "rgba(0, 0, 0, 0.5)"
                }
            })
        else:
            nodes.append({"name": str(node),
                          "symbolSize": 25,
                          })
    # 添加起始状态
    nodes.append({"name": "S",
                  "symbolSize": 25,
                  "x": 100,
                  "y": 250,
                  "fixed": "true"
                  })
    links.append({"source": "S",
                  "target": str(NFA.start),
                  "label": {"show": True, "formatter": 'start'},
                  })

    # 绘制关系图
    graph = Graph(init_opts=opt.InitOpts(width="90vw", height="80vh"))
    graph.add("",
              nodes,
              links,
              is_focusnode=False,
              edge_symbol=['none', 'arrow'],
              repulsion=8000)
    graph.set_global_opts(title_opts=opt.TitleOpts(title="NFA"))
    graph.render("NFA.html")


if __name__ == '__main__':
    regex = "a*"
    show(ToNFA(preprocess(regex)))
    print("done！")
    # 浏览器自动打开展示结果
    webbrowser.open("NFA.html")
