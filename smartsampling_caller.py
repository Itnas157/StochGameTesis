import random

from smartsampling.main import Transformer
from examples.example_alternative import init_vars, trans_str
from parser import get_states, get_actions, parse_trans_str, qlearning_parser, parse_transition
from utils import get_all_states, update_state

trans_raw = parse_trans_str(trans_str)
vars = init_vars

states = get_states(trans_raw)
actions = get_actions(trans_raw)

smartsampling = Transformer()

states = get_all_states(transitions=states, init_vars=init_vars)

smartsampling.set_max_z(1000)
smartsampling.calculate_state_max_val(states)


for z in smartsampling.zs:
    reward = 0
    i = 0
    vars = init_vars

    while reward == 0 and i < 1000:
        #print("Estado:", vars)
        
        # Obtener las opciones de transición basadas en el estado actual
        options = qlearning_parser(transitions=trans_raw, curr_vars=vars)

        # Si no hay opciones disponibles, estamos en un estado terminal
        if not options:
            print("Estado terminal alcanzado. No hay más opciones.")
            break

        #print("Opciones disponibles:", options)

        trans = {}
        for opt in options:
            transition, act = parse_transition(opt) # TODO: No soporta act is None
            trans[act] = transition

        #print("Transición disponible:", trans)

        hash_value = smartsampling.hash(vars, z)
        action = smartsampling.choose_action(hash_value, actions)

        #print("Accion elegida: ", action)

        #print("Elección:", trans[action])

        

        # Inicializamos las variables de siguiente estado y recompensa
        next_state = None
        cumulative_prob = 0
        rand_val = random.random()  # Valor aleatorio para decidir el cambio de estado
        #print("Rand:", rand_val)

        # Procesamos las transiciones
        for prob, state_change in trans[action]:
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
                            next_state = [part]  # Inicializamos el siguiente estado con la primera variable
                        else:
                            next_state.append(part)  # Añadimos las variables al siguiente estado
                
                break  # Salimos del loop cuando encontramos la transición adecuada

        #print(next_state, vars)
        

        if next_state:
            vars = update_state(next_state, vars)
            #print("Siguiente estado seleccionado:", next_state)
        else:
            vars = init_vars
        
        i += 1
    
    print("Z:", z, ": Recompensa obtenida:", reward)





