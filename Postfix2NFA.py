import graphviz
from State import State 

class NFA:
    def __init__(self, start=None, accept=None, postfix=None):
        self.start = start
        self.accept = accept
        if not start and not accept and postfix:
            obj = self.Postfix2NFA(postfix)
            self.start = obj.start
            self.accept = obj.accept
    #Shunting Yard Algorithm            
    def Postfix2NFA(self, postfix):
        NFA_Stack = []
        idx = 0
        for chr_posfix in postfix:
            if chr_posfix == '*':
                First_NFA_Operand = NFA_Stack.pop()
                start = State('S' + str(idx))
                accept = State('S' + str(idx + 1))
                
                start.add_Edge('ϵ', First_NFA_Operand.start)
                start.add_Edge('ϵ', accept)
                
                First_NFA_Operand.accept.add_Edge('ϵ', start)
                First_NFA_Operand.accept.add_Edge('ϵ', accept)
                
                NFA_Stack.append(NFA(start, accept))
                idx += 2

            elif chr_posfix == '+':
                First_NFA_Operand = NFA_Stack.pop()
                start = State('S' + str(idx))
                accept = State('S' + str(idx + 1))
                
                start.add_Edge('ϵ', First_NFA_Operand.start)
                
                First_NFA_Operand.accept.add_Edge('ϵ', start)
                First_NFA_Operand.accept.add_Edge('ϵ', accept)
                
                NFA_Stack.append(NFA(start, accept))
                idx += 2

            elif chr_posfix == '?':
                First_NFA_Operand = NFA_Stack.pop()
                start = State('S' + str(idx))
                accept = State('S' + str(idx + 1))
                
                start.add_Edge('ϵ', First_NFA_Operand.start)
                start.add_Edge('ϵ', accept)
                
                First_NFA_Operand.accept.add_Edge('ϵ', accept)
                
                NFA_Stack.append(NFA(start, accept))
                idx += 2

            elif chr_posfix == '.':
                First_NFA_Operand = NFA_Stack.pop()
                Second_NFA_Operand =   NFA_Stack.pop()
                
                Second_NFA_Operand.accept.add_Edge('ϵ', First_NFA_Operand.start)
                NFA_Stack.append(NFA(Second_NFA_Operand.start, First_NFA_Operand.accept))

            elif chr_posfix == '|':
                First_NFA_Operand = NFA_Stack.pop()
                Second_NFA_Operand =  NFA_Stack.pop()
                
                start = State('S' + str(idx))
                accept = State('S' + str(idx + 1))
                
                start.add_Edge('ϵ', Second_NFA_Operand.start)
                start.add_Edge('ϵ', First_NFA_Operand.start)
                
                Second_NFA_Operand.accept.add_Edge('ϵ', accept)
                First_NFA_Operand.accept.add_Edge('ϵ', accept)
                
                NFA_Stack.append(NFA(start, accept))
                idx += 2

            else:
                start = State('S' + str(idx))
                accept = State('S' + str(idx + 1))
                
                start.add_Edge(chr_posfix, accept)
                
                NFA_Stack.append(NFA(start, accept))
                idx += 2

        return NFA_Stack.pop()   

    # For Converting  NFA to JSON format
    def NFA_JSON_Converter(self):
        #Get States
        states = []
        visited = set()
        queue = [self.start]
        visited.add(self.start)
        while queue:
            state = queue.pop(0)
            states.append(state)
            for (Out_Edge) in state.Out_Edges:
                if Out_Edge[1] not in visited:
                    visited.add(Out_Edge[1])
                    queue.append(Out_Edge[1])        
        
        JSON_states = {}
        for state in states:
            state_dict = {
                'isTerminatingState': state.is_accept,
            }
            for symbol, next_state in state.Out_Edges:
                if symbol not in state_dict:
                    state_dict[symbol] = next_state.label
                else:
                    state_dict[symbol] += ',' + next_state.label
            JSON_states[state.label] = state_dict

        return {
            'startingState': self.start.label,
            **JSON_states,
        }
    
    def NFA_Graph(self, name='output_folder/NFA.gv', view=False):
        NFA_JSON = self.NFA_JSON_Converter()
        graph = graphviz.Digraph(engine='dot',graph_attr={'rankdir':'LR'})
        for state, Edges in NFA_JSON.items():
            if state == 'startingState':
                #graph.node("", _attributes={'shape' : 'none'})
                #graph.edge("", state.label)                
                continue
            if Edges['isTerminatingState']:
                graph.node(state, shape='doublecircle')
            else:
                graph.node(state, shape='circle')
                
            for symbol, next_state in Edges.items():
                if symbol == 'isTerminatingState':
                    continue
                children_states = next_state.split(',')
                for child in children_states:
                    graph.edge(state, child, label=symbol)
        graph.render(name, view=view)
        return graph      
        
        
        
