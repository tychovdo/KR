import graphviz as gv
import itertools

class CausalModel():
    def __init__(self):
        self.quantities = []
        self.influences = []
        self.proportionals = []
        self.value_cors = []

    def add_quantity(self, name, m_space, d_space):
        """ Add quantity including magnitude (m) and derivative (d) """
        self.quantities.append((name, m_space, d_space))

    def add_infl_rel(self, src, dst, amount):
        """ Add influencial relationship to causal model """
        self.influences.append((src, dst, amount))

    def add_prop_rel(self, src, dst, amount):
        """ Add proportional relationship to causal model """
        self.proportionals.append((src, dst, amount))

    def add_value_cor(self, q1, m1, q2, m2):
        """ Add constraint relationship to causal model """
        self.value_cors.append((q1, m1, q2, m2))

    def reason(self):
        """ Generate state-graph from causal model """

        # Generate fully-connected graph of possible states and transistions
        possibles = []
        for (name, m_space, d_space) in self.quantities:
            s = [name, m_space, d_space]
            possibles.append(list(itertools.product(*s)))
        
        self.states = list(itertools.product(*possibles))

        num_states = len(self.states)
        self.transitions = list(itertools.product(range(num_states), range(num_states)))

        # Reason value correspondences
        for (q1, m1, q2, m2) in self.value_cors:
            def filt_c_s(state):
                p = q = False
                for x in state:
                    if (x[0] == q1 and x[1] == m1):
                        p = True
                    if (x[0] == q2 and x[1] == m2):
                        q = True
                return not(p) or q # Return p implies q

            def filt_c_t(transition):
                s0 = self.states[transition[0]]
                s1 = self.states[transition[0]]
                return filt_c_s(s0) and filt_c_s(s1)

            for t in self.transitions:
                if not filt_c_t(t):
                    t = None
            for s in self.states:
                if not filt_c_s(s):
                    s = None

        # Reason derivative transistions
        for t in self.transistions:
            s0 = t[0]
            s1 = t[1]
            print(s0)


    def plot_state_graph(self):
        print("Plotting state graph")
        print("Nodes: ", len(self.states))
        print("Edges: ", len(self.transitions))

        # Plot state graph
        g = gv.Digraph(format='svg')
        
        # Adding quantities
        for s in self.states:
            g.node(str(s))

        # Add influencial relationships
        for r in self.transitions:
            src = str(self.states[r[0]])
            dst = str(self.states[r[1]])
            g.edge(src, dst, "a")

        styles = {
            'graph': {
                'label': 'Causal model',
                'fontsize': '15',
                'fontcolor': '#999999',
                'bgcolor': '#ffffff',
                'rankdir': 'LR',
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'circle',
                'fontcolor': 'white',
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
        print("\nRender causal model: ", filename)

            

    def print_model(self):
        """ Print quantities and relationships in causal model """
        print("=============== CAUSAL MODEL ===============")
        print("QUANTITIES")
        print("name            values               derivatives")
        for (name, m_space, d_space) in self.quantities:
            print("{:15} {:20} {:20}".format(name, str(m_space), str(d_space)))

        print("\nINFLUENCIAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.influences:
            print("{:15} {:10} {:10}".format(src, dst, amount))

        print("\nPROPORTIONAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.proportionals:
            print("{:15} {:10} {:10}".format(src, dst, amount))

        print("\nVALUE CORRESPONDENCES")
        for (src, src_amount, dst, dst_amount) in self.value_cors:
            print("{}({:5})   = {}({:5})".format(src, src_amount, dst, dst_amount))
        print("============================================")

    def plot_model(self):
        g = gv.Digraph(format='svg')
        
        # Adding quantities
        q_names = [x[0] for x in self.quantities]
        for q in q_names:
            g.node(q)

        # Add influencial relationships
        for (src, dst, amount) in self.influences:
            g.edge(src, dst, "I{}".format(amount))

        # Add proportional relationships
        for (src, dst, amount) in self.proportionals:
            g.edge(src, dst, "P{}".format(amount))

        styles = {
            'graph': {
                'label': 'Causal model',
                'fontsize': '15',
                'fontcolor': '#999999',
                'bgcolor': '#ffffff',
                'rankdir': 'LR',
            },
            'nodes': {
                'fontname': 'Helvetica',
                'shape': 'circle',
                'fontcolor': 'white',
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

        filename = g.render(filename='test')
        print("\nRender causal model: ", filename)

def main():
    # Define causal model
    cm = CausalModel()
    cm.add_quantity("I", ["0", "+"], ["0", "-", "+"])
    cm.add_quantity("O", ["0", "+", "max"], ["0", "-", "+"])
    cm.add_quantity("V", ["0", "+", "max"], ["0", "-", "+"])
    cm.add_infl_rel("I", "V", "+")
    cm.add_infl_rel("O", "V", "-")
    cm.add_prop_rel("V", "O", "+")
    cm.add_value_cor("V", "max", "O", "max")
    cm.add_value_cor("V", "0", "O", "0")

    # Print and plot causal model
    # cm.print_model()
    # cm.plot_model()

    # Generate state graph
    cm.reason()
    cm.plot_state_graph()

if __name__=="__main__":
    main()
