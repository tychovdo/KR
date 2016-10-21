# Qualitative Dynamic System State-graph Plotter
A python program able to generate state-graph of dynamic system solely based on a qualitative description of the model

## Example usage

Define a dynamic system using quantity, influence constraints, proportionality constraint and value using a system description.
Example:

```
# Define causal model
cm = CausalModel()
cm.add_quantity("I", ["0", "+"], [-1, 0, 1])
cm.add_quantity("V", ["0", "+", "m"], [-1, 0, 1])
cm.add_quantity("O", ["0", "+", "m"], [-1, 0, 1])
cm.add_quantity("H", ["0", "+", "m"], [-1, 0, 1])
cm.add_quantity("P", ["0", "+", "m"], [-1, 0, 1])
cm.add_infl_rel("I", "V", 1)
cm.add_infl_rel("O", "V", -1)
cm.add_prop_rel("V", "H", 1)
cm.add_prop_rel("H", "P", 1)
cm.add_prop_rel("P", "O", 1)
cm.add_value_cor("V", "m", "O", "m")
cm.add_value_cor("V", "m", "H", "m")
cm.add_value_cor("V", "m", "P", "m")
cm.add_value_cor("V", "0", "O", "0")
cm.add_value_cor("V", "0", "H", "0")
cm.add_value_cor("V", "0", "P", "0")
```

Generate a pdf of a state-graph

```
$ make pdf
```

## Requirements

- `python==3.5.1`
- `graphviz`

