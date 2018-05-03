from class_obj import State
from mdp import *


def run_mdp_on_system(policy="rand"):
    cur_state = State(get_first_state())
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    while n_inserted_items < N_CYCLES:
        immidiate_reward, new_state, chosen_action = choose_action_to_move(cur_state, method=policy)
        n_inserted_items += 1
        total_time_of_system += immidiate_reward
        all_processed_items[chosen_action] += 1
        cur_state = State(new_state)  #get_round
        print "A"
    print "-->>> Finished processing %s items, in total time of %s" % (N_CYCLES, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items


#run_mdp_on_system(policy="greedy")
run_mdp_on_system(policy="epsilon-greedy")
