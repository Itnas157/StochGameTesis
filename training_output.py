import os

from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

OUTPUT_DIR = "output/"

class TrainingOutput:
    def __init__(self, output_file):
        # Si el outputfile no existe, crearlo
        output_file = OUTPUT_DIR + output_file + ".txt"
        if os.path.exists(output_file):
            os.remove(output_file)
        open(output_file, 'a').close()
        self.output_file = output_file
    
    def run_test(self, q_table: Q_table, smartsampling: SmartSampling, parser: Parser, ss_contant: bool):
        ROUNDS = 1000

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
                vars = parser.get_vars()
                
                if reward is not None:
                    reward = float(reward)
                    break
                
                else:
                    options = parser.get_options(vars)
                    if parser.get_var("t") == "0":
                        action = q_table.choose_action(vars, parser.get_actions(options))
                        #print("En estado ", vars, "Q-learning eligió la acción", action)
                        parser.update_vars(action, options)
                    elif parser.get_var("t") == "1":
                        if not ss_contant:
                            z = smartsampling.get_random_z()
                        hash_value = smartsampling.hash(vars, z)
                        action = smartsampling.choose_action(hash_value, parser.get_actions(options))
                        #print("En estado ", vars, "SmartSampling eligió la acción", action)
                        parser.update_vars(action, options)
                    else:
                        print("Turno invalido:", parser.get_var("t"))
                        assert True
                
                j += 1
            
            
            if reward == 1: result_q += 1
            elif reward == -1: result_ss += 1
            else: result_draw += 1
        
        output = f"Q-learning: {result_q/10}%, SmartSampling: {result_ss/10}% y {result_draw/10}% empates."

        with open(self.output_file, 'a') as f:
            f.write(output + "\n")

    def print(self, text: str):
        with open(self.output_file, 'a') as f:
            f.write(text + "\n")
