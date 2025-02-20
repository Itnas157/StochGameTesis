import random
import examples.example_race as ex_race
from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

output = 'StochGameTesis/test/output_race.txt'

SMART_SAMPLING_N = 1024
Q_TABLE_ITERATIONS = 10000
Q_TABLE = Q_table()
SMART_SAMPLING = SmartSampling()

parser = Parser(ex_race.trans_str, ex_race.init_vars)

SMART_SAMPLING.set_max_z(SMART_SAMPLING_N)
SMART_SAMPLING.calculate_state_max_val(parser.get_combinations())

END_COMPARATION = 1000

# Version Q-learning resetea con cada loop de Smart Sampling
# Version Smart Sampling usa un z aleatorio en cada movimiento de Q-learning
iterarion = 1
while SMART_SAMPLING_N > 1:
    result_qlearning = 0
    result_smartsampling = 0
    result_draw = 0

    # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
    ## Inicializar Q-table
    Q_TABLE.init_q_table(parser.get_all_posibilities())

    ## Correr Q-learning
    games = 0
    for _ in range(Q_TABLE_ITERATIONS):
        vars = parser.get_vars()
        reward = parser.get_reward()
        action = '__None__'

        if reward is not None:
            reward = float(parser.get_reward())
            games += 1

            if reward == -1:
                result_smartsampling += 1
            elif reward == 1:
                result_qlearning += 1
            else:
                result_draw += 0

            parser.reset_vars()
        else:
            reward = 0
            options = parser.get_options(vars)

            if parser.get_var("t") == "0":
                action = Q_TABLE.choose_action(vars, parser.get_actions())
                parser.update_vars(action, options)

            elif parser.get_var("t") == "1":
                z = SMART_SAMPLING.get_random_z()
                hash_value = SMART_SAMPLING.hash(vars, z)
                action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
                parser.update_vars(action, options)
            
            else:
                assert True
                
        Q_TABLE.update_column(vars, action, parser.get_vars(), reward)
        if games > 1024:
            break

    with open(output, 'ab') as f:
        f.write(f"Q-learning vs Smart Sampling: ronda {iterarion}\n".encode())
        f.write(f"Q-learning post-traning: \n".encode())
        f.write(f"Q-learning: {result_qlearning}, ".encode())
        f.write(f"Smart Sampling: {result_smartsampling},".encode())
        f.write(f"Empates: {result_draw}\n".encode())

    # Correr las N estrategias de SmartSampling con Q-learning entrenado
    z_reward = []

    for z in SMART_SAMPLING.zs:
        #print(z)
        reward = None
        i = 0
        parser.reset_vars()

        while reward == None and i < 1000:
            reward = parser.get_reward()
            vars = parser.get_vars()
            if reward is not None:
                reward = float(reward)
                break
            else:
                options = parser.get_options(vars)
                if parser.get_var("t") == "0":
                    action = Q_TABLE.choose_action(vars, parser.get_actions())
                    #print("En estado ", vars, "Q-learning eligió la acción", action)
                    parser.update_vars(action, options)
                elif parser.get_var("t") == "1":
                    hash_value = SMART_SAMPLING.hash(vars, z)
                    action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
                    #print("En estado ", vars, "SmartSampling eligió la acción", action)
                    parser.update_vars(action, options)
                else:
                    assert True
            
            i += 1
        #print("Reward:", reward)

        if reward == None:
            reward = 1
        
        #print("Z:", z, ": Recompensa obtenida:", reward)
        z_reward.append({'z': z, 'r': reward})
    
    # Guardar resultados
    result_qlearning = 0
    result_smartsampling = 0
    result_draw = 0
    for z in z_reward:
        if z['r'] == -1:
            result_smartsampling += 1
        elif z['r'] == 1:
            result_qlearning += 1
        else:
            result_draw += 1

    with open(output, 'ab') as f:
        f.write(f"Smart Sampling post-training:\n".encode())
        f.write(f"Q-learning: {result_qlearning}, ".encode())
        f.write(f"Smart Sampling: {result_smartsampling}, ".encode())
        f.write(f"Empates: {result_draw}\n".encode())
        f.write(b"\n")

    # Actualizar Smart Sampling
    ## Ordenamos z_reward por recompensa
    random.shuffle(z_reward)
    z_reward = sorted(z_reward, key=lambda x: x['r'], reverse=True)
    SMART_SAMPLING_N = SMART_SAMPLING_N // 2
    z_reward = z_reward[:SMART_SAMPLING_N]

    z_keys = [z['z'] for z in z_reward]
    SMART_SAMPLING.update_zs(z_keys)

    iterarion +=1
    #Q_TABLE.display_q_table()


# POST-TRAINING
# Comparativa con ambos entrenados
assert len(SMART_SAMPLING.zs) == 1

result_qlearning = 0
result_smartsampling = 0
result_draw = 0

SMART_SAMPLING_ITERATIONS = END_COMPARATION // 2
Q_LEARNING_ITERATIONS = END_COMPARATION - SMART_SAMPLING_ITERATIONS

z = SMART_SAMPLING.zs[0]
print("Z final:", z)
for i in range(SMART_SAMPLING_ITERATIONS):
    reward = None
    parser.reset_vars()
    
    j = 0
    while reward == None and j < 1000:
        reward = parser.get_reward()
        vars = parser.get_vars()
        
        if reward is not None:
            reward = float(reward)
            break
        
        else:
            options = parser.get_options(vars)
            if parser.get_var("t") == "0":
                action = Q_TABLE.choose_action(vars, parser.get_actions())
                #print("En estado ", vars, "Q-learning eligió la acción", action)
                parser.update_vars(action, options)
            elif parser.get_var("t") == "1":
                hash_value = SMART_SAMPLING.hash(vars, z)
                action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
                #print("En estado ", vars, "SmartSampling eligió la acción", action)
                parser.update_vars(action, options)
            else:
                assert True
        
        j += 1

    if reward == -1:
        result_smartsampling += 1
    elif reward == 1:
        result_qlearning += 1
    else:
        result_draw += 0

with open(output, 'ab') as f:
    f.write(f"Q-LEARNING vs SMARTSAMPLING\n".encode())
    f.write(f"Smart Sampling fue el último entrenado\n".encode())
    f.write(f"Q-learning ganó {result_qlearning} veces\n".encode())
    f.write(f"Smart Sampling ganó {result_smartsampling} veces\n".encode())
    f.write(f"Hubo {result_draw} empates\n".encode())
    f.write(f"\n".encode())


Q_TABLE.init_q_table(parser.get_all_posibilities())

## Correr Q-learning
for _ in range(Q_TABLE_ITERATIONS):
    vars = parser.get_vars()
    reward = parser.get_reward()
    action = '__None__'

    if reward is not None:
        reward = float(parser.get_reward())
        parser.reset_vars()

    else:
        reward = 0
        options = parser.get_options(vars)
        
        if parser.get_var("t") == "0":
            action = Q_TABLE.choose_action(vars, parser.get_actions())
            parser.update_vars(action, options)

        elif parser.get_var("t") == "1":
            hash_value = SMART_SAMPLING.hash(vars, z)
            action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
            parser.update_vars(action, options)

        else:
            assert True
            
    Q_TABLE.update_column(vars, action, parser.get_vars(), reward)

result_qlearning = 0
result_smartsampling = 0
result_draw = 0
for i in range(Q_LEARNING_ITERATIONS):
    reward = None
    parser.reset_vars()
    
    j = 0
    while reward == None and j < 1000:
        reward = parser.get_reward()
        vars = parser.get_vars()
        
        if reward is not None:
            reward = float(reward)
            break
        
        else:
            options = parser.get_options(vars)
            if parser.get_var("t") == "0":
                action = Q_TABLE.choose_action(vars, parser.get_actions())
                #print("En estado ", vars, "Q-learning eligió la acción", action)
                parser.update_vars(action, options)
            elif parser.get_var("t") == "1":
                hash_value = SMART_SAMPLING.hash(vars, z)
                action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
                #print("En estado ", vars, "SmartSampling eligió la acción", action)
                parser.update_vars(action, options)
            else:
                assert True
        
        j += 1

    if reward == -1:
        result_smartsampling += 1
    elif reward == 1:
        result_qlearning += 1
    else:
        result_draw += 0

with open(output, 'ab') as f:
    f.write(f"Q-learning fue el último entrenado\n".encode())
    f.write(f"Q-learning ganó {result_qlearning} veces\n".encode())
    f.write(f"Smart Sampling ganó {result_smartsampling} veces\n".encode())
    f.write(f"Hubo {result_draw} empates\n".encode())
