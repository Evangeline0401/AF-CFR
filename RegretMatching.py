import numpy as np
import itertools
import copy


ite_num = 100000
player = [0, 1]
action = [0, 1]
action_profile = [0, 0]
utility = [ [ [5, -5], [1, -1] ],
            [ [0, 0], [7, -7] ] ]

regret = [[0, 0],
          [0, 0]]
strategy = [[0.5, 0.5],
            [0.5, 0.5]]
cum_strategy = [[0, 0],
                [0, 0]]


def update_strategy(p):

        check_strategy = copy.copy(regret[p])
        for a in action:
                if check_strategy[a] < 0:
                        check_strategy[a] = 0
        if sum(check_strategy) <= 0:
                for a in action:
                        strategy[p][a] = 1 / len(check_strategy)
        else:
                for a in action:
                        strategy[p][a] = check_strategy[a] / sum(check_strategy)


def get_regret(p, profile):

        now_util = utility[profile[0]][profile[1]][p]
        for a in action:
                if p == 0:
                        reg_util = utility[a][profile[1]][p]
                        regret[p][a] += reg_util - now_util
                else:
                        reg_util = utility[profile[0]][a][p]
                        regret[p][a] += reg_util - now_util


def get_action_profile():

        profile = [ np.random.choice(action, 1, p=strategy[num]) for num in player ]
        return profile


for ite in range(ite_num):
        for p in player:
                shimano = get_action_profile()
                for a in action:
                        action_profile[a] = shimano[a][0]
                        cum_strategy[p][a] += strategy[p][a]
                get_regret(p, action_profile)
                update_strategy(p)

for p, a in itertools.product(player, action):
        print ( cum_strategy[p][a]/ite_num )