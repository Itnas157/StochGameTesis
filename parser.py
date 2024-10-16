def parse_trans_str(t):
    trans_str = t.replace('\n', '')
    trans = trans_str.split(';')
    trans.pop()
    return trans

def qlearning_parser(transitions, curr_vars):
    options = []

    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        pred_valid = True
        for pred in sets[0].split(" ^ "):
            pred_valid = pred_valid and pred in curr_vars
        if pred_valid: options.append(sets[1])

    return options

def get_states(transitions):
    states = []
    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        state = []
        for pred in sets[0].split(" ^ "):
            state.append(pred)
        
        if not state in states: states.append(state)
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