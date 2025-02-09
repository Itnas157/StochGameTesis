def parse_trans_str(t):
    trans = t.split('\n')
    trans = [tr for tr in trans if not tr.startswith("--") and tr.strip()]
    return trans


def qlearning_parser(transitions, curr_vars):
    """
    Filtra las acciones posibles según el estado actual (curr_vars).
    Retorna una lista con las acciones permitidas.
    """
    options = []
    state = {}

    for v in curr_vars:
        dupla = v.split("=")
        assert(len(dupla) == 2)
        state[dupla[0]] = dupla[1]

    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)
        
        predicates = sets[0].split(" ^ ")
        expanded_predicates = {}

        for pred in predicates:
            for var, values in expand_ranges(pred):
                expanded_predicates[var] = values

        # Validar si el estado actual cumple con todos los predicados
        if all(var in state and state[var] in valid_values for var, valid_values in expanded_predicates.items()):
            options.append(sets[1])

    return options


import re
from itertools import product

def expand_ranges(predicate):
    """ Expande expresiones como x=0|...|14 y ac=5|10 en una lista de listas de valores posibles. """
    range_match = re.match(r"(\w+)=([\d]+)\|[.]+\|([\d]+)", predicate)
    if range_match:
        var, start, end = range_match.groups()
        return [(var, [str(i) for i in range(int(start), int(end) + 1)])]

    multi_match = re.match(r"(\w+)=([\d]+(?:\|[\d]+)*)", predicate)
    if multi_match:
        var, values = multi_match.groups()
        return [(var, values.split("|"))]

    var, value = predicate.split("=")
    return [(var, [value])]



def from_assign_get_var(assign):
    split = assign.split("=")
    assert(len(split) == 2)
    
    assigning = split[1]
    if "|...|" in assigning:
        spl = assigning.split("|...|")
        return split[0], [str(i) for i in range(int(spl[0]), int(spl[1]) + 1)]
    elif "|" in assigning:
        spl = assigning.split("|")
        return split[0], spl

    return split[0], [split[1]]

def get_states(non_final_states, final_states, init_vars):
    """
    Obtiene todos los estados a partir de las transiciones.
    Soporta expresiones con rangos (e.g., x=0|...|14) y múltiples valores (e.g., ac=5|10).
    """
    vars_values = {}
    
    for v in init_vars:
        var_name, var_values = from_assign_get_var(v)
        vars_values[var_name] = var_values

    for t in final_states:
        condition = t.split(" -> ")[0]
        condition = condition.replace("qf: ", "")
        conditions = condition.split(" ^ ")
        
        for c in conditions:
            var, values = from_assign_get_var(c)
            vars_values[var] = vars_values[var] + [values for values in values if values not in vars_values[var]]
    
    for t in non_final_states:
        condition = t.split(" -> ")[0]
        conditions = condition.split(" ^ ")

        for c in conditions:
            var, values = from_assign_get_var(c)
            vars_values[var] = vars_values[var] + [values for values in values if values not in vars_values[var]]   
        
    print(vars_values)

    # Generar todas las combinaciones posibles de valores para cada variable

    all_combinations = list(product(*vars_values.values()))  # Genera las combinaciones

    # Convertir las combinaciones en estados con el formato "var=value"
    states = []
    for combination in all_combinations:
        state = [f"{list(vars_values.keys())[i]}={combination[i]}" for i in range(len(combination))]
        states.append(state)
    
    return states



def get_actions(transitions):
    actions = []
    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        action_div = sets[1].split("!")
        if len(action_div) > 1 and not action_div[-1] in actions: actions.append(action_div[-1])
    return actions


def parse_transition(transition):
    parts = transition.split('!')

    # Si no hay acción (es un estado final), retornamos la transición sin acción
    if len(parts) == 1:
        transition = parts[0].strip()
        return [(-1.0, transition)], None  # No hay acción asociada

    state_changes = parts[0].strip()
    action = parts[1].strip()

    # Las probabilidades y nuevos estados están antes de la acción (!)
    changes_with_probs = state_changes.split()
    
    # Parsear cada cambio de estado con su probabilidad
    transitions = []
    for change in changes_with_probs:
        prob, state_change = change.split(':')
        transitions.append((float(prob), state_change))
    
    return transitions, action



import re

def parse_assign(expresion, vars):
    """
    Procesa una expresión de asignación, reemplaza las variables en el lado derecho
    con sus valores y realiza el cálculo.
    """
    # Convertir vars en un diccionario para facilitar la búsqueda
    var_dict = {var.split("=")[0]: var.split("=")[1] for var in vars}

    # Separar la expresión en dos partes: lado izquierdo y derecho de la asignación
    left, right = expresion.split("=")

    # Buscar las variables dentro del lado derecho (por ejemplo, 'y', 'ac')
    variables = re.findall(r'\b\w+\b', right)

    # Reemplazar las variables en el lado derecho con sus valores
    for var in variables:
        if var in var_dict:
            right = right.replace(var, var_dict[var])

    # Evaluar la expresión matemática del lado derecho
    try:
        right_value = eval(right)
    except Exception as e:
        raise ValueError(f"Error al evaluar la expresión '{right}': {e}")

    # Devolver la asignación con el cálculo resuelto
    return f"{left}={right_value}"




###### DEFINITIVE:

class Parser:
    def __init__(self, example, init_vars):
        # Example sin parsear
        self.example = example

        # Variables iniciales
        self.init_vars = init_vars

        # Nombres de variables
        self.var_names = [var.split("=")[0] for var in init_vars]

        # Estados finales
        example_no_comments = example.split('\n')
        example_no_comments = [tr for tr in example_no_comments if not tr.startswith("--") and tr.strip()]

        self.final_states = [tr for tr in example_no_comments if tr.startswith("qf: ")]

        # Estados no finales
        self.non_final_states = [tr for tr in example_no_comments if not tr.startswith("qf: ")]

        # Todos los estados
        self.all_combinations = get_states(self.non_final_states, self.final_states, self.init_vars)
        print(len(self.all_combinations), " estados generados.")
