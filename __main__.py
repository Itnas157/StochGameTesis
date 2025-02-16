import examples.example_race as ex_race
from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

SMART_SAMPLING_N = 1024
Q_TABLE_ITERATIONS = 100000
Q_TABLE = Q_table()
SMART_SAMPLING = SmartSampling()

parser = Parser(ex_race.trans_str, ex_race.init_vars)

SMART_SAMPLING.set_max_z(SMART_SAMPLING_N)
SMART_SAMPLING.calculate_state_max_val(parser.get_combinations())

while SMART_SAMPLING_N > 1:
    # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
    ## Inicializar Q-table
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
                z = SMART_SAMPLING.get_random_z()
                hash_value = SMART_SAMPLING.hash(vars, z)
                action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions())
                parser.update_vars(action, options)
            
            else:
                assert True
                
        Q_TABLE.update_column(vars, action, parser.get_vars(), reward)

    # Correr las N estrategias de SmartSampling con Q-learning entrenado
    z_reward = []

    for z in SMART_SAMPLING.zs:
        reward = None
        i = 0

        while reward == None and i < 1000:
            reward = parser.get_reward()
            if reward is not None:
                reward = float(reward)
                break
            else:
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
            
            i += 1
        
        if reward == None:
            reward = 1
        
        #print("Z:", z, ": Recompensa obtenida:", reward)
        z_reward.append({'z': z, 'r': reward})
        print(z_reward[-1])

        
    SMART_SAMPLING_N = SMART_SAMPLING_N // 2
    # Descartar N/2 estrategias peores

    #Q_TABLE.display_q_table()
