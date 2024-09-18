from examples.example_alternative import trans_str, vars

trans_str = trans_str.replace('\n', '')
trans = trans_str.split(';')
trans.pop()

#print(trans)

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

parser_res = qlearning_parser(trans, curr_vars=vars)

def get_states(transitions):
    states = []
    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        state = []
        for pred in sets[0].split(" ^ "):
            state.append(pred)
        
        states.append(state)

def get_actions(transitions):
    actions = []
    for t in transitions:
        sets = t.split(" -> ")
        assert(len(sets) == 2)

        # Sets[0] sera los predicados
        action_div = sets[1].split("!")
        if len(action_div) > 1 and not action_div[-1] in actions: actions.append(action_div[-1])
        

get_states(transitions=trans)
get_actions(transitions=trans)