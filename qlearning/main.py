import numpy as np
import random

# Parámetros Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Probabilidad de exploración inicial
min_epsilon = 0.01  # Valor mínimo de epsilon
epsilon_decay = 0.995  # Tasa de decrecimiento de epsilon

# Inicializar la tabla Q

class Q_table:
    def __init__(self) -> None:
        self.q_table = []
        self.i = 0
        self.epsilon = epsilon  # Probabilidad de exploración

    def set_column(self, state, action, value):
        i = self.find_column(state, action)
        if i == -1:
            self.q_table.append({
                'vars': state,
                'act': action,
                'value': value
            })
        else:
            self.q_table[i]['value'] = value

    def find_column(self, state, action) -> int:
        for i, entry in enumerate(self.q_table):
            if entry['vars'] == state and entry['act'] == action:
                return i
        return -1

    def q_iteration(self):
        self.i += 1
        # Decrecer epsilon después de cada iteración para reducir la exploración a medida que el agente aprende
        self.epsilon = max(min_epsilon, self.epsilon * epsilon_decay)

    def get_iteration(self) -> int:
        return self.i

    def update_column(self, state, action, next_state, reward):
        i = self.find_column(state, action)
        assert i != -1

        # Obtener el valor máximo de Q para el siguiente estado
        next_action_values = [entry['value'] for entry in self.q_table if entry['vars'] == next_state]
        max_next_value = max(next_action_values) if next_action_values else 0

        # Actualización de la tabla Q
        self.q_table[i]["value"] = (1 - alpha) * self.q_table[i]["value"] + alpha * (reward + gamma * max_next_value)

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
