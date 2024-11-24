from parser import get_states, get_actions, parse_trans_str, qlearning_parser, parse_transition
from utils import get_all_states, update_state
from examples.example_alternative import init_vars, trans_str

trans_raw = parse_trans_str(trans_str)
vars = init_vars

states = get_states(trans_raw)
actions = get_actions(trans_raw)

print(states)
print(actions)

all_states = get_all_states(transitions=states, init_vars=init_vars)
print(all_states)