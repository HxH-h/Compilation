from Rule import *


# 预处理 将字符串规则转为Rule对象
#       获取所有非终结符

# rule: 规则字符串
# seg: 规则间的分隔符
# der: 使用的推导符号
# return: Rule集合 非终结符列表
def preProcess(rule: str, seg: str, der: str):
    # 分割出一条规则
    rule = rule.replace(" ", "")
    rules = rule.split(seg)
    ret = []
    noEnd = []
    for r in rules:
        # 一条规则分左 右 部
        r = r.split(der)

        # 左部为 非终结符
        noEnd.append(r[0])

        # 右部可能有多个
        ret.append(Rule(r[0], r[1].split('|')))
    return ret, noEnd


# TODO 有问题
# 消除左递归
# Param : unEnd  非终结符集合
# Param : rules 规则集合
def RmLRecursion(unEnd: list, rules: list):
    # 消除间接左递归
    # 遍历每一个非终结符
    for i in range(len(unEnd)):
        # 看左部为i,右部含有j的规则
        for j in range(i):
            for r in rules:
                if r.left == unEnd[i]:
                    # 遍历右部每个可能的推导结果
                    for rr in r.right:
                        if unEnd[j] == rr[0]:
                            newRight = replace(unEnd[j], rr, rules)
                            # 将新的推导结果加入到右部中
                            r.right.extend(newRight)
                            # 去除原来的推导结果
                            r.right.remove(rr)

    # 消除直接左递归
    newRules = set()
    for rule in rules:
        # 获取规则的递归和非递归部分
        rec, nonRec = hasRecursion(rule)
        if rec:
            # 添加新规则R'
            # 非递归部分尾接R'
            newNonRec = set()
            for nr in nonRec:
                nr += (rule.left + '\'')
                newNonRec.add(nr)
            rule.right = newNonRec
            # 递归部分 R换位R' 并到结果式的最右边
            newRec = set()
            for rr in rec:
                rr += (rule.left + '\'')
                newRec.add(rr[1:])
            newRec.add('ε')
            newRules.add(Rule(rule.left + '\'', newRec))
    rules.extend(newRules)
    print(rules)


# 消除间接递归 进行替换
# Param : replaced 被替换的非终结符
# Param : right 右部集合
def replace(replaced: str, right: str, rules: list):
    # 获取replaced所能推导出的所有规则
    derivation = []
    for r in rules:
        if r.left == replaced:
            derivation.extend(r.right)
    newRight = set()

    # 将所有推导结果均进行一次替换
    for der in derivation:
        # temp 临时存储替换后的结果
        temp = right.replace(replaced, der)
        newRight.add(temp)
    return newRight


#   分离出递归项和非递归项
def hasRecursion(rule: Rule):
    rec = set()
    left = rule.left
    for r in rule.right:
        if left == r[0]:
            rec.add(r)
    return rec, set(rule.right) - rec


# TODO 优化求first集，每个first集只求一遍
# 获取非终结符的first集
# @param : char  非终结符
# @param : rules 规则集合
# @param : noEnd 非终结符集合
# rules中的每个rule左部应该唯一
def getFirst(char: str, rules: list, noEnd: list):
    first = set()
    # 求对应终结符的产生式
    right = []
    for rule in rules:
        if rule.left == char:
            right.extend(rule.right)
    # 遍历每个产生式
    for r in right:
        # 终结符直接加入first集
        if r[0] not in noEnd:
            first.add(r[0])
        else:
            # 终结符则递归求first集
            for i in range(len(r)):
                if r[i] in noEnd:
                    # 临时存储递归的first集
                    temp = getFirst(r[i], rules, noEnd)
                    first.update(temp - set('ε'))
                    # 若所有非终结符都可以产生空集，则加入first集
                    if i == len(r) - 1 and 'ε' in temp:
                        first.add('ε')
                    # 判断是否有空集
                    if 'ε' not in temp:
                        break
                else:
                    first.add(r[i])
                    break
    return first


def getFirstSet(noEnd: list, rules: list):
    ret = {}
    for char in noEnd:
        ret[char] = getFirst(char, rules, noEnd)
    return ret


# 获取非终结符的follow集
# @param : rules 规则集合
# @param : noEnd 非终结符集合
# @param : start: 开始符
def getFollow(rules: list, noEnd: list , start: str):
    follow = {}
    # 初始化所有非终结符的follow集为空集
    for char in noEnd:
        follow[char] = set()
    # 开始符加入$
    follow[start] = set('$')
    preCnt = -1
    Cnt = countDict(follow)
    # 循环直到follow集不再变化
    while preCnt != Cnt:
        preCnt = Cnt
        for rule in rules:
            # 遍历每一条产生式
            for r in rule.right:
                for i in range(len(r)):
                    # 若为非终结符
                    if r[i] in noEnd:
                        # 若为最后一个，则加入左部的follow集
                        if i == len(r) - 1:
                            follow[r[i]].update(follow[rule.left])
                        elif i == len(r) - 2 and 'ε' in getFirst(r[i + 1], rules, noEnd):
                            follow[r[i]].update(getFirst(r[i + 1], rules, noEnd) - set('ε'))
                            follow[r[i]].update(follow[rule.left])
                        else:
                            # 若为非终结符，则加入其first集去除ε
                            if r[i + 1] in noEnd:
                                temp = getFirst(r[i + 1], rules, noEnd)
                                follow[r[i]].update(temp - set('ε'))
                            # 若为终结符，则加入该终结符
                            else:
                                follow[r[i]].add(r[i + 1])
        Cnt = countDict(follow)
    return follow


def countDict(follow: dict):
    count = 0
    # 计算键值的个数
    for k, v in follow.items():
        count += 1
        count += len(v)
    return count


if __name__ == '__main__':
    #rule = "E -> TE' ; E' -> +TE'|ε ; T -> FT' ; T' -> *FT'|ε ; F -> (E) | i"
    # rule = "S -> ABC; A -> a|ε ;B -> b|ε; C -> c|ε"
    rule = input("请输入规则:")
    rules, noEnd = preProcess(rule, ";", "->")
    print(getFollow(rules, noEnd ,'E' ))


