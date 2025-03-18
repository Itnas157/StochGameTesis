import random
from parser import Parser
from training_output import TrainingOutput
from smartsampling.main import Transformer as SmartSampling 

def run(parser: Parser, outputter: TrainingOutput, data: dict):
    N1 = data['smart_sampling_n']
    N2 = data['smart_sampling_n']

    SS1 = SmartSampling(N1)
    SS2 = SmartSampling(N2)

    SS1.set_state_max_val(parser.calculate_state_max_value())
    SS2.set_state_max_val(parser.calculate_state_max_value())

    while N1 > 1 and N2 > 1:
        ## SS 1

        z2 = SS2.get_random_z()
        z_reward = []

        for z1 in SS1.zs:
            reward = None
            i = 0
            parser.reset_vars()

            while reward == None and i < 1000:
                reward = parser.get_reward()

                if reward is not None:
                    reward = float(reward)
                    break
                else:
                    actions, options = parser.get_options()
                    if parser.get_t() == 0:
                        hash_value = SS1.hash(parser.get_bin(), z1)
                        action = SS2.choose_action(hash_value, actions)
                        parser.update_vars(action, options)
                    elif parser.get_t() == 1:
                        if not data['smart_sampling_constant']:
                            z2 = SS2.get_random_z()
                        hash_value = SS2.hash(parser.get_bin(), z2)
                        action = SS2.choose_action(hash_value, actions)
                        parser.update_vars(action, options)
                    else:
                        assert True
                
                i += 1

            if reward == None: reward = 0
            z_reward.append({'z': z1, 'r': reward})

        # Actualizar Smart Sampling
        ## Ordenamos z_reward por recompensa
        random.shuffle(z_reward)
        z_reward = sorted(z_reward, key=lambda x: x['r'], reverse=True)
        N1 = N1 // 2
        z_reward = z_reward[:N1]

        z_keys = [z['z'] for z in z_reward]
        SS1.update_zs(z_keys)
    

        # SS 2

        z1 = SS1.get_random_z()
        z_reward = []

        for z2 in SS2.zs:
            reward = None
            i = 0
            parser.reset_vars()

            while reward == None and i < 1000:
                reward = parser.get_reward()

                if reward is not None:
                    reward = float(reward)
                    break
                else:
                    actions, options = parser.get_options()
                    if parser.get_t() == 0:
                        if not data['smart_sampling_constant']:
                            z1 = SS1.get_random_z()
                        hash_value = SS1.hash(parser.get_bin(), z1)
                        action = SS1.choose_action(hash_value, actions)
                        parser.update_vars(action, options)
                    elif parser.get_t() == 1:
                        hash_value = SS2.hash(parser.get_bin(), z2)
                        action = SS2.choose_action(hash_value, actions)
                        parser.update_vars(action, options)
                    else:
                        assert True
                
                i += 1

            if reward == None: reward = 0
            z_reward.append({'z': z2, 'r': reward})

        # Actualizar Smart Sampling
        ## Ordenamos z_reward por recompensa
        random.shuffle(z_reward)
        z_reward = sorted(z_reward, key=lambda x: x['r'], reverse=False)
        N2 = N2 // 2
        z_reward = z_reward[:N2]

        z_keys = [z['z'] for z in z_reward]
        SS2.update_zs(z_keys)

    assert N1 == 1 and len(SS1.zs) == 1 and N2 == 1 and len(SS2.zs) == 1

    return outputter.run_test_ss(SS1, SS2, parser, data)