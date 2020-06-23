import numpy as np

player = [0, 1]
action = [[0, 1, 2, 3, 4],
          [0, 1, 2]]


def CFR(history, i, t, pi_i, pi_other, I_map):

    if check_terminal(history):
        return 0 #return utility
    elif check_chance(history):
        return 1
    
    info_set = get_info_set(I_map, history)

    strategy = info_set.strategy


def check_terminal(history):

    return len(history) == 3


def check_chance(history):

    return len(history) == 2

def get_info_set(I_map, history):

    key = len(history)
    if key == 0:
        info_set_player = 0
    elif key == 1:
        info_set_player = 1
    info_set = None

    if key not in I_map:
        info_set = InformationSet(key, info_set_player)
        I_map[key] = info_set
        return info_set

    return I_map[key]


class InformationSet():
    def __init__(self, key, info_set_player):
        self.key = key
        self.regret_sum = np.zeros(len(action[info_set_player]))
        self.strategy_sum = np.zeros(len(action[info_set_player]))
        self.strategy = np.repeat(1/len(action[info_set_player]), len(action[info_set_player]))
        self.reach_pr = 0
        self.reach_pr_sum = 0


I_map = {}
ite = 100
for t in range(ite):
    for i in player:
        CFR("", i, t, 1, 1, I_map)

