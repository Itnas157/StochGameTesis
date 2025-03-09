def parse_trans_str(t):
    trans = t.split('\n')
    trans = [tr for tr in trans if not tr.startswith("--") and tr.strip()]
    return trans

def final_states_reward(transitions, curr_vars):
    options = []
    state = {}

    for v in curr_vars:
        dupla = v.split("=")
        assert(len(dupla) == 2)
        state[dupla[0]] = dupla[1]

    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        sets[0] = sets[0].replace("qf: ", "")
        predicates = sets[0].split(" ^ ")
        expanded_predicates = {}

        for pred in predicates:
            for var, values in expand_ranges(pred):
                expanded_predicates[var] = values

        # Validar si el estado actual cumple con todos los predicados
        if all(var in state and state[var] in valid_values for var, valid_values in expanded_predicates.items()):
            options.append(sets[1])
    
    # Caso de múltiple estados finales
    if len(options) > 1:
        if '-1' in options and '1' in options:
            return 0
        elif '-1' in options:
            return -1
        elif '1' in options:
            return 1

    assert len(options) == 1 or len(options) == 0
    return options[0] if len(options) > 0 else None

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


import random
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

    return vars_values

def get_comb(non_final_states, final_states, init_vars):
    vars_values = get_states(non_final_states, final_states, init_vars)
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
            right = re.sub(r'\b' + var + r'\b', var_dict[var], right)

    # Evaluar la expresión matemática del lado derecho
    try:
        right_value = eval(right)
    except Exception as e:
        raise ValueError(f"Error al evaluar la expresión '{right}': {e}")

    # Devolver la asignación con el cálculo resuelto
    return f"{left}={right_value}"

def chose_action(curr_vars, action, non_final_states):
    """
    Elige una acción y actualiza las variables actuales.
    """
    for t in non_final_states:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        action_div = sets[1].split("!!!")
        if action_div[-1] == action:
            state_changes = action_div[0].strip(" | ")
            changes_with_probs = state_changes.split()

            for change in changes_with_probs:
                prob, state_change = change.split(': ')
                if all(var in state_change for var in curr_vars):
                    return state_change

    return None



###### DEFINITIVE:

class Parser:
    def __init__(self, example, init_vars):
        # Example sin parsear
        self.example = example

        # Variables iniciales
        self.init_vars = init_vars

        # Variables actuales
        self.current_vars = init_vars

        # Nombres de variables
        self.var_names = [var.split("=")[0] for var in init_vars]

        # Estados finales
        example_no_comments = example.split('\n')
        example_no_comments = [tr for tr in example_no_comments if not tr.startswith("--") and tr.strip()]

        self.final_states = [tr for tr in example_no_comments if tr.startswith("qf: ")]

        # Estados no finales
        self.non_final_states = [tr for tr in example_no_comments if not tr.startswith("qf: ")]

        # Todos los estados
        self.all_combinations = get_comb(self.non_final_states, self.final_states, self.init_vars)
        print(len(self.all_combinations), "estados generados.")

        # Acciones
        self.actions = get_actions(self.non_final_states)
        pass

    def get_combinations(self):
        return self.all_combinations
        
    def get_actions(self, options):
        actions = []
        for opt in options:
            split = opt.split(" !!!")
            assert len(split) == 2

            if split[1] not in actions:
                actions.append(split[1])
        return actions
    
    def get_options(self, curr_vars):
        return qlearning_parser(self.non_final_states, curr_vars)
    
    def get_vars(self):
        return self.current_vars
    
    def update_vars(self, action, options):
        for opt in options:
            split = opt.split(" !!!")
            assert len(split) == 2

            accumulative_prob = 0
            rand = random.random()
            if split[1] == action:
                for prob in split[0].split(" | "):
                    if rand < accumulative_prob + float(prob.split(": ")[0]):
                        for assign in prob.split(": ")[1].split(";"):
                            new_var = parse_assign(assign, self.current_vars)

                            new_vars = []
                            for var in self.current_vars:
                                if var.split("=")[0] == new_var.split("=")[0]:
                                    new_vars.append(new_var)
                                else:
                                    #print(f"{var} != {new_var}")
                                    new_vars.append(var)

                            self.current_vars = new_vars
                            #self.current_vars = [new_var if var.split("=")[0] == new_var.split("=")[0] else var for var in self.current_vars]
                        return
                    else:
                        accumulative_prob += float(prob.split(": ")[0])

    def get_reward(self):
        final_states = final_states_reward(self.final_states, self.current_vars)
        return final_states

    def reset_vars(self):
        self.alternate_turns()
        self.current_vars = self.init_vars
    
    def get_var(self, var_name):
        for var in self.current_vars:
            if var.split("=")[0] == var_name:
                return var.split("=")[1]
        return None
    

    def is_final_state(self, state):
        for t in self.final_states:
            condition = t.split(" -> ")[0]
            condition = condition.replace("qf: ", "")
            conditions = condition.split(" ^ ")
            
            checks_all_conditions = True

            for c in conditions:
                var, values = from_assign_get_var(c)
                for assign in state:
                    var2, values2 = from_assign_get_var(assign)
                    if var == var2 and values2[0] not in values:
                        checks_all_conditions = False
            
            if checks_all_conditions:
                return True

        return False


    def get_all_posibilities(self):
        all_posibilities = []

        for state in self.all_combinations:
            if self.is_final_state(state):
                all_posibilities.append({
                    'vars': state,
                    'action': '__None__'
                })
            else:
                for opt in self.get_options(state):
                    all_posibilities.append({
                        'vars': state,
                        'action': opt.split(" !!!")[1]
                    })

        return all_posibilities
    
    def alternate_turns(self):
        if "t=0" in self.init_vars:
            self.init_vars = [var if var.split("=")[0] != "t" else "t=1" for var in self.init_vars]
        elif "t=1" in self.init_vars:
            self.init_vars = [var if var.split("=")[0] != "t" else "t=0" for var in self.init_vars]