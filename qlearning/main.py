import numpy as np
import random



# Inicializar la tabla Q

class Q_table:
    def __init__(self, alpha, alpha_decay, gamma, epsilon, min_epsilon, epsilon_decay) -> None:
        self.q_table = []
        self.i = 0
        self.epsilon = epsilon  # Probabilidad de exploración
        self.alpha = alpha
        self.apha_decay = alpha_decay
        self.gamma = gamma
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.init_index = -1


    def init_q_table(self, posibilities, init_index):
        """
        Inicializa la tabla Q con valores aleatorios para cada par estado-acción.
        """
        self.q_table = []
        for i in range(len(posibilities)):
            for state in posibilities[i]:
                if len(state) == 2 and state[0] == -1:
                    self.q_table.append([i, "__None__", state[1]])
                else:
                    assert len(state) == 5
                    has_already_i_action = False
                    for q in self.q_table:
                        has_already_i_action = has_already_i_action or (q[0] == i and q[1] == state[1])
                    if not has_already_i_action: self.q_table.append([i, state[1], 0])

        self.init_index = init_index


    def find_column(self, index, action) -> int:
        for i, entry in enumerate(self.q_table):
            if entry[0] == index and entry[1] == action:
                return i
        return -1

    def q_iteration(self):
        self.i += 1
        # Decrecer epsilon después de cada iteración para reducir la exploración a medida que el agente aprende
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)
        self.alpha -= self.apha_decay

    def get_iteration(self) -> int:
        return self.i

    def update_column(self, index, action, next_state, reward):
        i = self.find_column(index, action)
        assert i != -1

        # Obtener el valor máximo de Q para el siguiente estado
        next_action_values = [entry[2] for entry in self.q_table if entry[0] == next_state]
        max_next_value = max(next_action_values)

        # Actualización de la tabla Q
        self.q_table[i][2] = ((1 - self.alpha) * self.q_table[i][2]) + (self.alpha * (reward + self.gamma * max_next_value))
        self.q_iteration()

    def choose_action(self, index, actions):
        """
        Elige una acción usando el enfoque ε-greedy.
        Si random() < epsilon, elige una acción aleatoria (exploración).
        De lo contrario, elige la mejor acción basada en los valores Q actuales (explotación).
        """
        if random.random() < self.epsilon:
            # Exploración: elegir una acción aleatoria
            return random.choice(actions)
        else:
            # Explotación: elegir la mejor acción según la tabla Q
            state_values = [(entry[1], entry[2]) for entry in self.q_table if entry[0]== index]
            if state_values:
                # Devolver la acción con el valor Q más alto
                return max(state_values, key=lambda x: x[1])[0]
            else:
                # Si no hay valores para el estado, elegir aleatoriamente
                return random.choice(actions)

    def display_q_table(self):
        """
        Muestra el contenido actual de la tabla Q.
        """
        print("Tabla Q:")
        for entry in self.q_table:
            print(f"Corresponde a estado: {entry[0]}, Acción: {entry[1]}, Valor: {entry[2]}")

    def convergence(self, index):
        l = [q[2] for q in self.q_table if q[0] == index]
        print("INIT: ", max(l))
    
    def ready(self, index, actions):
        # Explotación: elegir la mejor acción según la tabla Q
        state_values = [(entry[1], entry[2]) for entry in self.q_table if entry[0]== index]
        if state_values:
            # Devolver la acción con el valor Q más alto
            return max(state_values, key=lambda x: x[1])[0]
        else:
            # Si no hay valores para el estado, elegir aleatoriamente
            return random.choice(actions)