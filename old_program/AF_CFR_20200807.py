import time
import sys
import numpy as np
from tqdm import tqdm

player   = [0, 1]
action   = [[0, 1, 2, 3, 4],
            [0, 1, 2]]
get_yard = [ [ [1, 3, 6],  [0, 2, 5],    [0, 2, 5]  ],
             [ [1, 3, 6],  [2, 4, 7],    [1, 3, 6]  ],
             [ [5, 7, 10], [5, 7, 10],   [3, 5, 8]  ],
             [ [6, 8, 11], [7, 9, 12],   [5, 7, 10] ],
             [ [5, 7, 10], [10, 12, 15], [3, 5, 8]  ] ]
possibilities = ["0", "1", "2"]
p_prob = [1/5, 3/5, 1/5]
fresh_yard = 10

def main():
    I_map = {}
    itelator = 10000

    start = time.time()
    for t in tqdm(range(itelator)):
        for i in player:
            CFR("", i, t, 1, 1, I_map)
        for key, v in I_map.items():
            v.next_strategy(key)
        sys.stdout.write("\r{}/{}\r".format(t+1, itelator))
    finish = time.time()
    
    for key, v in I_map.items():
        strategy = v.strategy_sum / v.reach_pr_sum
        strategy = np.where(strategy < 0.001, 0, strategy)
        total = sum(strategy)
        strategy /= total
        print (key+": ", strategy)

    
    print ("")
    print ("実行時間: %f" % (finish-start))


def CFR(history, i, t, pi_i, pi_other, I_map):
    if check_terminal(history):
        check = terminal_util(I_map, history, i)
        if check != "Continue":
            return check
    if check_chance(history):
        expected_value = 0
        #possibilities = ["0", "1"]
        #p_prob = [1/2, 1/2]
        for ite, act in enumerate(possibilities):
            expected_value += p_prob[ite]*CFR(history+act, i, t,
                                              pi_i, p_prob[ite]*pi_other, I_map)
        return expected_value
    
    info_set, info_set_player = get_info_set(I_map, history)
    if i == info_set_player:
        info_set.reach_pr += pi_i

    #info_set.next_strategy(info_set_player)
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
            info_set.strategy_sum[ite] += pi_i * strategy[ite]
    
    return util


def check_terminal(history):
    return len(history) == 3 or len(history) == 6 or len(history) == 9


def terminal_util(I_map, history, i):
    if len(history) == 3:
        yard = get_yard[int(history[0])][int(history[1])][int(history[2])]
        if yard >= fresh_yard:
            if i == 1:
                return 1
            else:
                return -1
        else:
            if i == 1:
                return "Continue"
            else:
                return "Continue"
    elif len(history) == 6:
        yard = ( get_yard[int(history[0])][int(history[1])][int(history[2])]+
                 get_yard[int(history[3])][int(history[4])][int(history[5])] )
        if yard >= fresh_yard:
            if i == 1:
                return 1
            else:
                return -1
        else:
            if i == 1:
                return "Continue"
            else:
                return "Continue"
    elif len(history) == 9:
        yard = ( get_yard[int(history[0])][int(history[1])][int(history[2])]+
                 get_yard[int(history[3])][int(history[4])][int(history[5])]+
                 get_yard[int(history[6])][int(history[7])][int(history[8])] )
        if yard >= fresh_yard:
            if i == 1:
                return 1
            else:
                return -1
        else:
            if i == 1:
                return -1
            else:
                return 1


def check_chance(history):
    return len(history) == 2 or len(history) == 5 or len(history) == 8


def get_info_set(I_map, history):
    n = len(history)
    if n == 0:
        key = "1st Off         "
        info_set_player = 0
    elif n == 1:
        key = "1st Def         "
        info_set_player = 1
    elif n == 3:
        key = "2nd Off = " + history + "   "
        info_set_player = 0
    elif n == 4:
        key = "2nd Def = " + history[:-1] + "   "
        info_set_player = 1
    elif n == 6:
        key = "3rd Off = " + history
        info_set_player = 0
    elif n == 7:
        key = "3rd Def = " + history[:-1]
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
        self.reach_pr = 0
        self.reach_pr_sum = 0
    
    def next_strategy(self, key):
        #self.strategy_sum += self.reach_pr * self.strategy
        self.strategy = self.calc_strategy(key)
        self.reach_pr_sum += self.reach_pr
        self.reach_pr = 0
    
    def calc_strategy(self, key):
        strategy = self.make_positive(self.regret_sum)
        total = sum(strategy)
        if total > 0:
            strategy = strategy / total
        else:
            if "Off" in key:
                n = len(action[0])
                strategy = np.repeat(1/n, n)
            else:
                n = len(action[1])
                strategy = np.repeat(1/n, n)

        return strategy
    
    def make_positive(self, x):
        return np.where(x > 0, x, 0)


if __name__ == "__main__":
    main()
