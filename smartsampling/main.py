import hashlib
import random

class Transformer:
    def __init__(self) -> None:
        self.state_max_val = {}
        self.max_z = -1
        self.zs= []

    def calculate_state_max_val(self, transitions):
        """
        Calcula los valores máximos de cada variable de estado a partir de las transiciones.

        Args:
            transitions (list of list): Lista de transiciones, donde cada transición es una lista de estados.
        """
        # Iterar sobre todas las transiciones
        for transition in transitions:
            for state in transition:
                # Dividir cada estado en clave=valor
                var, val = state.split('=')
                val = int(val)  # Convertir a entero
                
                # Actualizar el valor máximo de la variable si es necesario
                if var not in self.state_max_val:
                    self.state_max_val[var] = val
                else:
                    self.state_max_val[var] = max(self.state_max_val[var], val)
    
    def state_to_bin(self, state) -> str:
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
            max_val = self.state_max_val[var]
            num_bits = max_val.bit_length()  # Número de bits necesarios para representar el máximo valor

            # Convertir el valor actual a binario con padding
            bin_repr += format(val, f'0{num_bits}b')
        
        return bin_repr
    
    def set_max_z(self, z):
        self.max_z = z
        self.zs = [i for i in range(z)]
    
    def update_zs(self, z_keys):
        self.zs = z_keys + z_keys

    def hash(self, state, z):
        """
        Genera un número 'aleatorio' determinístico basado en el estado y z.

        Args:
            state: Estado.
            z (int): Valor de z.

        Returns:
            int: Número 'aleatorio' determinístico generado.
        """
        
        # Convertir z a binario con padding basado en max_z
        z_bin = format(z, f'0{self.max_z.bit_length()}b')
        
        # Concatenar state_bin y z_bin
        combined = self.state_to_bin(state) + z_bin
        
        # Usar hashlib para generar un hash determinístico
        hash_object = hashlib.sha256(combined.encode())  # Genera un hash SHA-256
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

