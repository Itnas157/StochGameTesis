import numpy as np

# Parámetros Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Probabilidad de exploración

# Inicializar la tabla Q
Q_table = np.zeros((len(states), len(actions)))

# Función de recompensa
def reward(state):
    if state == "x=1 ^ y=1":
        return 2
    elif state == "x=1 ^ y=2":
        return 3
    elif state == "x=2 ^ y=1":
        return 1
    elif state == "x=2 ^ y=2":
        return 4
    return 0

# Implementar el bucle de Q-learning
def q_learning_parser(transitions, curr_vars):
    options = []

    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        pred_valid = True
        for pred in sets[0].split(" ^ "):
            pred_valid = pred_valid and pred in curr_vars
        if pred_valid: options.append(sets[1])

    return options

# Entrenar el agente
num_episodes = 1000
for episode in range(num_episodes):
    state = np.random.choice(states)  # Estado inicial aleatorio

    while True:
        # Selección de acción (ε-greedy)
        if np.random.uniform(0, 1) < epsilon:
            action = np.random.choice(actions)  # Exploración
        else:
            action = actions[np.argmax(Q_table[states.index(state)])]  # Explotación

        # Obtener las opciones basadas en el estado actual
        parser_res = q_learning_parser(trans_str.split(';'), curr_vars=vars)
        
        if len(parser_res) == 0:  # Terminar si no hay más opciones
            break

        # Elegir la siguiente acción y estado
        next_state_option = parser_res[np.random.choice(len(parser_res))]
        next_state = state  # Esto debería cambiar basado en tu implementación de transición

        # Calcular la recompensa
        r = reward(next_state)

        # Actualizar la tabla Q
        state_idx = states.index(state)
        action_idx = actions.index(action)
        next_state_idx = states.index(next_state)

        Q_table[state_idx, action_idx] = Q_table[state_idx, action_idx] + alpha * (r + gamma * np.max(Q_table[next_state_idx]) - Q_table[state_idx, action_idx])

        # Mover al siguiente estado
        state = next_state

# Mostrar la tabla Q final
print(Q_table)