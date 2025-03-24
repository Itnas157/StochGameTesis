import random
from parser import Parser
from qlearning.main import Q_table
from training_output import TrainingOutput
from smartsampling.main import Transformer as SmartSampling 

def run(parser: Parser, outputter: TrainingOutput, data: dict, q_learning_role: str, ss_role: str):
    SMART_SAMPLING_N = data['smart_sampling_n']
    Q_TABLE_ITERATIONS = data['q_learning_episodes']

    alpha_decay = (data['alpha'] - data['alpha'] * data['final_alpha_porc']) / Q_TABLE_ITERATIONS
    ss_is_maxing = ss_role == "MAX"

    Q_TABLE = Q_table(data['alpha'], alpha_decay, data['gamma'], data['epsilon'], data['epsilon_decay'], q_learning_role)
    SMART_SAMPLING = SmartSampling(SMART_SAMPLING_N)

    SMART_SAMPLING.set_state_max_val(parser.get_state_max_value())
    Q_TABLE.init_q_table(parser.get_table(), parser.index_init)

    while SMART_SAMPLING_N > 1:
        # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
        ## Inicializar Q-table
        if data['q_learning_reset']:
            Q_TABLE.init_q_table(parser.get_table(), parser.index_init)
        Q_TABLE.alpha = data['alpha']

        z = SMART_SAMPLING.get_random_z()

        i = 0
        for _ in range(Q_TABLE_ITERATIONS):
            last_index = parser.current_index
            reward = parser.get_reward()
            actions, options = parser.get_options()

            if reward is not None:
                action = '__None__'
                reward = float(reward)
                i = -1
                parser.reset_vars()
            elif i < 1000:
                reward = 0
                actions, options = parser.get_options()
                t = parser.get_t()

                if (t == 0 and q_learning_role == "MAX") or (t == 1 and ss_role == "MAX"):
                    action = Q_TABLE.ready(last_index, actions)
                    parser.update_vars(action, options)

                elif (t == 1 and q_learning_role == "MAX") or (t==0 and ss_role == "MAX"):
                    if not data['smart_sampling_constant']:
                        z = SMART_SAMPLING.get_random_z()
                    hash_value = SMART_SAMPLING.hash(parser.get_bin(), z)
                    action = SMART_SAMPLING.choose_action(hash_value, actions)
                    parser.update_vars(action, options)
            else:
                reward = 0
                parser.reset_vars()
                i = -1

            Q_TABLE.update_column(last_index, action, parser.current_index, reward)
            i += 1

        # Correr las N estrategias de SmartSampling con Q-learning entrenado
        z_reward = []
        for z in SMART_SAMPLING.zs:
            reward = None
            i = 0
            parser.reset_vars()

            while reward == None and i < 1000:
                reward = parser.get_reward()
                last_index = parser.current_index

                if reward is not None:
                    reward = float(reward)
                    break
                else:
                    actions, options = parser.get_options()
                    t = parser.get_t()
                    if (t==0 and q_learning_role == "MAX") or (t==1 and ss_role=="MAX"):
                        action = Q_TABLE.choose_action(last_index, actions)
                        parser.update_vars(action, options)
                    elif (t==1 and q_learning_role=="MAX") or (t==0 and ss_role=="MAX"):
                        hash_value = SMART_SAMPLING.hash(parser.get_bin(), z)
                        action = SMART_SAMPLING.choose_action(hash_value, actions)
                        parser.update_vars(action, options)
                
                i += 1

            if reward == None: reward = 0
            z_reward.append({'z': z, 'r': reward})

        # Actualizar Smart Sampling
        ## Ordenamos z_reward por recompensa
        random.shuffle(z_reward)
        z_reward = sorted(z_reward, key=lambda x: x['r'], reverse=ss_is_maxing)
        SMART_SAMPLING_N = SMART_SAMPLING_N // 2
        z_reward = z_reward[:SMART_SAMPLING_N]

        z_keys = [z['z'] for z in z_reward]
        SMART_SAMPLING.update_zs(z_keys)

    assert SMART_SAMPLING_N == 1 and len(SMART_SAMPLING.zs) == 1
    return outputter.run_test(Q_TABLE, SMART_SAMPLING, parser, data, q_learning_role, ss_role)