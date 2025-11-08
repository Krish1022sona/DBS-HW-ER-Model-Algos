class FD:
    def __init__(self, lhs: set[str], rhs:set[str]):
        self.lhs = lhs
        self.rhs = rhs
    
    def printFD(self):
        print(f"{self.lhs} -> {self.rhs}")

    