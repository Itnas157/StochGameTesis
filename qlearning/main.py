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
        print(f"Alpha: {alpha}, Decay: {alpha_decay}")
        self.gamma = gamma
        self.min_epsilon = min_epsilon
        self.epsilon_decay = epsilon_decay
        self.init_state_is = []


    def init_q_table(self, posibilities, init_states = []):
        """
        Inicializa la tabla Q con valores aleatorios para cada par estado-acción.
        """
        self.q_table = []
        for poss in posibilities:
            self.q_table.append({
                'vars': poss['vars'],
                'act': poss['action'],
                'value': 0
            })
        
        if init_states != []:
            self.init_state_is = []
            for init_state in init_states:
                self.init_state_is.append(self.find_column(init_state['vars'], init_state['action']))

    def find_column(self, state, action) -> int:
        for i, entry in enumerate(self.q_table):
            if entry['vars'] == state and entry['act'] == action:
                return i
        return -1

    def q_iteration(self):
        self.i += 1
        # Decrecer epsilon después de cada iteración para reducir la exploración a medida que el agente aprende
        self.epsilon = max(self.min_epsilon, self.epsilon - self.epsilon_decay)
        self.alpha -= self.apha_decay

    def get_iteration(self) -> int:
        return self.i

    def update_column(self, state, action, next_state, reward):
        i = self.find_column(state, action)
        assert i != -1

        # Obtener el valor máximo de Q para el siguiente estado
        next_action_values = [entry['value'] for entry in self.q_table if entry['vars'] == next_state]
        max_next_value = max(next_action_values)

        # Actualización de la tabla Q
        self.q_table[i]["value"] = ((1 - self.alpha) * self.q_table[i]["value"]) + (self.alpha * (reward + self.gamma * max_next_value))

    def choose_action(self, state, actions):
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
            state_values = [(entry['act'], entry['value']) for entry in self.q_table if entry['vars'] == state]
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
            print(f"Estado: {entry['vars']}, Acción: {entry['act']}, Valor: {entry['value']:.2f}")

    def get_status(self):
        c = 0.0; sum = len(self.init_state_is)
        for i in self.init_state_is:
            c += self.q_table[i]['value']
        return c / sum