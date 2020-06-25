import numpy as np

player = [0, 1]
action = [[0, 1, 2, 3, 4],
          [0, 1, 2]]


def CFR(history, i, t, pi_i, pi_other, I_map):
    if check_terminal(history):
        return 0 #return utility
    elif check_chance(history):
        expected_value = 0
        possibilities = ["L", "H"]
        p_prob = [1/2, 1/2]
        for ite, act in enumerate(possibilities):
            expected_value += p_prob[ite]*CFR(history+act, i, t,
                                              pi_i, p_prob[ite]*pi_other, I_map)
        return expected_value
    
    info_set, info_set_player = get_info_set(I_map, history)

    info_set.next_strategy(info_set_player)
    strategy = info_set.strategy

    action_utils = np.zeros(len(action[info_set_player]))
    for ite, act in enumerate(action[info_set_player]):
        next_history = history + str(act)
        if info_set_player == i:
            action_utils[ite] = CFR(next_history, i, t,
                                    strategy[ite]*pi_i, pi_other, I_map)
        else:
            action_utils[ite] = CFR(next_history, i, t,
                                    pi_i, strategy[ite]*pi_other, I_map)
    util = sum(action_utils * strategy)

    if info_set_player == i:
        for ite, act in enumerate(action[info_set_player]):
            info_set.regret_sum[ite] += pi_other * ( action_utils[ite] - util )
    
    return util


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
        return info_set, info_set_player

    return I_map[key], info_set_player


class InformationSet():
    def __init__(self, key, info_set_player):
        self.key = key
        self.regret_sum = np.zeros(len(action[info_set_player]))
        self.strategy_sum = np.zeros(len(action[info_set_player]))
        self.strategy = np.repeat(1/len(action[info_set_player]), len(action[info_set_player]))
        self.reach_pr = 0#最終的な出力を表示するのに使う？
        self.reach_pr_sum = 0
    
    def next_strategy(self, info_set_player):
        self.strategy_sum += self.reach_pr * self.strategy
        self.strategy = self.calc_strategy(info_set_player)
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0
    
    def calc_strategy(self, info_set_player):
        strategy = self.make_positive(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy = strategy / total
        else:
            n = len(action[info_set_player])
            strategy = np.repeat(1/n, n)

        return strategy
    
    def make_positive(self, x):
        return np.where(x > 0, x, 0)


I_map = {}
itelator = 100
for t in range(itelator):
    for i in player:
        CFR("", i, t, 1, 1, I_map)

