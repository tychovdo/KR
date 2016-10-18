import graphviz as gv
import itertools

class CausalModel():
    def __init__(self):
        self.quantities = []
        self.influences = []
        self.proportionals = []
        self.value_cors = []

        self.states = []

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
        class State():
            def __init__(self, state_tuple):
                self.state_tuple = state_tuple
                self.links = []

            def __str__(self):
                out = ""
                for (q, m, d) in self.state_tuple:
                    out += "{}|{} {}\n".format(q, m, d)
                return out

            def add_links(self, states):
                new_links = []

                # Possible derivative changes
                q = self.state_tuple[0]

                    if q[2] == '0':
                        new_state_tuple = self.state_tuple
                        new_state_tuple[i][2] == '+'
                        new_links.append(new_state_tuple)

                # Add links
                for n in new_links:
                    for s in states:
                        if n == s:
                            self.links.append(s)
                print(len(new_links))

            def __eq__(self, other):
                return self.state_tuple == self.state_tuple

        # Generate all possible states
        state_tuples = []
        for (name, m_space, d_space) in self.quantities:
            s = [name, m_space, d_space]
            state_tuples.append(list(itertools.product(*s)))
        state_tuples = list(itertools.product(*state_tuples))
        self.states = [State(x) for x in state_tuples]

        # Generate possisble transitions
        for s in self.states:
            s.add_links(self.states)

        # Remove nodes without connections
        self.states = [x for x in self.states if x.links != []]

    def plot_state_graph(self):
        print("Plotting state graph")

        # Plot state graph
        g = gv.Digraph(format='svg')
        
        # Adding quantities
        for s in self.states:
            g.node(str(s))
            for l in s.links:
                g.edge(str(s), str(l))

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
    cm.add_quantity("O", ["0", "+", "m"], ["0", "-", "+"])
    cm.add_quantity("V", ["0", "+", "m"], ["0", "-", "+"])
    cm.add_infl_rel("I", "V", "+")
    cm.add_infl_rel("O", "V", "-")
    cm.add_prop_rel("V", "O", "+")
    cm.add_value_cor("V", "m", "O", "m")
    cm.add_value_cor("V", "0", "O", "0")

    # Print and plot causal model
    # cm.print_model()
    # cm.plot_model()

    # Generate state graph
    cm.reason()
    cm.plot_state_graph()

if __name__=="__main__":
    main()
