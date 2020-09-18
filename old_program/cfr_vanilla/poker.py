import numpy as np

player   = [0, 1]
action   = [0, 1]
EU = [0, 0]

def main():
    I_map = {}
    itelator = 10000
    for t in range(itelator):
        for i in player:
            EU[i] += CFR("", i, t, 1, 1, I_map)
        for key, v in I_map.items():
            v.next_strategy(key)
    for i in EU:
        print (i/itelator)

    for key, v in I_map.items():
        strategy = v.strategy_sum / v.reach_pr_sum
        strategy = np.where(strategy < 0.001, 0, strategy)
        total = sum(strategy)
        strategy /= total
        print ("  "+key)
        print (strategy)


def CFR(history, i, t, pi_i, pi_other, I_map):
    if check_terminal(history):
        return terminal_util(I_map, history, i)
    elif check_chance(history):
        expected_value = 0
        possibilities = ["J", "Q", "K"]
        for _, act in enumerate(possibilities):
            for _, Act in enumerate(possibilities):
                if act != Act:
                    expected_value += (1/6) * CFR(history+act+Act, i, t,
                                                  pi_i, (1/6)*pi_other, I_map)
        return expected_value
    
    info_set, info_set_player = get_info_set(I_map, history)
    if i == info_set_player:
        info_set.reach_pr += pi_i

    strategy = info_set.strategy

    action_utils = np.zeros(len(action))
    for ite, act in enumerate(action):
        next_history = history + str(act)
        if info_set_player == i:
            action_utils[ite] = CFR(next_history, i, t,
                                    strategy[ite]*pi_i, pi_other, I_map)
        else:
            action_utils[ite] = CFR(next_history, i, t,
                                    pi_i, strategy[ite]*pi_other, I_map)
    util = sum(action_utils * strategy)

    if info_set_player == i:
        for ite, act in enumerate(action):
            info_set.regret_sum[ite] += pi_other * ( action_utils[ite] - util )
            info_set.strategy_sum[ite] += pi_i * strategy[ite]
    
    return util


def check_terminal(history):
    hogehoge = "CC" + history[2:]
    possibilities = {"CC00": True, "CC010": True,
                     "CC011": True, "CC10": True, "CC11": True}
    return hogehoge in possibilities


def terminal_util(I_map, history, i):
    if history[0] == "J":
        card1 = 0
        card2 = 1 if history[1] == "Q" else 2
    elif history[0] == "Q":
        card1 = 1
        card2 = 0 if history[1] == "J" else 2
    else:
        card1 = 2
        card2 = 0 if history[1] == "J" else 1

    HISTORY = "CC"+history[2:]
    if HISTORY == "CC010":
        return -1 if i == 0 else 1
    elif HISTORY == "CC10":
        return 1 if i == 0 else -1
    elif HISTORY== "CC00":
        if i == 0:
            return 1 if card1 > card2 else -1
        else:
            return 1 if card2 > card1 else -1
    assert(HISTORY == "CC011" or HISTORY == "CC11")
    if i == 0:
        return 2 if card1 > card2 else -2
    else:
        return 2 if card2 > card1 else -2


def check_chance(history):
    return history == ""


def get_info_set(I_map, history):
    n = len(history)
    info_set_player = 0 if n % 2 == 0 else 1
    if n == 2:
        key = history[0]+" CC" if info_set_player == 0 else history[1]+" CC"
    else:
        key = history[0]+" CC"+history[2:] if info_set_player == 0 else history[1]+" CC"+history[2:]
    info_set = None

    if key not in I_map:
        info_set = InformationSet(key, info_set_player)
        I_map[key] = info_set
        return info_set, info_set_player

    return I_map[key], info_set_player


class InformationSet():
    def __init__(self, key, info_set_player):
        self.key = key
        self.regret_sum = np.zeros(len(action))
        self.strategy_sum = np.zeros(len(action))
        self.strategy = np.repeat(1/len(action), len(action))
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
            n = len(action)
            strategy = np.repeat(1/n, n)

        return strategy
    
    def make_positive(self, x):
        return np.where(x > 0, x, 0)


if __name__ == "__main__":
    main()
