import random
import re
from itertools import product

import numpy as np

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
        return split[0], [i for i in range(int(spl[0]), int(spl[1]) + 1)]
    elif "|" in assigning:
        spl = assigning.split("|")
        return split[0], [int(i) for i in spl]

    return split[0], [int(split[1])]

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


def calculate_next_state(state, assigns):
    new_vars = state.copy()
    for assign in assigns.split(";"):
        new_var = parse_assign(assign, state)
        
        for i in range(len(new_vars)):
            if new_vars[i].split("=")[0] == new_var.split("=")[0]:
                new_vars[i] = new_var

    return new_vars

def get_comb(non_final_states, final_states, init_vars):
    vars_values = get_states(non_final_states, final_states, init_vars)
    # Generar todas las combinaciones posibles de valores para cada variable

    #print(non_final_states)

    all_combinations = list(product(*vars_values.values()))  # Genera las combinaciones
    #print(all_combinations)

    # Convertir las combinaciones en estados con el formato "var=value"
    states = []
    for combination in all_combinations:
        state = [f"{list(vars_values.keys())[i]}={combination[i]}" for i in range(len(combination))]
        states.append(state)
    
    return states

def create_parser_table(states, non_final_states, final_states, init_vars, bins):
    tuples = []
    state_index = {tuple(states[i]): i for i in range(len(states))}  # Índices rápidos
    index_init = None

    assert len(states) == len(bins)
    
    for i in range(len(states)):
        state = states[i]
        bin = bins[i]
    
        t_value = from_assign_get_var(state[0])
        assert t_value[0] == 't'
        t = t_value[1][0]

        reward = final_states_reward(final_states, state)
        if reward is not None:
            tuples.append([(-1, float(reward), state, "__None__", bin, t)])  # t = 1 para estados finales
        else:
            options = qlearning_parser(non_final_states, state)
            state_entries = []
            
            for opt in options:
                action = opt.split(" !!!")[1]
                assigns = opt.split(" !!!")[0]
                
                for poss in assigns.split(" | "):
                    tmp = poss.split(": ")
                    prob_tuple = (float(tmp[0]), tmp[1], state, action, bin, t)  # t = 0 para transiciones normales
                    state_entries.append(prob_tuple)
            
            tuples.append(state_entries)

    rewards = []
    for t in tuples:
        if t[0][0] == -1 and not t[0][1] in rewards: rewards.append(t[0][1])

    # Añadir siguientes estados
    for i in range(len(tuples)):
        for j in range(len(tuples[i])):
            poss = tuples[i][j]
            if poss[0] == -1:
                next_index = rewards.index(poss[1])
                tuples[i][j] = poss + (next_index,)

    for i in range(len(tuples)):
        for j in range(len(tuples[i])):
            poss = tuples[i][j]
            if poss[0] != -1:
                next_state = calculate_next_state(poss[2], poss[1])
                next_index = state_index.get(tuple(next_state), None)
                if tuples[next_index][0][0] == -1: next_index = tuples[next_index][0][6]
                tuples[i][j] = poss + (next_state, next_index)

    new_tuples = [[(-1, r)] for r in rewards]
    c = len(new_tuples)
    for poss in tuples:
        if poss[0][0] != -1:
            new_poss = []
            for t in poss:
                new_poss.append((t[0], t[3], t[4], t[5], t[2]))
                if t[2] == init_vars: index_init = c
            new_tuples.append(new_poss)
            c += 1
    
    assert not index_init is None

    final_tuples = [[(-1, r)] for r in rewards]

    for i in range(len(new_tuples)):
        if new_tuples[i][0][0] != -1:
            new_poss = []
            index = -1
            for j in range(len(new_tuples[i])):
                action = new_tuples[i][j][1]
                state = new_tuples[i][j][4]

                while index == -1:
                    for t_i in range(len(tuples)):
                        if tuples[t_i][j][2] == state:
                            index = t_i
                            break
                
                pointing = tuples[index][j][7]
                if pointing >= len(rewards):
                    for second_i in range(len(new_tuples)):
                        if new_tuples[second_i][0][0] != -1 and new_tuples[second_i][0][4] == tuples[pointing][0][2]:
                            pointing = second_i
                            break
                
                new_poss.append((new_tuples[i][j][0], new_tuples[i][j][1], new_tuples[i][j][2], new_tuples[i][j][3], pointing))
            final_tuples.append(new_poss)

    
    tuples = [np.array(t, dtype=object) for t in final_tuples]
    
    return tuples, index_init

def update_parser_table_with_hash(table, hashes):
    tuples = []
    for t in table:
        tuples.append()


def get_actions(transitions):
    actions = []
    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        action_div = sets[1].split("!!!")
        if len(action_div) > 1 and not action_div[-1] in actions: actions.append(action_div[-1])
    return actions


def parse_transition(transition):
    parts = transition.split('!!!')

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


        self.table = []
        self.index_init = -1

        # Acciones
        self.actions = get_actions(self.non_final_states)
    
    def create_table(self, bins):
        self.table, self.index_init = create_parser_table(self.all_combinations, self.non_final_states, self.final_states, self.init_vars, bins)

        # Variables actuales
        self.current_index = self.index_init

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
    
    def get_options(self):
        actions = []
        for opt in self.table[self.current_index]:
            if not opt[1] in actions: actions.append(opt[1])
        return actions, self.table[self.current_index]
    
    def get_vars(self):
        return self.table[self.current_index]
    
    def update_vars(self, action, options):
        for opt in options:
            accumulative_prob = 0
            rand = random.random()
            if opt[1] == action:
                if rand < accumulative_prob + opt[0]:
                    self.current_index = opt[4]

    def get_reward(self):
        return self.table[self.current_index][0][1] if self.table[self.current_index][0][0] == -1 else None

    def reset_vars(self):
        self.current_index = self.index_init
    
    def get_t(self):
        return self.table[self.current_index][0][3]


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
    

    def get_init_states(self):
        options = self.get_options(self.init_vars)
        init_states = []
        for opt in options:
            init_states.append({
                'vars': self.init_vars,
                'action': opt.split(" !!!")[1]
            })
        return init_states
    
    def calculate_state_max_value(self) -> dict:
        """
        Calcula los valores máximos de cada variable de estado a partir de las transiciones.

        Args:
            transitions (list of list): Lista de transiciones, donde cada transición es una lista de estados.
        """
        # Iterar sobre todas las transiciones
        vars = {}

        for transition in self.non_final_states + self.final_states:
            t = transition.replace("qf: ", "")
            precs = t.split(" -> ")[0]
            for prec in precs.split(" ^ "):
                # Dividir cada estado en clave=valor
                var, vals = from_assign_get_var(prec)
                if not var in vars.keys(): vars[var] = max(vals)
                else: vars[var] = max([vars[var]] + vals)
        
        return vars
    
    def get_table(self):
        return self.table
    
    def get_bin(self):
        return self.table[self.current_index][0][2]