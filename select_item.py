from stochasic_arrival import time_to_event, get_random_item_type
from CONFIG import *


def choose_item_to_insert(all_items_in_queue):
    avail_items = [i[0] for i in all_items_in_queue.items() if i[1] > 0]
    if len(avail_items) != 0:
        return 0, avail_items[0]  # currently - a random item
    else:
        # time.sleep(time_to_event(total_lamb))
        print "sleeping "
        return time_to_event(total_lamb), get_random_item_type()

#
# def calc_total_process_time(item_name):
#     item_dist = ITEMS_WORK_DIST_DICT[item_name]
#
#     delta_work = WORKERS_POWER_DICT[W0][
#              ] * delta_time
# items_prod_line[item_number][WORK_UNITS][station_idx] -= delta_work
