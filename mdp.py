# from run_process import *
from CONFIG import *
from utils import sum_dicts, constract_finished_items_dict
from system_dynamics import init_production_line, run_one_cycle, add_item_to_line, workers_change_bb
from stochasic_arrival import *
from class_obj import State
# generating the first state (state is defined when the last worker finishes its work)
# in the production line:


def get_first_state():
    """
    :return: state, defined by : workers order in stations, items in the production line, items waiting in queue.
    """
    workers_prod_line, items_prod_line, all_items_in_queue = init_production_line()
    cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
                                                                                        items_prod_line)
    all_items_in_queue = sum_dicts(all_items_in_queue, items_arrive_in_process)
    return [workers_prod_line, items_prod_line, all_items_in_queue]


def choose_action_to_move_greedy(state):
    if len(state.available_items) > 0:
        state.calc_rewards_for_actions()
        # TODO - not sure it's the minimum!!
        greedy_best_action = min(state.rewards_states.iteritems(), key=operator.itemgetter(1))[0]
        immidiate_reward = state.rewards_states[greedy_best_action][REWARD]
        new_state = state.rewards_states[greedy_best_action][NEXT_STEP]
        return immidiate_reward, new_state, greedy_best_action
    else:
        t = time_to_event(total_lamb)
        action = get_random_item_type()
        cycle_time, new_state = state.calc_reward_per_state(action=action)
        return cycle_time + t, new_state, action


