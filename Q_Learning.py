from CONFIG import *

R = np.matrix([[-1, -1, -1, -1, 0, -1],
               [-1, -1, -1, 0, -1, 100],
               [-1, -1, -1, 0, -1, -1],
               [-1, 0, 0, -1, 0, -1],
               [-1, 0, 0, -1, -1, 100],
               [-1, 0, -1, -1, 0, 100]])

Q = np.matrix(np.zeros([6, 6]))
GAMMA = 0.8
initial_state = 1


def get_available_actions(state):
    # This function returns all available actions in the state given as an argument
    current_state_row = R[state, ]
    return np.where(current_state_row >= 0)[1]


def sample_next_action(available_act):
    # This function chooses at random which action to be performed within the range
    # of all the available actions.
    return int(np.random.choice(available_act, 1))


def update_Q(current_state, action, gamma=GAMMA):
    # This function updates the Q matrix according to the path selected and the Q
    # learning algorithm
    max_index = np.where(Q[action, ] == np.max(Q[action, ]))[1]
    if max_index.shape[0] > 1:
        max_index = int(np.random.choice(max_index, size=1))
    else:
        max_index = int(max_index)
    max_value = Q[action, max_index]
    # Q learning formula
    Q[current_state, action] = R[current_state, action] + gamma * max_value
    return R[current_state, action]

# -------------------------------------------------------------------------------
# Training

def train_system():
    for i in range(10000):
        current_state = np.random.randint(0, int(Q.shape[0]))
        available_act = get_available_actions(current_state)
        action = sample_next_action(available_act)
        r = update_Q(current_state, action, GAMMA)
    # Normalize the "trained" Q matrix
    print("Trained Q matrix:")
    print(Q / np.max(Q) * 100)


def run_test():
    train_system()
    current_state = 2
    steps = [current_state]
    MAX_ITER = 10
    iter = 0
    while (current_state != 5) or (iter < MAX_ITER):
        next_step_index = np.argmax(Q[current_state, ])
        steps.append(next_step_index)
        current_state = next_step_index
        iter += 1
    print steps

run_test()