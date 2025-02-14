import examples.example_race as ex_race
from parser import Parser
from qlearning.main import Q_table
from smartsampling.main import Transformer as SmartSampling

SMART_SAMPLING_N = 1024
Q_TABLE_ITERATIONS = 100000
Q_TABLE = Q_table()
SMART_SAMPLING = SmartSampling()

parser = Parser(ex_race.trans_str, ex_race.init_vars)

SMART_SAMPLING.set_max_z(SMART_SAMPLING_N)
SMART_SAMPLING.calculate_state_max_val(parser.get_combinations())

while SMART_SAMPLING_N > 1:
    # Correr Q-learning donde Smart Sampling elige con probabilidad 1/N
    ## Inicializar Q-table
    Q_TABLE.init_q_table(parser.get_combinations(), parser.get_actions())

    ## Correr Q-learning
    for _ in range(Q_TABLE_ITERATIONS):
        vars = parser.get_vars()
        reward = parser.get_reward()

        if reward is not None:
            reward = float(parser.get_reward())
            parser.reset_vars()
        else:
            reward = 0
            options = parser.get_options(vars)
            if parser.get_var("t") == 0:
                action = Q_TABLE.choose_action(vars, parser.get_actions())
                parser.update_vars(action, options)
            elif parser.get_var("t") == 1:
                pass
                
        Q_TABLE.update_column(vars, action, parser.get_vars(), reward)

    # Correr las N estrategias de SmartSampling con Q-learning entrenado
    z_reward = []

    for z in SMART_SAMPLING.zs:
        print("z:", z)
        reward = 0
        i = 0
        
    SMART_SAMPLING_N = SMART_SAMPLING_N // 2
    print(SMART_SAMPLING_N)
    # Descartar N/2 estrategias peores

    Q_TABLE.display_q_table()
