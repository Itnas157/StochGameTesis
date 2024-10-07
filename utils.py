import itertools


def get_vars_names(vars):
    var_names = []
    for v in vars:
        assign= v.split("=")
        assert(len(assign)==2)
        var_names.append(assign[0])
    return var_names

def assign_is_var(assign, var) -> bool:
    return assign.split("=")[1] == var

def get_var_values(transitions, var_name):
    """
    Obtiene todos los posibles valores que puede tomar una variable en base a las transiciones.
    """
    values = set()
    for t in transitions:
        # Consideramos tanto las asignaciones en la parte de la izquierda como en la derecha
        for assignment in t:
            assert("=" in assignment)
            var, value = assignment.split("=")
            if var == var_name:
                values.add(value)
    return sorted(values)  # Ordenar para consistencia

def get_all_states(transitions, init_vars):
    """
    Genera todos los estados posibles en base a las variables y sus valores posibles.
    """
    var_names = get_vars_names(init_vars)  # Obtiene los nombres de las variables (ejemplo: ["t", "x", "y"])

    # Obtener todos los valores posibles para cada variable
    var_values = {var: get_var_values(transitions, var) for var in var_names}
    
    # Generar todas las combinaciones posibles de valores para cada variable
    all_combinations = list(itertools.product(*var_values.values()))  # Genera las combinaciones

    # Convertir las combinaciones en estados con el formato "var=value"
    all_states = []
    for combination in all_combinations:
        state = [f"{var_names[i]}={combination[i]}" for i in range(len(combination))]
        all_states.append(state)

    return all_states
