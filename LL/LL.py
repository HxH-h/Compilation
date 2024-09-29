from Rule import *
# 预处理 将字符串规则转为Rule对象
#       获取所有非终结符

# rule: 规则字符串
# seg: 规则间的分隔符
# der: 使用的推导符号
# return: Rule集合 非终结符列表
def preProcess(rule: str , seg: str , der: str):
    # 分割出一条规则
    rule = rule.replace(" ","")
    rules = rule.split(seg)
    ret = []
    noEnd = []
    for r in rules:
        # 一条规则分左 右 部
        r = r.split(der)

        # 左部为 非终结符
        noEnd.append(r[0])

        # 右部可能有多个
        ret.append(Rule(r[0] , r[1].split('|')))
    return ret , noEnd

# 消除左递归
# Param : unEnd  非终结符集合
# Param : rules 规则集合
def RmLRecursion(unEnd: list , rules: list):
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
                            newRight = replace(unEnd[j] , rr , rules)
                            # 将新的推导结果加入到右部中
                            r.right.extend(newRight)
                            # 去除原来的推导结果
                            r.right.remove(rr)

    # 消除直接左递归
    newRules = set()
    for rule in rules:
        # 获取规则的递归和非递归部分
        rec , nonRec = hasRecursion(rule)
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
def replace(replaced: str , right: str , rules: list):
    # 获取replaced所能推导出的所有规则
    derivation = []
    for r in rules:
        if r.left == replaced:
            derivation.extend(r.right)
    newRight = set()

    # 将所有推导结果均进行一次替换
    for der in derivation:
        # temp 临时存储替换后的结果
        temp = right.replace(replaced , der)
        newRight.add(temp)
    return newRight

#   分离出递归项和非递归项
def hasRecursion(rule: Rule):
    rec = set()
    left = rule.left
    for r in rule.right:
        if left == r[0]:
            rec.add(r)
    return rec , set(rule.right) - rec






if __name__ == '__main__':
    rule = " A -> Ab | Bb ; B -> Ba | Ca ; C -> Cb | d"
    rules , noEnd = preProcess(rule , ";" , "->")
    RmLRecursion(noEnd,rules)


