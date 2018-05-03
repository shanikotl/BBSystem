from utils import *
from system_dynamics import *
from stochasic_arrival import *
from select_item import choose_random_item_from_queue


def main():
    workers_prod_line, items_prod_line, all_items_in_queue = init_production_line()
    n_inserted_items = 0
    total_time_of_system = 0
    all_processed_items = constract_finished_items_dict()
    while n_inserted_items < N_CYCLES:
        print "at the beginning of cycle, workers are - %s " % workers_prod_line
        # First scenario: 2 workers can't work together in the same station.
        cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
                                                                                       items_prod_line)

        print "at the end of cycle, workers are - %s " % workers_prod_line
        all_items_in_queue = sum_dicts(all_items_in_queue, items_arrive_in_process)
        print all_items_in_queue
        t1, chosen_item = choose_random_item_from_queue(all_items_in_queue)
        total_time_of_system += t1
        all_items_in_queue[chosen_item] -= 1
        all_processed_items[chosen_item] += 1
        items_prod_line = add_item_to_line(items_prod_line, ITEMS_WORK_DIST_DICT, chosen_item=chosen_item)
        print "items_prod_line", items_prod_line
        workers_prod_line = workers_change_bb(workers_prod_line)
        n_inserted_items += 1
        total_time_of_system += cycle_time
        print "item inserted - %s,  workers order: %s " % (n_inserted_items, workers_prod_line)

    print "-->>> Finished processing %s items, in total time of %s" % (N_CYCLES, total_time_of_system)
    print "-->>> Processes items: %s " % all_processed_items


if __name__ == "__main__":
    main()
