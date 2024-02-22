class Tree:
    def __init__(self):
        self.branches = []
        self.name = ''

    def add_branch(self, branch):
        self.branches.append(branch)

    def _to_wolfram(self) -> str:
        branches = [b._to_wolfram() for b in self.branches]
        if len(branches) == 0:
            return f'"{self.name}"'
        else:
            return f'"{self.name}"[{", ".join(branches)}]'

    def to_wolfram(self) -> str:
        return f'TreeForm[{self._to_wolfram()}]'
