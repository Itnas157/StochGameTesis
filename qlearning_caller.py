import random

from qlearning.main import Q_table
from examples.example_race import init_vars, trans_str
from parser import get_states, get_actions, parse_trans_str, qlearning_parser, parse_transition, parse_assign
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

print("Q-table creada")

for _ in range(100000):
    #print("Estado:", vars)
    
    # Obtener las opciones de transición basadas en el estado actual
    options = qlearning_parser(transitions=trans_raw, curr_vars=vars)
    
    # Si no hay opciones disponibles, estamos en un estado terminal
    if not options:
        print("Estado terminal alcanzado. No hay más opciones.")
        break
    
    action = q.choose_action(vars, actions)
    trans = []

    #print("Opciones disponibles:", options)

    #print("Accion elegida: ", action)

    for opt in options:
        transition, act = parse_transition(opt)
        if action == act or act is None:
            trans = trans + transition
            break
    
    #print("Transición disponible:", trans)

    # Inicializamos las variables de siguiente estado y recompensa
    next_state = None
    reward = 0
    cumulative_prob = 0
    rand_val = random.random()  # Valor aleatorio para decidir el cambio de estado
    #print("Rand:", rand_val)

    # Procesamos las transiciones
    for prob, state_change in trans:
        cumulative_prob += prob

        if rand_val <= cumulative_prob:
            # Dividimos el estado por comas, ya que puede haber múltiples variables, y chequeamos por recompensa
            state_parts = state_change.split(',')

            # Verificamos si hay una recompensa en la transición
            for part in state_parts:
                if "_R_=" in part:
                    reward = float(part.split('=')[1])  # Extraemos la recompensa
                    next_state = None
                else:
                    if next_state is None:
                        next_state = [parse_assign(part, vars)]  # Inicializamos el siguiente estado con la primera variable
                    else:
                        next_state.append(parse_assign(part, vars))  # Añadimos las variables al siguiente estado
            
            break  # Salimos del loop cuando encontramos la transición adecuada

    #print(next_state, vars)
    
    if next_state:
        next_state = update_state(next_state, vars)
        #print("Siguiente estado seleccionado:", next_state)
    #else:
        #print(f"Recompensa obtenida: {reward}")
    
    # Actualizamos la tabla Q
    q.update_column(vars, action, next_state or vars, reward)
    
    # Mover al siguiente estado solo si no es una recompensa final
    if next_state:
        vars = next_state
    else:
        vars = init_vars

    # Incrementar el número de iteración y reducir epsilon
    q.q_iteration()

q.display_q_table()




