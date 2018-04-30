from CONFIG import *
from system_dynamics import *
from utils import *

class State(object):
    """A customer of ABC Bank with a checking account. Customers have the
    following properties:

    Attributes:
        name: A string representing the customer's name.
        balance: A float tracking the current balance of the customer's account.
    """

    def __init__(self, state):
        workers_prod_line, items_prod_line, all_items_in_queue = state
        """Return a Customer object whose name is *name* and starting
        balance is *balance*."""
        self.workers_prod_line = workers_prod_line
        self.items_prod_line = items_prod_line
        self.all_items_in_queue = all_items_in_queue
        self.available_items = np.unique([i[0] for i in all_items_in_queue.items() if i[1] > 0])
        self.rewards_states = {}
        #self.calc_rewards_for_actions()

    def calc_rewards_for_actions(self):
        for action in self.available_items:
            immidiate_reward, next_state = self.calc_reward_per_state(action=action)
            self.rewards_states[action] = {REWARD: immidiate_reward, NEXT_STEP: next_state}

    def calc_reward_per_state(self, action=I3):
        """
        :param self:
        :param action:
        :return: cycle_time = immidiate reward.
        """
        # add the new item to the production
        items_prod_line = add_item_to_line(self.items_prod_line, ITEMS_WORK_DIST_DICT, chosen_item=action)
        # re-arrange the workers
        workers_prod_line = workers_change_bb(self.workers_prod_line)
        # remove the chosen item for queue
        self.all_items_in_queue[action] -= 1
        # run a cycle. finished when last item finish!
        cycle_time, items_prod_line, workers_prod_line, items_arrive_in_process = run_one_cycle(workers_prod_line,
                                                                                            items_prod_line)
        all_items_in_queue = sum_dicts(self.all_items_in_queue, items_arrive_in_process)
        new_s = [workers_prod_line, items_prod_line, all_items_in_queue]
        return cycle_time, new_s


print "bye"
# # immidiate_reward, new_state = calc_reward_per_state(state, action=I3)

# immidiate_reward, new_state, chosen_action = choose_action_greedy(state)
