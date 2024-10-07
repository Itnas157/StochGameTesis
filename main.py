import random

from qlearning.main import Q_table
from examples.example_alternative import init_vars, trans_str
from parser import get_states, get_actions, parse_trans_str, qlearning_parser
from utils import get_all_states

trans = parse_trans_str(trans_str)
vars = init_vars

states = get_states(trans)
actions = get_actions(trans)


q = Q_table()

states = get_all_states(transitions=states, init_vars=init_vars)

for s in states:
    for a in actions:
        q.set_column(s, a, 0)

# Mostrar la tabla Q inicial
print("Tabla Q inicial:", q.q_table)

options = qlearning_parser(transitions=trans, curr_vars=vars)
print(options)


q.set_column(init_vars, 'yes', 1)

print(q.q_table)