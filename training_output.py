import json
import os

from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

OUTPUT_DIR = "output/"

class TrainingOutput:
    def __init__(self, output_file):
        # Si el outputfile no existe, crearlo
        output_f = OUTPUT_DIR + output_file + ".txt"
        output_json = OUTPUT_DIR + output_file + ".json"

        open(output_f, 'a').close()
        open(output_json, 'a').close()
        
        self.output_file = output_f
        self.output_json = output_json
    
    def run_test(self, q_table: Q_table, smartsampling: SmartSampling, parser: Parser, data: dict):
        ROUNDS = 10000

        result_q = 0
        result_ss = 0
        result_draw = 0

        z = smartsampling.get_random_z()

        for _ in range(ROUNDS):
            reward = None
            parser.reset_vars()
    
            j = 0
            while reward == None and j < 1000:
                reward = parser.get_reward()
                last_index = parser.current_index
                vars = parser.get_vars()
                
                if reward is not None:
                    reward = float(reward)
                    break
                
                else:
                    actions, options = parser.get_options()

                    if parser.get_t() == 0:
                        action = q_table.ready(last_index, actions)
                        #print("Q-learning eligió la acción", action)
                        parser.update_vars(action, options)
                    elif parser.get_t() == 1:
                        if not data['smart_sampling_constant']:
                            z = smartsampling.get_random_z()
                        hash_value = smartsampling.hash(parser.get_bin(), z)
                        action = smartsampling.choose_action(hash_value, actions)
                        #print("SmartSampling eligió la acción", action)
                        parser.update_vars(action, options)
                    else:
                        print("Turno invalido:", parser.get_var("t"))
                        assert True
                
                j += 1
            
            
            if reward == 1: result_q += 1
            elif reward == -1: result_ss += 1
            else: result_draw += 1
        
        """
        output = f"Q-learning: {result_q/(ROUNDS//100)}%, SmartSampling: {result_ss/(ROUNDS//100)}% y {result_draw/(ROUNDS//100)}% empates."

        
        with open(self.output_file, 'a') as f:
            f.write(output + "\n")
        """

        data["Q-learning"] = result_q/(ROUNDS//100)
        data["SmartSampling"] = result_ss/(ROUNDS//100)
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