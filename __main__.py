import random
import examples.example_coin_flipper as ex_coin_flipper
import examples.example_dice as ex_dice
import examples.example_race as ex_race
import examples.example_three_line as ex_three_line
from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling
from training_output import TrainingOutput

def run(q_learning_reset, smart_sampling_constant, ex):
    SMART_SAMPLING_N = 2**10
    Q_TABLE_ITERATIONS = 10000
    Q_TABLE = Q_table()
    SMART_SAMPLING = SmartSampling()

    parser = Parser(ex.trans_str, ex.init_vars)

    SMART_SAMPLING.set_max_z(SMART_SAMPLING_N)
    SMART_SAMPLING.calculate_state_max_val(parser.get_combinations())

    END_COMPARATION = 1000

    OUTPUT_FILE = ex.name + '_'
    if q_learning_reset:
        OUTPUT_FILE += 'qreset_'
    else:
        OUTPUT_FILE += 'noqreset_'
    if smart_sampling_constant:
        OUTPUT_FILE += 'ssconstant'
    else:
        OUTPUT_FILE += 'nossconstant'
        


    OUTPUTTER = TrainingOutput(OUTPUT_FILE)

    # Version Q-learning resetea con cada loop de Smart Sampling
    # Version Smart Sampling usa un z aleatorio en cada movimiento de Q-learning
    Q_TABLE.init_q_table(parser.get_all_posibilities())

    while SMART_SAMPLING_N > 1:
        # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
        ## Inicializar Q-table
        if q_learning_reset:
            Q_TABLE.init_q_table(parser.get_all_posibilities())

        z = SMART_SAMPLING.get_random_z()

        ## Correr Q-learning
        games = 0
        for _ in range(Q_TABLE_ITERATIONS):
            vars = parser.get_vars()
            reward = parser.get_reward()
            action = '__None__'

            if reward is not None:
                reward = float(parser.get_reward())
                games += 1

                parser.reset_vars()
            else:
                reward = 0
                options = parser.get_options(vars)

                if parser.get_var("t") == "0":
                    action = Q_TABLE.choose_action(vars, parser.get_actions(options))
                    parser.update_vars(action, options)

                elif parser.get_var("t") == "1":
                    if not smart_sampling_constant:
                        z = SMART_SAMPLING.get_random_z()
                    hash_value = SMART_SAMPLING.hash(vars, z)
                    action = SMART_SAMPLING.choose_action(hash_value, parser.get_actions(options))
                    parser.update_vars(action, options)
                
                else:
                    assert True
                    
            Q_TABLE.update_column(vars, action, parser.get_vars(), reward)
            if games > 1024:
                break

        # Guardar resultados

        OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)

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
            #print("Reward:", reward)

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

        OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)

        #Q_TABLE.display_q_table()

    OUTPUTTER.print("Entrenamiento terminado. Corriendo 3 juegos de prueba.")
    for _ in range(3):
        OUTPUTTER.run_test(Q_TABLE, SMART_SAMPLING, parser, smart_sampling_constant)



for ex in [ex_three_line, ex_dice]:
    print("Corriendo ejemplo", ex.name)
    for q_learning_reset in [True, False]:
        for smart_sampling_constant in [True, False]:
            print("Corriendo con Q-learning reseteado:", q_learning_reset, "y Smart Sampling constante:", smart_sampling_constant)
            run(q_learning_reset, smart_sampling_constant, ex)