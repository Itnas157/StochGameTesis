import examples.example_race as ex_race
from parser import Parser
from qlearning.main import Q_table

SMART_SAMPLING_N = 1024
Q_TABLE_ITERATIONS = 100000
Q_TABLE = Q_table()

parser = Parser(ex_race.trans_str, ex_race.init_vars)


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
            action = Q_TABLE.choose_action(vars, parser.get_actions())
            parser.update_vars(action, options)

        Q_TABLE.update_column(vars, action, parser.get_vars(), reward)
    # Correr las N estrategias de SmartSampling con Q-learning entrenado
    SMART_SAMPLING_N = SMART_SAMPLING_N // 2
    print(SMART_SAMPLING_N)
    # Descartar N/2 estrategias peores

    Q_TABLE.display_q_table()
