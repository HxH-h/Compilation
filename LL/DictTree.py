from Rule import *
class Node:

    # @param char: str 节点代表的字符
    # @param der: str 若该节点为产生式的终点，则存储产生式，否则为none
    # @param children: dict 子节点字典 key: 26个字母 value: Node
    def __init__(self , char: str , der: str = None):
        self.char = char
        self.der = der
        self.children = {}
    def setDer(self , der: str):
        self.der = der

class DictTree:

    # @param left: str 对应产生式集的左部
    # @param der: str 待构造的树对应的产生式集
    def __init__(self ,left: str , der: list):
        self.left = left
        self.root = Node('')
        for i in der:
            self.insert(i)

    # 将产生式插入树中
    # @param der: str 待插入的产生式
    def insert(self, der: str):
        p = self.root
        for i in range(len(der) - 1):
            # 若该字符节点不存在，则创建
            if der[i] not in p.children.keys():
                p.children[der[i]] = Node(der[i])
            # 移动到下一个节点
            p = p.children[der[i]]
        # 结尾节点存储产生式
        # 若该字符节点已存在，则覆盖 , 不存在则覆盖
        if der[-1] not in p.children.keys():
            p.children[der[-1]] = Node(der[-1], der)
        else:
            p.children[der[-1]].setDer(der)

    # 提取左公共因子
    # @param depth: int 当前深度
    # @param node: Node 当前节点
    # @param ret: dict  存储提取完公共因子的结果 ， key: 新的规则的左部，value: 结果
    # @return: str     返回可能还可以被提取的推导式
    def extractFactor(self , depth: int ,node: Node , ret: dict):
        # 递归出口 没有孩子则为叶子节点
        if not node.children:
            # 叶子节点必为推导式的结尾,der必不为None
            return node.der

        childProduction = []
        for n in node.children.values():
            # 后序遍历
            prod = self.extractFactor(depth + 1, n , ret)
            childProduction.append(prod)

        # 根节点没有公因式，不需要提取，直接作为结果
        if node.char == '':
            ret[self.left] = childProduction
            return

        # 看当前节点是否为一个推导式的结尾
        if node.der:
            childProduction.append(node.der)

        # 只有一个产生式，不用提公因子
        if len(childProduction) == 1:
            return childProduction[0]

        # 提取公共因子 , depth的值为公共前缀的长度
        prefix = childProduction[0][:depth]

        # 存储提取后的结果
        temp = set()
        for prod in childProduction:
            if prod[depth:]:
                temp.add(prod[depth:])
            else:
                temp.add('ε')
        # 找一个字典中没有用过的左部
        key = self.left + (len(ret) + 1) * '`'
        ret[key] = temp

        return prefix + key

    # 提取公共因子，获取结果并封装成Rule
    def getRet(self):
        ret = {}
        tree.extractFactor(0, tree.root, ret)
        return [Rule(k,v) for k,v in ret.items()]





if __name__ == '__main__':
    tree = DictTree('S',['aaB','aaaC','aaaD','cd'])
    print(tree.getRet())




