from itertools import product

import examples.example_coin_flipper as ex_coin_flipper
import examples.example_race as ex_race
import examples.example_three_line as ex_three_line
import examples.example_three_line_prob as ex_three_prob
import examples.example_basic as ex_basic
import examples.example_basic_loop as ex_basic_loop

from parser import Parser
from smartsampling.main import state_to_bin
from training_output import TrainingOutput
from graphic import Graphic

import q_ss
import ss_ss


for ex in [ex_three_line, ex_race, ex_three_prob, ex_coin_flipper]:
    complete = 2 * 2 * len(ex.alphas) * len(ex.final_alphas_porc) * len(ex.gammas) * len(ex.epsilons) * len(ex.epsilon_decays) * len(ex.smart_sampling_ns) * len(ex.q_learning_episodes)
    print("Completitud esperada:", complete)
    print("Corriendo ejemplo", ex.name)
    parser = Parser(ex.trans_str, ex.init_vars)
    bins = [state_to_bin(comb, parser.get_state_max_value()) for comb in parser.all_combinations]
    parser.create_table(bins)

    for roles in [("Q", "SS"), ("SS", "Q"), ("SS", "SS")]:
        OUTPUT_FOLDER = f"output/{roles[0]}_{roles[1]}/{ex.name}"
        OUTPUTTER = TrainingOutput(OUTPUT_FOLDER)

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

            for smart_sampling_n in ex.smart_sampling_ns:
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
                    r['alpha'], r['final_alpha_porc'], r['gamma'], r['epsilon'], r['epsilon_decay'], r['smart_sampling_n'], 
                    r['q_learning_episodes'], r['q_learning_reset'], r['smart_sampling_constant']
                ) 
                for r in results
            }

            param_combinations = product(
                ex.alphas, ex.final_alphas_porc, ex.gammas, ex.epsilons, 
                ex.epsilon_decays, ex.smart_sampling_ns, ex.q_learning_episodes
            )
            for alpha, final_alpha_porc, gamma, epsilon, epsilon_decay, smart_sampling_n, q_learning_episode in param_combinations:
                for q_learning_reset in [True, False]:
                    for smart_sampling_constant in [True, False]:
                        data = {
                            'q_learning_reset': q_learning_reset,
                            'smart_sampling_constant': smart_sampling_constant,
                            "alpha": alpha,
                            "final_alpha_porc": final_alpha_porc,
                            "gamma": gamma,
                            "epsilon": epsilon,
                            "epsilon_decay": epsilon_decay,
                            "smart_sampling_n": smart_sampling_n,
                            "q_learning_episodes": q_learning_episode
                        }
                        key = (
                            alpha, final_alpha_porc, gamma, epsilon,
                            epsilon_decay, smart_sampling_n, q_learning_episode,
                            q_learning_reset, smart_sampling_constant
                        )
                        if key not in existing_results:
                            will_test.append(data)

        # Ejecutar y guardar por batches
        batch_results = []
        total_tests = complete - len(will_test)
        i = 1
        for data in will_test:
            for _ in range(25):
                match roles:
                    case ("Q", "SS"):batch_results.append(q_ss.run(parser, OUTPUTTER, data.copy(), "MAX", "MIN")); i += 1
                    case ("SS", "Q"): batch_results.append(q_ss.run(parser, OUTPUTTER, data.copy(), "MIN", "MAX")); i += 1
                    case ("SS", "SS"):batch_results.append(ss_ss.run(parser, OUTPUTTER, data.copy())); i += 1

                if i % 10 == 0:
                    results.extend(batch_results)
                    OUTPUTTER.save_json(results)
                    batch_results.clear()
                    print(f"Progreso: {100 * i / (len(will_test)*25):.2f}%")
    
        OUTPUTTER.save_json(results)

        Grap = Graphic(OUTPUT_FOLDER)
        Grap.graph(is_ss_ss=(roles == ('SS', 'SS')))


    