from igraph import *
from pylog import *

class CausalModel():
    def __init__(self):
        self.quantities = {}
        self.influences = []
        self.proportionals = []

    def add_quantity(self, name, values, derivatives):
        self.quantities[name] = (values, derivatives)

    def add_influence(self, src, dst, amount):
        self.quantities.append((values, derivatives))

    def add_proportional(self, src, dst, amount):
        self.proportionals.append((src, dst, amount))

    def __str__(self):
        print("Quantities: ")
        for q in self.quantities:
            print(q)

# Define causal model
cm = CausalModel()
cm.add_quantity("Inflow", ["0", "+"], ["0", "-", "+"])
cm.add_quantity("Outflow", ["0", "+", "max"], ["0", "-", "+"])
cm.add_quantity("Volume", ["0", "+", "max"], ["0", "-", "+"])
cm.add_influence("Inflow", "Volume", "+")
cm.add_influence("Outflow", "Volume", "-")
cm.add_proportional("Volume", "Outflow", "+")
print(cm)

# Generate state graph
