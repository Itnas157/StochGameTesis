import random
from parser import Parser
from qlearning.main import Q_table
from training_output import TrainingOutput
from smartsampling.main import Transformer as SmartSampling 

def run(parser: Parser, outputter: TrainingOutput, data: dict, q_learning_role: str, ss_role: str):
    # Desempaquetar configuraciones
    ss_n = data['smart_sampling_n']
    q_iters = data['q_learning_episodes']
    alpha, gamma, epsilon = data['alpha'], data['gamma'], data['epsilon']
    reset_q_table = data['q_learning_reset']
    ss_constant = data['smart_sampling_constant']
    ss_is_maxing = ss_role == "MAX"

    # Inicializar estructuras
    
    smart_sampling = SmartSampling(ss_n)
    smart_sampling.set_state_max_val(parser.get_state_max_value())

    q_table = Q_table(alpha, gamma, epsilon, q_learning_role)
    q_table.init_q_table(parser.get_table(), parser.index_init)

    def select_action(t, last_idx, actions, options, z, q_l_training=False):
        if (t == 0 and q_learning_role == "MAX") or (t == 1 and ss_role == "MAX"):
            if q_l_training:
                action = q_table.choose_action(last_idx, actions)
            else:
                action = q_table.ready(last_idx, actions)
        else:
            action = smart_sampling.choose_action(parser.get_bin(), z, actions)
        parser.update_vars(action, options)
        return action

    # Fase de entrenamiento y evaluación
    while ss_n > 1:
        if reset_q_table:
            q_table = Q_table(alpha, gamma, epsilon, q_learning_role)
            q_table.init_q_table(parser.get_table(), parser.index_init)
        
        z = smart_sampling.get_random_z()

        # Fase de entrenamiento Q-learning
        for c in range(q_iters):
            reward = None
            parser.reset_vars()
            while reward is None:
                last_idx = parser.current_index
                reward = parser.get_reward()

                if reward is not None:
                    action = '__None__'
                    parser.reset_vars()
                    break
                else:
                    actions, options = parser.get_options()
                    t = parser.get_t()
                    if not ss_constant:
                        z = smart_sampling.get_random_z()
                    action = select_action(t, last_idx, actions, options, z, q_l_training=True)
                    q_table.update_column(last_idx, action, parser.current_index, 0)
                
            q_table.update_column(last_idx, action, parser.current_index, reward)

        # Fase de evaluación Smart Sampling
        z_rewards = []
        for z in smart_sampling.zs:
            reward_prom = 0
            for _ in range(10):
                parser.reset_vars()
                reward = None

                while reward is None:
                    reward = parser.get_reward()
                    last_idx = parser.current_index

                    if reward is not None:
                        reward = float(reward)
                        break
                    actions, options = parser.get_options()
                    t = parser.get_t()
                    action = select_action(t, last_idx, actions, options, z)
                
                reward_prom += reward or 0
            z_rewards.append({'z': z, 'r': reward_prom / 10})

        # Actualización de Smart Sampling
        random.shuffle(z_rewards)  # Evita sesgos de empate
        z_rewards.sort(key=lambda x: x['r'], reverse=ss_is_maxing)
        ss_n //= 2
        smart_sampling.update_zs([entry['z'] for entry in z_rewards[:ss_n]])

    assert ss_n == 1 and len(smart_sampling.zs) == 1
    return outputter.run_test(q_table, smart_sampling, parser, data, q_learning_role, ss_role)