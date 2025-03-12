from itertools import product
import random

import examples.example_coin_flipper as ex_coin_flipper
import examples.example_dice as ex_dice
import examples.example_race as ex_race
import examples.example_three_line as ex_three_line
import examples.example_basic as ex_basic

from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling
from training_output import TrainingOutput


# Parámetros Q-learning
alphas = [0.01, 0.05, 0.1, 0.2]  # Tasa de aprendizaje
final_alphas_porc = [0.5, 0.1, 0.05, 0.01]
gammas = [0.8, 0.9, 0.95]  # Factor de descuento
epsilons = [0.5, 0.7, 0.9]  # Probabilidad de exploración inicial
min_epsilons = [0.001, 0.05]  # Valor mínimo de epsilon
epsilon_decays = [0.0001, 0.0005, 0.001, 0.005]  # Tasa de decrecimiento de epsilon

smart_sampling_ns = [2**8, 2**10, 2**12]
q_learning_episodes = [1000, 5000, 10**4, 2*10**4]

def run(parser: Parser, outputter: TrainingOutput, data: dict):
    #print("Empezando entrenamiento"

    SMART_SAMPLING_N = data['smart_sampling_n']
    Q_TABLE_ITERATIONS = data['q_learning_episodes']


    alpha_decay = (data['alpha'] - data['alpha'] * data['final_alpha_porc']) / Q_TABLE_ITERATIONS

    Q_TABLE = Q_table(data['alpha'], alpha_decay, data['gamma'], data['epsilon'], data['min_epsilon'], data['epsilon_decay'])
    SMART_SAMPLING = SmartSampling()

    SMART_SAMPLING.set_max_z(SMART_SAMPLING_N)
    SMART_SAMPLING.calculate_state_max_val(parser.get_combinations())

    #OUTPUTTER.print(f"Corriendo con alpha: {alpha}, gamma: {gamma}, epsilon: {epsilon}, min_epsilon: {min_epsilon}, epsilon_decay: {epsilon_decay}, smart_sampling_n: {smart_sampling_n}, q_learning_episodes: {q_learning_episodes}")

    Q_TABLE.init_q_table(parser.get_all_posibilities(), parser.get_init_states())

    while SMART_SAMPLING_N > 1:
        # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
        ## Inicializar Q-table
        if data['q_learning_reset']:
            Q_TABLE.init_q_table(parser.get_all_posibilities())
        Q_TABLE.alpha = data['alpha']

        z = SMART_SAMPLING.get_random_z()

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
                    action = Q_TABLE.choose_action(vars, parser.get_actions(options))
                    parser.update_vars(action, options)

                elif parser.get_var("t") == "1":
                    if not data['smart_sampling_constant']:
                        z = SMART_SAMPLING.get_random_z()
                    hash_value = SMART_SAMPLING.hash(vars, z)
                    action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions(options))
                    parser.update_vars(action, options)
                
                else:
                    assert True
                    
            Q_TABLE.update_column(vars, action, parser.get_vars(), reward)

        # Guardar resultados

        print(Q_TABLE.get_status())

        #OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)

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
                        action = Q_TABLE.choose_action(vars, parser.get_actions(options))
                        #print("En estado ", vars, "Q-learning eligió la acción", action)
                        parser.update_vars(action, options)
                    elif parser.get_var("t") == "1":
                        hash_value = SMART_SAMPLING.hash(vars, z)
                        action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions(options))
                        #print("En estado ", vars, "SmartSampling eligió la acción", action)
                        parser.update_vars(action, options)
                    else:
                        assert True
                
                i += 1

            if reward == None:
                reward = 0
            
            #print("Z:", z, ": Recompensa obtenida:", reward)
            z_reward.append({'z': z, 'r': reward})

        # Actualizar Smart Sampling
        ## Ordenamos z_reward por recompensa
        random.shuffle(z_reward)
        z_reward = sorted(z_reward, key=lambda x: x['r'], reverse=False)
        SMART_SAMPLING_N = SMART_SAMPLING_N // 2
        z_reward = z_reward[:SMART_SAMPLING_N]

        z_keys = [z['z'] for z in z_reward]
        SMART_SAMPLING.update_zs(z_keys)

        #OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)

        #Q_TABLE.display_q_table()

    assert SMART_SAMPLING_N == 1 and len(SMART_SAMPLING.zs) == 1

    #OUTPUTTER.print("Entrenamiento terminado. Corriendo 3 juegos de prueba.")
    #for _ in range(3):
    #   OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)
    #OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)

    

    #print("Entrenamiento terminado")
    return outputter.run_test(Q_TABLE, SMART_SAMPLING, parser, data)

complete = 2 * 2 * len(alphas) * len(gammas) * len(epsilons) * len(min_epsilons) * len(epsilon_decays) * len(smart_sampling_ns) * len(q_learning_episodes)
print("Completitud esperada:", complete)

for ex in [ex_basic]:
    print("Corriendo ejemplo", ex.name)
    parser = Parser(ex.trans_str, ex.init_vars)
    OUTPUT_FILE = ex.name
    OUTPUTTER = TrainingOutput(OUTPUT_FILE, 1)

    results = OUTPUTTER.load_json()
    will_test = []

    for q_learning_reset in [True, False]:
        for smart_sampling_constant in [True, False]:
            for alpha, final_alpha_porc, gamma, epsilon, min_epsilon, epsilon_decay, smart_sampling_n, q_learning_episode in product(alphas, final_alphas_porc,gammas, epsilons, min_epsilons, epsilon_decays, smart_sampling_ns, q_learning_episodes):
                
                is_already_tested = False

                for r in results:
                    if r['alpha'] == alpha and r['final_alpha_porc'] == final_alpha_porc and r['gamma'] == gamma and r['epsilon'] == epsilon and r['min_epsilon'] == min_epsilon and r['epsilon_decay'] == epsilon_decay and r['smart_sampling_n'] == smart_sampling_n and r['q_learning_episodes'] == q_learning_episode and r['q_learning_reset'] == q_learning_reset and r['smart_sampling_constant'] == smart_sampling_constant:
                        is_already_tested = True
                        break

                if not is_already_tested:

                    data = {
                        'q_learning_reset': q_learning_reset,
                        'smart_sampling_constant': smart_sampling_constant,
                        "alpha": alpha,
                        "final_alpha_porc": final_alpha_porc,
                        "gamma": gamma,
                        "epsilon": epsilon,
                        "min_epsilon": min_epsilon,
                        "epsilon_decay": epsilon_decay,
                        "smart_sampling_n": smart_sampling_n,
                        "q_learning_episodes": q_learning_episode
                    }
                    will_test.append(data)

    print("Necesitamos correr", len(will_test), "tests")
    i = complete - len(will_test)
    for data in will_test:
        data_dump = data.copy()
        results.append(run(parser, OUTPUTTER, data_dump))
        OUTPUTTER.save_json(results)

        i += 1
        print(f"Progreso: {i*100/complete}")

    