import json
import random
import re
from itertools import product
import time

import numpy as np

def timer(func):
    """Decorador para medir el tiempo de ejecución de una función."""
    def wrapper(*args, **kwargs):
        start = time.perf_counter()  # Inicia el cronómetro
        result = func(*args, **kwargs)  # Ejecuta la función
        end = time.perf_counter()  # Detiene el cronómetro
        print(f"{func.__name__} tardó {end - start:.6f} segundos en ejecutarse")
        return result  # Devuelve el resultado original
    return wrapper

def final_states_reward(transitions, state):
    for t in transitions:
        left, _, right = t.partition(" -> ")
        predicates = left.removeprefix("qf: ").split(" ^ ")
        
        expanded_predicates = {
            var: values for pred in predicates for var, values in expand_ranges(pred)
        }

        # Validar si el estado actual cumple con todos los predicados
        if all(state.get(var) in valid_values for var, valid_values in expanded_predicates.items()):
            if right in {"-1", "1"}:  # Salida temprana si se encuentra ambos valores
                return 0 if "-1" in expanded_predicates and "1" in expanded_predicates else int(right)
            return right

    return None


def qlearning_parser(transitions):
    options = []

    for t in transitions:
        left, _, right = t.partition(" -> ")
        
        predicates = left.split(" ^ ")
        expanded_predicates = {}

        for pred in predicates:
            for var, values in expand_ranges(pred):
                expanded_predicates[var] = values

        possibilities = []
        assigns, _, action = right.partition(" !!!")  # Más rápido que split(" !!!")[1]
        for poss in assigns.split(" | "):
            prob, _, state_str = poss.partition(": ")  # Más eficiente que split(": ")
            possibilities.append((float(prob), state_str, action))


        options.append((expanded_predicates, possibilities))

    return options




def expand_ranges(predicate):
    """ Expande expresiones como x=0|...|14 y ac=5|10 en una lista de listas de valores posibles. """
    range_match = re.match(r"(\w+)=([\d]+)\|[.]+\|([\d]+)", predicate)
    if range_match:
        var, start, end = range_match.groups()
        return [(var, [i for i in range(int(start), int(end) + 1)])]

    multi_match = re.match(r"(\w+)=([\d]+(?:\|[\d]+)*)", predicate)
    if multi_match:
        var, values = multi_match.groups()
        return [(var, [int(i) for i in values.split("|")])]

    var, value = predicate.split("=")
    return [(var, [int(value)])]



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

    # Separar la expresión en dos partes: lado izquierdo y derecho de la asignación
    left, right = expresion.split("=")

    # Buscar las variables dentro del lado derecho (por ejemplo, 'y', 'ac')
    variables = re.findall(r'\b\w+\b', right)

    # Reemplazar las variables en el lado derecho con sus valores
    for var in variables:
        if var in vars:
            right = re.sub(r'\b' + var + r'\b', vars[var], right)

    # Evaluar la expresión matemática del lado derecho
    try:
        right_value = eval(right)
    except Exception as e:
        raise ValueError(f"Error al evaluar la expresión '{right}': {e}")

    # Devolver la asignación con el cálculo resuelto
    return left, right_value


def calculate_next_state(state, assigns):
    new_vars = state.copy()
    for assign in assigns.split(";"):
        key, new_var = parse_assign(assign, state)
        new_vars[key] = new_var

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

@timer
def create_parser_table(states, non_final_states, final_states, init_vars, bins):
    tuples = []
    index_init = None

    assert len(states) == len(bins)
    
    t_values = list(map(from_assign_get_var, (state[0] for state in states)))
    final_states = set(final_states)
    non_final_states = set(non_final_states)

    init_vars = {k: int(v) for k, _, v in (var.partition("=") for var in init_vars)}
    states = [{k: int(v) for k, _, v in (var.partition("=") for var in state)} for state in states]

    options = qlearning_parser(non_final_states)

    for state, bin, t_value in zip(states, bins, t_values):
        #print(i); i+=1
        assert t_value[0] == 't'
        t = t_value[1][0]

        reward = final_states_reward(final_states, state)
        if reward is not None:
            tuples.append([(-1, float(reward), state, "__None__", bin, t)])  # t = 1 para estados finales
        else:
            state_entries = []
            for opt in options:
                if all(state.get(var) in valid_values for var, valid_values in opt[0].items()):
                    for poss in opt[1]:
                        state_entries.append((poss[0], poss[1], state, poss[2], bin, t))
            
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


    state_index_map = {frozenset(tuples[t][0][2].items()): t for t in range(len(tuples))}
    # Iterar sobre la lista de tuples
    for i, sublist in enumerate(tuples):
        for j, poss in enumerate(sublist):
            if poss[0] == -1:
                continue  # Saltar si es -1 (estado final)
            
            next_state = calculate_next_state(poss[2], poss[1])
            next_state_key = frozenset(next_state.items())
            next_index = state_index_map.get(next_state_key, -1)

            assert next_index != -1, f"Estado {next_state} no encontrado en state_index_map"

            # Si el estado es final, asignar índice alternativo
            if tuples[next_index][0][0] == -1:
                next_index = tuples[next_index][0][6]

            # Reemplazar la tupla original con la nueva versión
            sublist[j] = poss + (next_state, next_index)

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

    pointing_map = {frozenset(new_tuples[i][0][4].items()): i for i in range(len(new_tuples)) if new_tuples[i][0][0] != -1}

    for i, sublist in enumerate(new_tuples):
        if sublist[0][0] == -1:
            continue  # Saltar si es un estado final
        
        new_poss = []
        for j, poss in enumerate(sublist):
            state = poss[4]  # new_tuples[i][j][4]
            # Buscar el índice del estado en `tuples`
            index = state_index_map.get(frozenset(state.items()), -1)
            assert index != -1, f"Estado {state} no encontrado en tuples"
            
            # Obtener `pointing`
            pointing = tuples[index][j][7]
            
            # Validar si `pointing` está dentro del rango de `rewards`
            if pointing >= len(rewards):
                pointing = pointing_map.get(frozenset(tuples[pointing][0][2].items()), pointing)
            
            # Construir nueva tupla optimizada
            new_poss.append((poss[0], poss[1], poss[2], poss[3], pointing))
        
        # Agregar a final_tuples manteniendo su estructura original
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
        accumulative_prob = 0
        rand = random.random()
        for opt in options:
            if opt[1] == action:
                accumulative_prob += opt[0]
                if rand < accumulative_prob:
                    #print(rand, accumulative_prob, opt)
                    self.current_index = opt[4]
                    break

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