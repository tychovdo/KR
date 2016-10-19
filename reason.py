import itertools
import graphviz as gv

class CausalModel():
    def __init__(self):
        self.quantities = []
        self.influences = []
        self.proportionals = []
        self.value_cors = []
        self.states = []

    def add_quantity(self, name, m_space, d_space):
        self.quantities.append((name, m_space, d_space))

    def add_infl_rel(self, src, dst, amount):
        self.influences.append((src, dst, amount))

    def add_prop_rel(self, src, dst, amount):
        self.proportionals.append((src, dst, amount))

    def add_value_cor(self, q1, m1, q2, m2):
        self.value_cors.append((q1, m1, q2, m2))

    def next_states(self, s):
        next_states = []

        # Remove illegal states
        def is_legal(state):
            for i in range(len(state)):
                q, m, d = state[i]
                name, m_space, d_space = self.quantities[i]
                if (m_space.index(m) + d < 0):            # No underflow
                    return False
                if (m_space.index(m) + d > len(m_space)): # No overflow
                    return False

#           # Check value correlations
#           for (q1, m1, q2, m2) in self.value_cors:
#               q1i = [x[0] for x in self.quantities].index(q1)
#               q2i = [x[0] for x in self.quantities].index(q2)
#               if state[q1i][1] == m1 and not state[q2i][1] == m2:
#                   return False

#               if state[q2i][1] == m2 and not state[q1i][1] == m1:
#                   return False
            return True

        if not is_legal(s):
            return False

        # Calculate new magnitude space
        new_m_spaces = []
        for i in range(len(s)):
            q, m, d = s[i]
            name, m_space, d_space = self.quantities[i]
            new_m_space = []

            if(0 < m_space.index(m)):
                new_m_space.append(m)

            if(0 <= m_space.index(m) + d < len(m_space)):
                new_m_space.append(m_space[m_space.index(m) + d])

            new_m_spaces.append(new_m_space)


        # Calculate new derivative space (inflow adjust)
        new_d_spaces = []
        for i in range(len(s)):
            q, m, d = s[i]
            new_d_space = [d]

            if(i == 0): # Inflow adjust
                for new_d in range(d - 1, d + 2):
                    if new_d in d_space:
                        if not (m_space.index(m) + new_d < 0):                # No underflow
                            if not (m_space.index(m) + new_d > len(m_space)): # No overflow
                                new_d_space.append(new_d)
            new_d_spaces.append(new_d_space)


        # Generate next possible states situations
        new_tmp = []
        for i in range(len(new_m_spaces)):
            pos = [s[i][0]], new_m_spaces[i], new_d_spaces[i]
            new_tmp.append(list(itertools.product(*pos)))
        new_tmp = list(itertools.product(*new_tmp))

        for new_state in new_tmp:
            next_state = [list(x) for x in new_state]
            next_states.append(next_state)

 #      # Apply influencial relationship
 #      for src, dst, amount in self.influences:
 #          src_i = [x[0] for x in self.quantities].index(src)
 #          dst_i = [x[0] for x in self.quantities].index(dst)
 #          for i in range(len(next_states)):
 #              if self.quantities[src_i][1].index(next_states[i][src_i][1]) > 0:
 #                  next_states[i][dst_i][2] = amount
 
#       # Apply proportional relationship (fakey)
#       for src, dst, amount in self.proportionals:
#           src_i = [x[0] for x in self.quantities].index(src)
#           dst_i = [x[0] for x in self.quantities].index(dst)
#           for i in range(len(next_states)):
#               if(amount > 0): # todo negative prop
#                   if next_states[i][src_i][1] == '+':
#                       next_states[i][dst_i][1] == '+' # todo multiple positives

        legals = [x for x in next_states if is_legal(x)]

        return legals

    def reason(self):
        g = gv.Digraph(format='svg')

        # Generate possible states
        self.states = []
        for [name, m_space, d_space] in self.quantities:
            s = (name, m_space, d_space)
            self.states.append(list(itertools.product(*s)))
        self.states = list(itertools.product(*self.states))

#        self.states = self.states[342:343]

#       for i in range(len(self.states)):
#           print("{:4} : {}".format(i, self.states[i]))

        # Generate possible transitions
        self.transitions = []
        num_states = 0
        for s in self.states:
            # Find next states
            next_states = self.next_states(s)

            # Add next states to graph
            if next_states != False:
                list_s = [list(x) for x in s]
                g.node(self.to_str(list_s))
                num_states += 1
                for n in next_states:
                    self.transitions.append((self.to_str(list_s), self.to_str(n)))

        # Remove duplicates
        print(len(self.transitions))
        self.transitions = list(set(self.transitions))
        print(len(self.transitions))
        for (a, b) in self.transitions:
            g.edge(a, b)

        # Plot
        styles = {
            'graph': {
                'label': 'Causal model',
                'fontsize': '15',
                'fontcolor': '#999999',
                'bgcolor': '#ffffff',
            },
            'nodes': {
                'fontname': 'Monospace',
                'shape': 'circle',
                'fontcolor': 'white',
                'fontsize': '10',
                'color': 'white',
                'style': 'filled',
                'fillcolor': '#006699',
            },
            'edges': {
                'color': '#999999',
                'arrowhead': 'open',
                'fontname': 'Helvetica',
                'fontsize': '12',
                'fontcolor': '#999999',
            }
        }

        g.graph_attr.update(
            ('graph' in styles and styles['graph']) or {}
        )
        g.node_attr.update(
            ('nodes' in styles and styles['nodes']) or {}
        )
        g.edge_attr.update(
            ('edges' in styles and styles['edges']) or {}
        )

        filename = g.render(filename='stategraph')
        print("States: ", num_states)
        print("Graph:  ", filename)

    def to_str(self, s):
        out = ""
        for (q, m, d) in s:
            out += "{}|{} {:2}\n".format(q, m, d)
        return out


def main():
    # Define causal model
    cm = CausalModel()
    cm.add_quantity("I", ["0", "+"], [-1, 0, 1])
    cm.add_quantity("V", ["0", "+", "m"], [0, -1, 1])
    cm.add_quantity("O", ["0", "+", "m"], [0, -1, 1])
    cm.add_infl_rel("I", "V", 1)
    cm.add_infl_rel("O", "V", -1)
    cm.add_prop_rel("V", "O", 1)
    cm.add_value_cor("V", "m", "O", "m")
    cm.add_value_cor("V", "0", "O", "0")

    # Generate state graph
    cm.reason()

if __name__=="__main__":
    main()
