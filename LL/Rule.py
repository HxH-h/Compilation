class Rule:
    def __init__(self , left: str , right: set):
        self.left = left
        self.right = right
    def __str__(self):
        return self.left + " -> " + " |".join(self.right) +" "
    def __repr__(self):
        return self.__str__()