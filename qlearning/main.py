import random
from collections import defaultdict

class Q_table:
    def __init__(self, alpha, gamma, epsilon, role) -> None:
        self.q_table = defaultdict(lambda: 0.0)
        self.actions_by_state = defaultdict(set)

        self.i = 0

        self.epsilon = epsilon  # Probabilidad de exploración
        self.epsilon_0 = epsilon  # Valor inicial de epsilon

        self.alpha = alpha  # Tasa de aprendizaje
        self.alpha_0 = alpha

        self.gamma = gamma

        self.init_index = -1
        self.role = role


    def init_q_table(self, posibilities, init_index):
        """
        Inicializa la tabla Q con valores 0 para cada par estado-acción.
        """
        for i, states in enumerate(posibilities):
            for state in states:
                if len(state) == 2 and state[0] == -1:
                    self.q_table[(i, "__None__")] = state[1]
                    self.actions_by_state[i].add("__None__")
                else:
                    assert len(state) == 5
                    self.q_table.setdefault((i, state[1]), 0.0)
                    self.actions_by_state[i].add(state[1])

        self.init_index = init_index
    
    def q_iteration(self):
        self.i += 1
        # Decrecer epsilon después de cada iteración para reducir la exploración a medida que el agente aprende
        self.epsilon = self.epsilon_0 / (1 + (1/2000) * self.i)  # Decrecimiento de epsilon
        self.alpha = self.alpha_0 / (1 + (1/2000) * self.i)  # Decrecimiento de la tasa de aprendizaje

    def get_iteration(self) -> int:
        return self.i

    def get_actions(self, index):
        return list(self.actions_by_state.get(index, []))


    def update_column(self, index, action, next_state, reward):
        key = (index, action)
        assert key in self.q_table

        # Obtener el valor máximo de Q en el siguiente estado
        if self.role == "MAX":
            next_value = max((self.q_table.get((next_state, a), 0.0) for a in self.get_actions(next_state)), default=0.0)
        else:
            next_value = min((self.q_table.get((next_state, a), 0.0) for a in self.get_actions(next_state)), default=0.0)

        # Actualización de la tabla Q
        self.q_table[key] = ((1 - self.alpha) * self.q_table[key]) + (self.alpha * (reward + self.gamma * next_value))
        self.q_iteration()

    def choose_action(self, index, actions):
        """
        Elige una acción usando ε-greedy: exploración o explotación.
        """
        if random.random() < self.epsilon:
            return random.choice(actions)  # Exploración

        # Explotación: elegir la mejor acción
        state_values = [(a, self.q_table.get((index, a), 0.0)) for a in actions]
        if self.role == "MAX":
            return max(state_values, key=lambda x: x[1])[0] if state_values else random.choice(actions)
        return min(state_values, key=lambda x: x[1])[0] if state_values else random.choice(actions)

    def display_q_table(self):
        """
        Muestra el contenido actual de la tabla Q.
        """
        print("Tabla Q:")
        for (state, action), value in sorted(self.q_table.items()):
            print(f"Estado: {state}, Acción: {action}, Valor: {value:.4f}")

    def convergence(self, index):
        if self.role == "MAX": value = max((self.q_table.get((index, a), 0.0) for a in self.get_actions(index)), default=0.0)
        else: value = min((self.q_table.get((index, a), 0.0) for a in self.get_actions(index)), default=0.0)
        return value
    
    def ready(self, index, actions):
        # Explotación: elegir la mejor acción según la tabla Q
        state_values = [(a, self.q_table.get((index, a), 0.0)) for a in actions]
        if self.role == "MAX":
            return max(state_values, key=lambda x: x[1])[0] if state_values else random.choice(actions)
        return min(state_values, key=lambda x: x[1])[0] if state_values else random.choice(actions)