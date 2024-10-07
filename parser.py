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