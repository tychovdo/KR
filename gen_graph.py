import itertools
import graphviz as gv
import math
import time

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


    def print_model(self):
        print("=============== CAUSAL MODEL ===============")
        print("QUANTITIES")
        print("name            values               derivatives")
        for (name, m_space, d_space) in self.quantities:
            print("{:15} {:20} {:20}".format(name, str(m_space), str(d_space)))

        print("\nINFLUENCIAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.influences:
            print("{:15} {:1} {:10}".format(src, dst, amount))

        print("\nPROPORTIONAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.proportionals:
            print("{:15} {:1} {:10}".format(src, dst, amount))

        print("\nVALUE CORRESPONDENCES")
        for (src, src_amount, dst, dst_amount) in self.value_cors:
            print("{}({})   = {}({})".format(src, src_amount, dst, dst_amount))
        print("============================================")

    def next_states(self, s):
        # Remove illegal states
        def is_legal(state):
            for i in range(len(state)):
                q, m, d = state[i]
                name, m_space, d_space = self.quantities[i]
                if (m_space.index(m) + d < 0):            # No underflow
                    return False
                if (m_space.index(m) + d > len(m_space)): # No overflow
                    return False

            # Check value constraints
            for (q1, m1, q2, m2) in self.value_cors:
                q1i = [x[0] for x in self.quantities].index(q1)
                q2i = [x[0] for x in self.quantities].index(q2)
                if state[q1i][1] == m1 and not state[q2i][1] == m2:
                    return False
                if state[q2i][1] == m2 and not state[q1i][1] == m1:
                    return False
            
            # Apply influencial relationship
            for i in range(len(state)):
                q, m, d = state[i]

                pos_ds = self.quantities[i][2]
                inf_ds = []
                for src, dst, amount in self.influences:
                    src_i = [x[0] for x in self.quantities].index(src)
                    dst_i = [x[0] for x in self.quantities].index(dst)
                    if(dst == q):
                        a = state[src_i][1]
                        a_int = +1
                        if(a == '-'):
                            a_int = -1
                        if(a == '0'):
                            a_int = 0
                        # if(a_int * amount != 0):
                        inf_ds.append(a_int * amount)
                
                if (0 in inf_ds and len(inf_ds) > 1):
                    inf_ds.remove(0)

                if inf_ds != []:
                    pos_ds = list(range(min(inf_ds), max(inf_ds) + 1))
                    if d not in pos_ds:
                        return False

            # Apply proportionality constraints
            for src, dst, amount in self.proportionals:
                src_i = [x[0] for x in self.quantities].index(src)
                dst_i = [x[0] for x in self.quantities].index(dst)
                d1 = state[src_i][2]
                d2 = state[dst_i][2]
                if(d1 != d2):
                    return False

            return True

        if not is_legal(s):
            return False

        next_states = []

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
            else:
                if(q != 'I'):
                    return [] # todo

            new_m_spaces.append(new_m_space)

        # Calculate new derivative space
        new_d_spaces = []
        for i in range(len(s)):
            q, m, d = s[i]
            new_d_space = [d]

            # Derivative
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

        legals = [x for x in next_states if is_legal(x)]

        return legals

    def reason(self):
        # Print system description
        self.print_model()


        # Generate possible states
        print("Generating states...")
        time_start = time.time()
        self.all_states = []
        for [name, m_space, d_space] in self.quantities:
            s = (name, m_space, d_space)
            self.all_states.append(list(itertools.product(*s)))
        self.all_states = list(itertools.product(*self.all_states))
        print("All states:      ", len(self.all_states))

        # Generate possible transitions
        print("Generating successor states...")

        transitions = []
        num_states = 0
        for s in self.all_states:
            # Find next states
            next_states = self.next_states(s)

            # Add next states to graph
            if next_states != False:
                num_states += 1
                list_s = [list(x) for x in s]
                for n in next_states:
                    transitions.append((self.to_str(list_s), self.to_str(n)))

        transitions = list(set(transitions))

        # Time generation
        time_stop = time.time()
        timed = time_stop - time_start
        print("Timed:            %.2f s" % timed)

        # Add state and transition strings to plot
        print("Plotting state-graph...")
        print("States:          ", num_states)
        print("Transitions:     ", len(transitions))

        # Create graph
        g = gv.Digraph(format='dot')
        for (a, b) in transitions:
            g.edge(a, b)

        # Plot using style
        styles = {
            'graph': {
                'label': 'State graph',
                'splines':'curved',
                'fontsize': '15',
                'fontcolor': '#999999',
                'bgcolor': '#ffffff',
                'size': '420,594',
            },
            'nodes': {
                'fontname': 'Monospace',
                'shape': 'circle',
                'fontcolor': 'white',
                'fontsize': '8',
                'color': 'white',
                'style': 'filled',
                'fillcolor': '#006699',
            },
            'edges': {
                'color': '#999999',
                'arrowhead': 'open',
                'arrowsize': '.5',
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
        print("Graph output:    ", filename)

    def to_str(self, s):
        out = ""
        for (q, m, d) in s:
            out += "{}|{} {:2}\n".format(q, m, d)
        return out


def main():
    # Define causal model
    simple = CausalModel()
    simple.add_quantity("I", ["0", "+"], [-1, 0, 1])
    simple.add_quantity("V", ["0", "+", "m"], [-1, 0, 1])
    simple.add_quantity("O", ["0", "+", "m"], [-1, 0, 1])
    simple.add_infl_rel("I", "V", 1)
    simple.add_infl_rel("O", "V", -1)
    simple.add_prop_rel("V", "O", 1)
    simple.add_value_cor("V", "m", "O", "m")
    simple.add_value_cor("V", "0", "O", "0")

    # Define causal model
    advanced = CausalModel()
    advanced.add_quantity("I", ["0", "+"], [-1, 0, 1])
    advanced.add_quantity("V", ["0", "+", "m"], [-1, 0, 1])
    advanced.add_quantity("O", ["0", "+", "m"], [-1, 0, 1])
    advanced.add_quantity("P", ["0", "+", "m"], [-1, 0, 1])
    advanced.add_quantity("H", ["0", "+", "m"], [-1, 0, 1])
    advanced.add_infl_rel("I", "V", 1)
    advanced.add_infl_rel("O", "V", -1)
    advanced.add_prop_rel("V", "H", 1)
    advanced.add_prop_rel("H", "P", 1)
    advanced.add_prop_rel("P", "O", 1)
    advanced.add_value_cor("V", "m", "O", "m")
    advanced.add_value_cor("V", "m", "P", "m")
    advanced.add_value_cor("V", "m", "H", "m")
    advanced.add_value_cor("V", "0", "O", "0")
    advanced.add_value_cor("V", "0", "P", "0")
    advanced.add_value_cor("V", "0", "H", "0")

    # Generate state graphs
    simple.reason()
    advanced.reason()

if __name__=="__main__":
    main()
