from run_process import *

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


def calc_reward_per_state(state, action=I3):
    """
    :param state:
    :param action:
    :return: cycle_time = immidiate reward.
    """
    workers_prod_line, items_prod_line, all_items_in_queue = state
    # add the new item to the production
    items_prod_line = add_item_to_line(items_prod_line, ITEMS_WORK_DIST_DICT, chosen_item=action)
    # re-arrange the workers
    workers_prod_line = workers_change_bb(workers_prod_line)
    # remove the chosen item for queue
    all_items_in_queue[action] -= 1
    # run a cycle. finished when last item finish!
    cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
                                                                                        items_prod_line)
    all_items_in_queue = sum_dicts(all_items_in_queue, items_arrive_in_process)
    new_state = [workers_prod_line, items_prod_line, all_items_in_queue]
    return cycle_time, new_state


def choose_action_move_state(state):
    # TODO change the name of the funvtion
    workers_prod_line, items_prod_line, all_items_in_queue = state
    avail_items = np.unique([i[0] for i in all_items_in_queue.items() if i[1] > 0])
    if len(avail_items) > 0:
        action_values = defaultdict(list)
        for action in avail_items:
            cycle_time, new_state = calc_reward_per_state(state, action=action)
            action_values[action] = [cycle_time, new_state]
        greedy_best_action = min(action_values.iteritems(), key=operator.itemgetter(1))[0]
        immidiate_reward = action_values[greedy_best_action][0]
        new_state = action_values[greedy_best_action][1]
        return immidiate_reward, new_state, greedy_best_action
    else:
        t = time_to_event(total_lamb)
        action = get_random_item_type()
        cycle_time, new_state = calc_reward_per_state(state, action=action)
        return cycle_time + t, new_state, action


# state = get_first_state()
# # immidiate_reward, new_state = calc_reward_per_state(state, action=I3)
# immidiate_reward, new_state, chosen_action = choose_action_greedy(state)
# print "bye"


def main():
    state = get_first_state()
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    while n_inserted_items < N_CYCLES:
        immidiate_reward, new_state, chosen_action = choose_action_move_state(state)
        state = new_state
        n_inserted_items += 1
        total_time_of_system += immidiate_reward
        all_processed_items[chosen_action] += 1
    print "-->>> Finished processing %s items, in total time of %s" % (N_CYCLES, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items

main()
#C:\Users\shkotler\Documents\thesis\BBSystem\mdp.py
