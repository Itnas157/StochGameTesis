import json
import os

from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

class TrainingOutput:
    def __init__(self, folder):
        # Crear directorio si no existe
        output_dir = folder
        os.makedirs(output_dir, exist_ok=True)
        
        self.output_json = folder + "/results.json"
        open(self.output_json, 'a').close()
        
    
    def run_test(self, q_table: Q_table, smartsampling: SmartSampling, parser: Parser, data: dict, q_learning_role: str, ss_role: str):
        ROUNDS = 10000

        result_q = 0
        result_ss = 0
        result_draw = 0

        z = smartsampling.get_random_z()
        for _ in range(ROUNDS):
            reward = None
            parser.reset_vars()
    
            historial=[]
            
            i = 0
            while reward is None and i < 100000:
                reward = parser.get_reward()
                last_index = parser.current_index

                if reward is not None:
                    reward = float(reward)
                    historial.append(reward)
                    break 
                else:
                    historial.append(parser.bin_to_state[parser.get_bin()])
                    actions, options = parser.get_options()
                    t = parser.get_t()
                    if (t==0 and q_learning_role=="MAX") or (t==1 and ss_role=="MAX"):
                        action = q_table.ready(last_index, actions)
                        parser.update_vars(action, options)
                    elif (t==1 and q_learning_role=="MAX") or (t==0 and ss_role=="MAX"):
                        action = smartsampling.choose_action(parser.get_bin(), z, actions)
                        parser.update_vars(action, options)
                    else:
                        print("Turno invalido:", parser.get_var("t"))
                        assert False
                    historial.append(action)
                i += 1

            if (reward == 1 and q_learning_role == "MAX") or (reward == -1 and ss_role =="MAX"):
                result_q += 1
            elif (reward == -1 and q_learning_role == "MAX") or (reward == 1 and ss_role=="MAX"):
                result_ss += 1
            else:
                result_draw += 1
                print("FALLO: ", reward, "historial:", historial)
                assert False

        data["Q-learning"] = result_q/(ROUNDS//100)
        data["SmartSampling"] = result_ss/(ROUNDS//100)
        data["Draw"] = result_draw/(ROUNDS//100)

        return data
    
    def run_test_ss(self, ss1: SmartSampling, ss2: SmartSampling, parser: Parser, data: dict):
        ROUNDS = 5000

        result_max = 0
        result_min = 0
        result_draw = 0

        z1 = ss1.get_random_z()
        z2 = ss2.get_random_z()

        for _ in range(ROUNDS):
            reward = None
            parser.reset_vars()
    
            i = 0
            while reward is None and i < 10000:
                reward = parser.get_reward()
                
                if reward is not None: reward = float(reward); break
                else:
                    actions, options = parser.get_options()

                    if parser.get_t() == 0:
                        action = ss1.choose_action(parser.get_bin(), z1, actions)
                        parser.update_vars(action, options)
                    elif parser.get_t() == 1:
                        action = ss2.choose_action(parser.get_bin(), z2, actions)
                        parser.update_vars(action, options)
                    else:
                        print("Turno invalido:", parser.get_var("t"))
                        assert True
                
                i += 1
            
            
            if reward == 1: result_max += 1
            elif reward == -1: result_min += 1
            else: result_draw += 1

        data["SS_Max"] = result_max/(ROUNDS//100)
        data["SS_Min"] = result_min/(ROUNDS//100)
        data["Draw"] = result_draw/(ROUNDS//100)

        return data

    def print(self, text: str):
        with open(self.output_file, 'a') as f:
            f.write(text + "\n")

    
    def load_json(self):
        with open(self.output_json, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
        
    
    def save_json(self, data: dict):
        with open(self.output_json, 'w') as f:
            json.dump(data, f)