import hashlib


class Transformer:
    def __init__(self) -> None:
        self.state_max_val = {}
        self.max_z = -1

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
    
    def hash(self, state_bin, z):
        """
        Genera un número 'aleatorio' determinístico basado en el estado y z.

        Args:
            state_bin (str): Estado representado en binario (por ejemplo, 10001).
            z (int): Valor de z.

        Returns:
            int: Número 'aleatorio' determinístico generado.
        """
        
        # Convertir z a binario con padding basado en max_z
        z_bin = format(z, f'0{self.max_z.bit_length()}b')
        
        # Concatenar state_bin y z_bin
        combined = state_bin + z_bin
        
        # Usar hashlib para generar un hash determinístico
        hash_object = hashlib.sha256(combined.encode())  # Genera un hash SHA-256
        hash_value = int(hash_object.hexdigest(), 16)  # Convertir el hash a entero
        
        # Retornar el hash como entero
        return hash_value

# Ejemplo de uso
transitions = [
    ['t=0', 'x=0', 'y=0'], ['t=0', 'x=0', 'y=1'], ['t=0', 'x=0', 'y=2'],
    ['t=0', 'x=1', 'y=0'], ['t=0', 'x=1', 'y=1'], ['t=0', 'x=1', 'y=2'],
    ['t=0', 'x=2', 'y=0'], ['t=0', 'x=2', 'y=1'], ['t=0', 'x=2', 'y=2'],
    ['t=1', 'x=0', 'y=0'], ['t=1', 'x=0', 'y=1'], ['t=1', 'x=0', 'y=2'],
    ['t=1', 'x=1', 'y=0'], ['t=1', 'x=0', 'y=1'], ['t=1', 'x=1', 'y=2'],
    ['t=1', 'x=2', 'y=0'], ['t=1', 'x=2', 'y=1'], ['t=1', 'x=2', 'y=2']
]

transformer = Transformer()
transformer.calculate_state_max_val(transitions)

# Configurar el máximo z
transformer.set_max_z(1000)

z = 0
hash_value = 0
veces_0 = 0
veces_1 = 0
veces_2 = 0
veces_3 = 0

for t in transitions:
    state_bin = transformer.state_to_bin(t)
    for z in range(1000):
        hash_value = transformer.hash(state_bin, z)
        if hash_value % 4 == 0: veces_0 +=1
        elif hash_value % 4 == 1: veces_1 += 1
        elif hash_value % 4 == 2: veces_2 += 1
        else: veces_3 += 1

print('Veces 0: ', veces_0)
print('Veces 1: ', veces_1)
print('Veces 2: ', veces_2)
print('Veces 3: ', veces_3)
