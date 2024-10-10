import random

from qlearning.main import Q_table
from examples.example_alternative import init_vars, trans_str
from parser import get_states, get_actions, parse_trans_str, qlearning_parser, parse_transition
from utils import get_all_states, update_state

trans_raw = parse_trans_str(trans_str)
vars = init_vars

states = get_states(trans_raw)
actions = get_actions(trans_raw)


q = Q_table()

states = get_all_states(transitions=states, init_vars=init_vars)

for s in states:
    for a in actions:
        q.set_column(s, a, 0)

# Mostrar la tabla Q inicial
print("Tabla Q inicial:", q.q_table)



for _ in range(100):
    print("Estado:", vars)
    options = qlearning_parser(transitions=trans_raw, curr_vars=vars)
    action = q.choose_action(vars, actions)
    trans = ""

    print("Opciones disponlibes:", options)

    for opt in options:
        transition, act = parse_transition(opt)
        if action == act or act is None:
            trans = transition
            break
    
    print("Transición disponible:", trans)

    # Selecciona el siguiente estado basado en las probabilidades de transición
    cumulative_prob = 0
    rand_val = random.random()  # Valor aleatorio para decidir el cambio de estado
    print("Rand:", rand_val)
    next_state = None
    for prob, state_change in trans:
        cumulative_prob += prob
        print(cumulative_prob)
        if rand_val <= cumulative_prob:
            next_state = state_change.split(',')  # Divide por las comas si hay múltiples variables
            break
    
    print(next_state, vars)
    next_state = update_state(next_state, vars)
    print("SNiguiente estado seleccionado:", next_state)

    reward = 1.0  # Recompensa ficticia
    
    # Actualizamos la tabla Q
    q.update_column(vars, action, next_state, reward)
    
    # Mover al siguiente estado para la próxima iteración
    vars = next_state
    
    # Incrementar el número de iteración y reducir epsilon
    q.q_iteration()