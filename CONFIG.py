from collections import Counter
from scipy.stats import poisson
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import random
import math
import time

ITEMS_NAMES = [I1, I2, I3] = ["I1", "I2", "I3"]
WORKERS_NAMES = [W0, W1, W2, W3, W4] = ["w0", "w1", "w2", "w3", "w4"]
TASKS_NAMES = [Q1, Q2, Q3, Q4, Q5] = ["q1", "q2", "q3", "q4", "q5"]
WORK_TYPES = "work_types"
WORK_UNITS = "work_units"
ITEM_NAME = "item_name"
LAST_WORKER = WORKERS_NAMES[-1]

TIME_DELTA = 0.001
N_STATIONS = 4
N_WORKERS = 5
N_CYCLES = 10

# Poisson arrival of items:
LAMB1 = 10 # item 1
LAMB2 = 10 # item 2
LAMB3 = 10 # item 3
#  work for 1 unit of time, for each worker.

WORKERS_POWER_DICT = {
    W0: {Q1: 1, Q2: 3, Q3: 1, Q4: 10, Q5: 1},
    W1: {Q1: 2, Q2: 1, Q3: 1, Q4: 10, Q5: 0.5},
    W2: {Q1: 0.3, Q2: 0.1, Q3: 1, Q4: 8, Q5: 1},
    W3: {Q1: 1, Q2: 3, Q3: 1, Q4: 4, Q5: 1},
    W4: {Q1: 1, Q2: 5, Q3: 1, Q4: 7, Q5: 1}
}

# the work for each item
ITEMS_WORK_DIST_DICT = {
    I1: {WORK_UNITS: [2, 3, 1, 20], WORK_TYPES: [Q1, Q1, Q3, Q2]},
    I2: {WORK_UNITS: [1, 10, 2, 3], WORK_TYPES: [Q5, Q4, Q1, Q2]},
    I3: {WORK_UNITS: [4, 1, 3, 4], WORK_TYPES: [Q2, Q1, Q1, Q2]}
}



# 3 types of items: "I1", "I2", "I3"
# 5 workers: "w0", "w1", "w2", "w3", "w4"



total_lamb = LAMB1 + LAMB2 + LAMB3
p_lamb1 = LAMB1 / total_lamb
p_lamb2 = LAMB2 / total_lamb
p_lamb3 = LAMB3 / total_lamb
# global lamb1
# global lamb2
# global lamb3
