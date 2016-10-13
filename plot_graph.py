import graphviz as gv

class CausalModel():
    def __init__(self):
        self.quantities = []
        self.influences = []
        self.proportionals = []

    def add_quantity(self, name, values, derivatives):
        """ Add quantity to causal model """
        self.quantities.append((name, values, derivatives))

    def add_influence(self, src, dst, amount):
        """ Add influencial relationship to causal model """
        self.influences.append((src, dst, amount))

    def add_proportional(self, src, dst, amount):
        """ Add proportional relationship to causal model """
        self.proportionals.append((src, dst, amount))

    def reason(self):
        pass

    def print_model(self):
        """ Print quantities and relationships in causal model """

        print("QUANTITIES")
        print("name            values               derivatives")
        for (name, values, derivatives) in self.quantities:
            print("{:15} {:20} {:20}".format(name, str(values), str(derivatives)))

        print("\nINFLUENCIAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.influences:
            print("{:15} {:10} {:10}".format(src, dst, amount))

        print("\nPROPORTIONAL RELATIONSHIPS")
        print("from            to         amount")
        for (src, dst, amount) in self.proportionals:
            print("{:15} {:10} {:10}".format(src, dst, amount))

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
        print(filename)

# Define causal model
cm = CausalModel()
cm.add_quantity("Inflow", ["0", "+"], ["0", "-", "+"])
cm.add_quantity("Outflow", ["0", "+", "max"], ["0", "-", "+"])
cm.add_quantity("Volume", ["0", "+", "max"], ["0", "-", "+"])
cm.add_influence("Inflow", "Volume", "+")
cm.add_influence("Outflow", "Volume", "-")
cm.add_proportional("Volume", "Outflow", "+")

# Print and plot model
# cm.print_model()
cm.plot_model()

# Generate state graph
