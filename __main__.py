from itertools import product

import examples.example_coin_flipper as ex_coin_flipper
import examples.example_dice as ex_dice
import examples.example_race as ex_race
import examples.example_three_line as ex_three_line
import examples.example_basic as ex_basic
import examples.example_basic_loop as ex_basic_loop

from parser import Parser
from smartsampling.main import state_to_bin
from training_output import TrainingOutput

import q_ss
import ss_ss

# Parámetros Q-learning
alphas = [0.05, 0.1, 0.2]  # Tasa de aprendizaje
final_alphas_porc = [0.5, 0.1, 0.05, 0.01]
gammas = [0.8, 0.9, 0.95]  # Factor de descuento
epsilons = [0.5, 0.7, 0.9]  # Probabilidad de exploración inicial
min_epsilons = [0.001, 0.05]  # Valor mínimo de epsilon
epsilon_decays = [0.0001, 0.0005, 0.001]  # Tasa de decrecimiento de epsilon

smart_sampling_ns = [2**8, 2**10, 2**12]
q_learning_episodes = [1000, 5000, 10**4]



complete = 2 * 2 * len(alphas) * len(final_alphas_porc) * len(gammas) * len(epsilons) * len(min_epsilons) * len(epsilon_decays) * len(smart_sampling_ns) * len(q_learning_episodes)
print("Completitud esperada:", complete)


for ex in [ex_three_line]:
    print("Corriendo ejemplo", ex.name)
    parser = Parser(ex.trans_str, ex.init_vars)
    bins = [state_to_bin(comb, parser.calculate_state_max_value()) for comb in parser.all_combinations]
    parser.create_table(bins)

    for roles in [("SS", "SS"), ("SS", "Q"), ("Q", "SS")]:
        OUTPUT_FILE = f"{roles[0]}_{roles[1]}/{ex.name}"
        OUTPUTTER = TrainingOutput(OUTPUT_FILE)

        results = OUTPUTTER.load_json()
        
        will_test = []
        # Caso SS-SS ignora los parámetros de Q-learning
        if roles == ("SS", "SS"):
            existing_results = {
                (
                    r['smart_sampling_n'], r['smart_sampling_constant']
                ) 
                for r in results
            }

            for smart_sampling_n in smart_sampling_ns:
                for smart_sampling_constant in [True, False]:
                    data = {
                        'smart_sampling_constant': smart_sampling_constant,
                        "smart_sampling_n": smart_sampling_n,
                    }
                    key = (data["smart_sampling_n"], data["smart_sampling_constant"])
                    if key not in existing_results:
                        will_test.append(data)

        else:
            # Combinaciones completas de parámetros para Q-learning + SS
            existing_results = {
                (
                    r['alpha'], r['final_alpha_porc'], r['gamma'], r['epsilon'], 
                    r['min_epsilon'], r['epsilon_decay'], r['smart_sampling_n'], 
                    r['q_learning_episodes'], r['q_learning_reset'], r['smart_sampling_constant']
                ) 
                for r in results
            }

            param_combinations = product(
                alphas, final_alphas_porc, gammas, epsilons, min_epsilons, 
                epsilon_decays, smart_sampling_ns, q_learning_episodes
            )
            for alpha, final_alpha_porc, gamma, epsilon, min_epsilon, epsilon_decay, smart_sampling_n, q_learning_episode in param_combinations:
                for q_learning_reset in [True, False]:
                    for smart_sampling_constant in [True, False]:
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
                        key = (
                            alpha, final_alpha_porc, gamma, epsilon, min_epsilon,
                            epsilon_decay, smart_sampling_n, q_learning_episode,
                            q_learning_reset, smart_sampling_constant
                        )
                        if key not in existing_results:
                            will_test.append(data)

        # Ejecutar y guardar por batches
        batch_results = []
        total_tests = complete - len(will_test)
        for i, data in enumerate(will_test, 1):
            match roles:
                case ("Q", "SS"): batch_results.append(q_ss.run(parser, OUTPUTTER, data.copy(), "MAX", "MIN"))
                case ("SS", "Q"): batch_results.append(q_ss.run(parser, OUTPUTTER, data.copy(), "MIN", "MAX"))
                case ("SS", "SS"): batch_results.append(ss_ss.run(parser, OUTPUTTER, data.copy()))

            if i % 100 == 0 or i == len(will_test):
                results.extend(batch_results)
                OUTPUTTER.save_json(results)
                batch_results.clear()
                print(f"Progreso: {100 * i / len(will_test):.2f}%")


    