from CONFIG import *
from stochasic_arrival import p_event, get_random_item_type
from utils import constract_finished_items_dict, get_round

# update the order of items in the production line:
# this is done at the end of each cycle:
def add_item_to_line(items_prod_line, items_dict, chosen_item=I3):
    """
    :param items_prod_line: dictionary, of items in the production line, with current left tasks.
    key = 1 -> worker number 1.
    :param items_dict: the items work distribution
    :param chosen_item: what item to add to production line
    :return: update items_prod_line by changing location of the items in line + adding the new item data.
    """
    for idx in range(N_WORKERS)[1:][::-1]:
        items_prod_line[idx] = items_prod_line[idx - 1]
    # add the first item to the production line.. (currently - always I3. :
    items_prod_line[0] = {ITEM_NAME: chosen_item, WORK_UNITS: items_dict[chosen_item][WORK_UNITS][:],
                          WORK_TYPES: items_dict[chosen_item][WORK_TYPES][:]}
    for i in items_prod_line.keys():
        items_prod_line[i][WORK_UNITS] = np.ceil(items_prod_line[i][WORK_UNITS])
        #get_round(items_prod_line[i][WORK_UNITS])

    return items_prod_line


def workers_change_bb(workers_prod_line):
    """
    input: workers_prod_line - array of arrays. each array is a station, with names of workers in the station
    output: workers_prod_line  - following the BB scheme.
    """
    idx = 1
    while idx < len(workers_prod_line):
        station = workers_prod_line[idx]
        if len(station) > 0:
            find_empty_station = True
            i = idx
            while find_empty_station:
                prev_station = workers_prod_line[i - 1]
                if (i - 1 == 0) or (len(prev_station) != 0):
                    # if worker 0 reached the begining of line
                    # or worker x found an unempty station
                    worker_to_move = station.pop(0)
                    prev_station.insert(len(prev_station), worker_to_move)
                    find_empty_station = False
                    break
                else:
                    i -= 1
        idx += 1
    return workers_prod_line


def init_production_line():
    # the last worker in each array is the one that is working. the others are blocked, waiting for her to continue.
    workers_prod_line = [[W0], [W1, W2], [W3], [W4]]

    # worker1 works on the first item. worker2 works on the second item. workers can't change location.
    items_prod_line = {
        0: {ITEM_NAME: I1, WORK_UNITS: [1, 3, 1, 20], WORK_TYPES: [Q1, Q1, Q3, Q2]},
        1: {ITEM_NAME: I3, WORK_UNITS: [0, 1, 3, 4], WORK_TYPES: [Q2, Q1, Q1, Q2]},
        2: {ITEM_NAME: I3, WORK_UNITS: [0, 1, 3, 4], WORK_TYPES: [Q2, Q1, Q1, Q2]},
        3: {ITEM_NAME: I2, WORK_UNITS: [0, 0, 2, 3], WORK_TYPES: [Q5, Q4, Q1, Q2]},
        4: {ITEM_NAME: I1, WORK_UNITS: [0, 0, 0, 20], WORK_TYPES: [Q1, Q1, Q3, Q2]}
    }
    items_in_queue = {I1: 1, I2: 0, I3: 1}
    return workers_prod_line, items_prod_line, items_in_queue


def run_one_cycle(workers_prod_line, items_prod_line, workers_order=WORKERS_ORDER):
    last_worker_working = True
    total_time = 0
    time_from_prev_event = 0
    items_arrive_in_process = constract_finished_items_dict()
    while last_worker_working:
        # time.sleep(delta_time)
        total_time += TIME_DELTA
        time_from_prev_event += TIME_DELTA
        # generate an event, by probability.
        alpha = random.random()
        if alpha <= p_event(time_from_prev_event):
            items_arrive_in_process[get_random_item_type()] += 1
            time_from_prev_event = 0
        # print "time from beginning of cycle: %s and workers in line: %s " % (total_time, workers_prod_line)
        for station_idx, station in enumerate(workers_prod_line):
            if len(station) > 0:
                active_worker = station[-1]
                item_number = workers_order[active_worker]
                task = items_prod_line[item_number][WORK_TYPES][station_idx]
                delta_work = WORKERS_POWER_DICT[active_worker][task] * TIME_DELTA
                items_prod_line[item_number][WORK_UNITS][station_idx] -= delta_work
                curr_work_units = items_prod_line[item_number][WORK_UNITS][station_idx]
                if curr_work_units <= 0:
                    if (active_worker == LAST_WORKER) & (station_idx == N_STATIONS - 1):
                        last_worker_working = False
                        print "Last worker finished"
                        break
                    else:
                        w = station.pop()  # removes the last worker in the station.
                        workers_prod_line[station_idx + 1].insert(0, w)
                        # worker is moving together with item she is working on.
    #                     print workers_prod_line
    print "total_time of cycle - %s " % total_time
    #print "items arrivied into queue during cycle: %s" % items_arrive_in_process
    return total_time, items_prod_line, workers_prod_line, items_arrive_in_process
