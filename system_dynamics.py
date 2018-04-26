from CONFIG import *
from stochasic_arrival import p_event, get_random_item_type

# update the order of items in the production line:
# this is done at the end of each cycle:
def add_item_to_line(items_prod_line, items_dict, chosen_item=I3):
    # update the keys - 0 -> 1
    for idx in range(N_WORKERS)[1:][::-1]:
        items_prod_line[idx] = items_prod_line[idx - 1]
    # add the first item to the production line.. (currently - always I3. :
    items_prod_line[0] = {ITEM_NAME: chosen_item, WORK_UNITS: items_dict[chosen_item][WORK_UNITS][:],
                          WORK_TYPES: items_dict[chosen_item][WORK_TYPES][:]}
    #     print "after: %s "
    #     for k in items_prod_line.items():
    #         print k[0], k[1]['name']
    return items_prod_line


def workers_change_bb(workers_prod_line):
    """
    input: workers_prod_line - array of arrays. each array is a station, with names of workers in the station
    output: workers_prod_line  - after
    """
    # TODO - fix this wierd function!
    station_idx = 0
    idx = 1
    for station in workers_prod_line[1:]:
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
    workers_order = dict(zip(WORKERS_NAMES, range(len(WORKERS_NAMES))))
    return workers_prod_line, items_prod_line, workers_order


def run_one_cycle(workers_prod_line, items_prod_line, workers_order):
    last_worker_working = True
    total_time = 0
    time_from_prev_event = 0
    items_in_queue = {I1: 0, I2: 0, I3: 0}
    while last_worker_working:
        delta_time = TIME_DELTA
        # time.sleep(delta_time)
        total_time += delta_time
        time_from_prev_event += delta_time
        # generate an event, by probability.
        alpha = random.random()
        if alpha <= p_event(time_from_prev_event):
            items_in_queue[get_random_item_type()] += 1
            time_from_prev_event = 0
        # print "time from begining of cycle: %s and workers in line: %s " % (total_time, workers_prod_line)
        for station_idx, station in enumerate(workers_prod_line):
            if len(station) > 0:
                active_worker = station[-1]
                item_number = workers_order[active_worker]
                task = items_prod_line[item_number][WORK_TYPES][station_idx]
                delta_work = WORKERS_POWER_DICT[active_worker][task] * delta_time
                items_prod_line[item_number][WORK_UNITS][station_idx] -= delta_work
                # print items_prod_line[item_number]
                # print delta_work, task, workers_dict[active_worker][task], active_worker
                curr_work_units = items_prod_line[item_number][WORK_UNITS][station_idx]
                #                 if active_worker=="w4":
                #                     print "work left for the last worker: %s,
                # of type %s" % (items_prod_line[item_number]['work_units'][station_idx], task)
                if curr_work_units <= 0:
                    # print "%s worker finisehd item %s, task %s" % (active_worker, item_number, task)
                    # print workers_prod_line
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
    print "items arrivied into queue during cycle: %s" % items_in_queue
    return total_time, items_prod_line, workers_prod_line, items_in_queue
