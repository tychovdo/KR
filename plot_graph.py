from igraph import *

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
        g = Graph(directed=True)
        
        # Adding quantities
        q_names = [x[0] for x in self.quantities]
        q_values = [x[1] for x in self.quantities]
        q_derivatives = [x[2] for x in self.quantities]

        g.add_vertices(len(self.quantities))
        g.vs["name"] = q_names
        g.vs["value"] = q_values
        g.vs["derivative"] = q_derivatives
        g.vs["label"] = g.vs["name"]

        # Add relationships
        edges = []
        labels = []

        # Add influencial relationships
        for (src, dst, amount) in self.influences:
            src_id = q_names.index(src)
            dst_id = q_names.index(dst)

            edges.append((src_id, dst_id))
            labels.append("I{}".format(amount))

        # Add proportional relationships
        for (src, dst, amount) in self.proportionals:
            src_id = q_names.index(src)
            dst_id = q_names.index(dst)

            edges.append((src_id, dst_id))
            labels.append("P{}".format(amount))

        g.add_edges(edges)
        g.es["label"] = labels

        # Plot model
        visual_style = {}
        visual_style["vertex_color"] = "#a6bddb"
        visual_style["vertex_frame_width"] = 0
        visual_style["vertex_label_color"] = "#fff"
        visual_style["vertex_size"] = 80
        visual_style["vertex_label_size"] = 15
        visual_style["vertex_label_family"] = "Arial"

        visual_style["edge_color"] = "#999"
        visual_style["edge_width"] = 5
        visual_style["edge_curved"] = True
        visual_style["edge_label_distance"] = 1000
        visual_style["edge_arrow_size"] = 2
        visual_style["edge_label_size"] = 20
        visual_style["edge_label_color"] = "#999"
        visual_style["edge_label_family"] = "Arial"
        visual_style["margin"] = 80


        plot(g, **visual_style)


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
