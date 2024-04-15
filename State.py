class State:
    def __init__(self, label, Out_Edges=[], parents=[], is_start=False, is_accept=True):
        self.label = label
        self.parents = parents
        self.Out_Edges = Out_Edges
        self.is_start = is_start
        self.is_accept = is_accept

    def add_Edge(self, symbol, state):
        self.Out_Edges.append((symbol, state))
        self.is_accept = False
        state.parents.append(self)

    def get_parents(self):
        return self.parents.copy()