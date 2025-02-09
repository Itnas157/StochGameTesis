import examples.example_race as ex_race
from parser import Parser
from qlearning.main import Q_table


SMART_SAMPLING_N = 1024
Q_TABLE = Q_table()

parser = Parser(ex_race.trans_str, ex_race.init_vars)

"""
while SMART_SAMPLING_N > 1:
    # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
    ## Inicializar Q-table
    

    # Correr las N estrategias de SmartSampling con Q-learning entrenado

    # Descartar N/2 estrategias peores
"""