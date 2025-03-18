import hashlib
import random

def state_to_bin(state, state_max_val) -> str:
        """
        Convierte un estado a un número binario basado en los bits necesarios según state_max_val.

        Args:
            state (list): Estado representado como una lista de variables (por ejemplo, ['t=0', 'x=0', 'y=1']).

        Returns:
            str: Representación binaria del estado.
        """
        bin_repr = ""
        for var_val in state:
            var, val = var_val.split('=')
            val = int(val)
            
            # Determinar el número de bits necesarios para esta variable
            if var in state_max_val.keys():
                max_val = state_max_val[var]
                num_bits = max_val.bit_length()  # Número de bits necesarios para representar el máximo valor

                # Convertir el valor actual a binario con padding
                bin_repr += format(val, f'0{num_bits}b')
        
        return bin_repr

class Transformer:
    def __init__(self, max_z) -> None:
        self.state_max_val = {}
        self.max_z = max_z
        self.zs= [i for i in range(max_z)]

    def set_state_max_val(self, max_values):
        self.state_max_val = max_values
        
    def update_zs(self, z_keys):
        self.zs = z_keys

    def hash(self, state, z):
        # Convertir z a binario con padding basado en max_z
        z_bin = format(z, f'0{self.max_z.bit_length()}b')
        
        # Concatenar state_bin y z_bin
        h = state + z_bin
        
        # Usar hashlib para generar un hash determinístico
        hash_object = hashlib.sha256(h.encode())  # Genera un hash SHA-256
        hash_value = int(hash_object.hexdigest(), 16)  # Convertir el hash a entero
        
        # Retornar el hash como entero
        return hash_value
    
    def choose_action(self, hash_value, actions):
        """
        Elige la accion en base al hash_value
        """
        return actions[hash_value % len(actions)]
    
    def get_random_z(self):
        return random.choice(self.zs)


