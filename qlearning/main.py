import numpy as np

# Parámetros Q-learning
alpha = 0.1  # Tasa de aprendizaje
gamma = 0.9  # Factor de descuento
epsilon = 0.1  # Probabilidad de exploración

# Inicializar la tabla Q

class Q_table:
    def __init__(self) -> None:
        self.q_table = []
        self.i = 0

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
        i = 0
        while i < len(self.q_table):
            if self.q_table[i]['vars'] == state and self.q_table[i]['act'] == action:
                return i

            i += 1

        return -1
    
    def get_q_value(self, state, action):
        """
        Devuelve el valor Q para un par de estado y acción si existe,
        de lo contrario devuelve 0.
        """
        i = self.find_column(state, action)
        if i != -1:
            return self.q_table[i]['value']
        else:
            return 0.0

    def display_q_table(self):
        """
        Imprime la tabla Q.
        """
        print("Tabla Q actual:")
        for entry in self.q_table:
            print(entry)
    
    def q_iteration(self):
        self.i += 1
    def get_iteration(self) -> int:
        return self.i