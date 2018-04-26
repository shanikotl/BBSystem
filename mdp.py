from run_process import *

# generating the first state (state is defined when the last worker finishes its work)
# in the production line:

def gen_first_state():
    workers_prod_line, items_prod_line, all_items_in_queue = init_production_line()
    cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
                                                                                        items_prod_line)
    all_items_in_queue = sum_dicts(all_items_in_queue, items_arrive_in_process)
    return [workers_prod_line, items_prod_line, all_items_in_queue]

def cal_reward_per_state(state, action=I3):
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

state = gen_first_state()
immidiate_reward, new_state = cal_reward_per_state(state, action=I3)


