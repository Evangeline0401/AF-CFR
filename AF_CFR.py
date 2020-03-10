"""
Counterfactual Regret
American Football
"""
import time
import copy
import itertools


itelater = 100000
player = [0, 1] #Offence, Defence
chance_action = [0, 1, 2] #low, middle, high
action = [ [0, 1, 2, 3, 4, 5, 6], #inside, outside, short, middle, long, PassfakeRun, RunfakePass
           [0, 1, 2], ] #4men, 5men, 6men

payoff = []
m_payoff = [3, 2, 2, 3, 4, 3, 7, 7, 5, 8, 9, 7, 7, 12, 5, 4, -1, 4, 7, 6, 0]
for p in m_payoff:
    payoff.append(p-2)
payoff += m_payoff
for p in m_payoff:
    payoff.append(p+3)

terminal = []
for c, o, d in itertools.product(chance_action, action[0], action[1]):
    terminal.append([c, o, d])

information_set = [ [[]],
                    [[0], [1], [2]],
                    [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6],
                     [1, 0], [1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [1, 6],
                     [2, 0], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [2, 6]] ]
node_player = [ 3,
                0,
                1, ]
node_action = [ [0, 1, 2],
                [0, 1, 2, 3, 4, 5, 6],
                [0, 1, 2], ]
chance_node = [ [] ]

sigma = [ [1/3, 1/3, 1/3],
          [1/7, 1/7, 1/7, 1/7, 1/7, 1/7, 1/7],
          [1/3, 1/3, 1/3], ]
nu_sigma_list = [ [0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0], ]
sigma_sum = [ [0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0], ]
Regret = [ [0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0], ]
pi_i_sum = [ 0,
             0,
             0, ]


def CFR(h, i, t, pi_i, pi_other):

    print (pi_i)

    for c in information_set:
        if h in c:
            info_index = information_set.index(c)

    if h in terminal:
        if i == 0:
            if payoff[ terminal.index(h) ] >= 3:
                return  1
            else:
                return 0
        else:
            if payoff[ terminal.index(h) ] >= 3:
                return  -1
            else:
                return 0

    elif h in chance_node:
        chance_node_eu = 0
        for a in chance_action:
            dummy = copy.copy(h)
            dummy.append(a)
            chance_node_eu += sigma[info_index][a] * CFR(dummy, i, t, pi_i, sigma[info_index][a]*pi_other)
        return chance_node_eu

    nu_sigma = 0
    for a in node_action[info_index]:
        nu_sigma_list[info_index][a] = 0

    for a in node_action[info_index]:
        if node_player[info_index] == i:
            dummy = copy.copy(h)
            dummy.append(a)
            nu_sigma_list[info_index][a] = CFR(dummy, i, t, sigma[info_index][a]*pi_i, pi_other)
        else:
            dummy = copy.copy(h)
            dummy.append(a)
            nu_sigma_list[info_index][a] = CFR(dummy, i, t, pi_i, sigma[info_index][a]*pi_other)
        nu_sigma += sigma[info_index][a] * nu_sigma_list[info_index][a]
    if node_player[info_index] == i:
        for a in node_action[info_index]:
            Regret[info_index][a] += pi_other * ( nu_sigma_list[info_index][a] - nu_sigma )
            sigma_sum[info_index][a] += pi_i * sigma[info_index][a]
        pi_i_sum[info_index] += pi_i

    sum_regret = 0
    for a in node_action[info_index]:
        if Regret[info_index][a] > 0:
            sum_regret += Regret[info_index][a]
    for a in node_action[info_index]:
        if sum_regret > 0:
            if Regret[info_index][a] > 0:
                sigma[info_index][a] = Regret[info_index][a] / sum_regret
            else:
                sigma[info_index][a] = 0
        else:
            sigma[info_index][a] = 1/len(node_action[info_index])

    return nu_sigma


start = time.time()
for t in range(itelater):
    for i in player:
        CFR([], i, t, 1, 1)
finish = time.time()



#Result
for i in range(len(sigma_sum)):
    if i == 0:
        continue
    print ("===")
    if i == 1:
        for a in action[i-1]:
            print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a] / pi_i_sum[i]) )
            #print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
    elif i == 2:
        for a in action[i-1]:
            print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a] / pi_i_sum[i]) )
            #print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
print ("")
print ("実行時間: %f" % (finish-start))
