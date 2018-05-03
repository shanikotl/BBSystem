from stochasic_arrival import time_to_event, get_random_item_type
# from mdp import calc_reward_per_state
from CONFIG import *


def choose_random_item_from_queue(all_items_in_queue):
    """
    :param all_items_in_queue: dictionary of items waiting in queue
    :return: - time it took to get item : 0 if the item was waiting in the queue , or exponential dist. time otherwise
             - item name to add to system
    """
    avail_items = [i[0] for i in all_items_in_queue.items() if i[1] > 0]
    if len(avail_items) != 0:
        return 0, avail_items[0]  # currently - a random item
    else:
        # time.sleep(time_to_event(total_lamb))
        print "sleeping "
        return time_to_event(total_lamb), get_random_item_type()

