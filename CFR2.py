"""
Counterfactual Regret
Kuhn Poker
"""
import time
import copy


itelater = 100000
player = [0, 1] #Player1, Player2
action = [0, 1, 2, 3] #check, bet, fold, call
chance_action = [0, 1, 2, 3, 4, 5] #JQ, JK, QJ, QK, KJ, KQ
paypff = [-1, -1, -2, 1, -2,
          -1, -1, -2, 1, -2,
           1, -1,  2, 1,  2,
          -1, -1, -2, 1, -2,
           1, -1,  2, 1,  2,
           1, -1,  2, 1,  2, ] #zero sum
terminal = [ [0, 0, 0], [0, 0, 1, 2], [0, 0, 1, 3], [0, 1, 2], [0, 1, 3],
             [1, 0, 0], [1, 0, 1, 2], [1, 0, 1, 3], [1, 1, 2], [1, 1, 3],
             [2, 0, 0], [2, 0, 1, 2], [2, 0, 1, 3], [2, 1, 2], [2, 1, 3],
             [3, 0, 0], [3, 0, 1, 2], [3, 0, 1, 3], [3, 1, 2], [3, 1, 3],
             [4, 0, 0], [4, 0, 1, 2], [4, 0, 1, 3], [4, 1, 2], [4, 1, 3],
             [5, 0, 0], [5, 0, 1, 2], [5, 0, 1, 3], [5, 1, 2], [5, 1, 3], ]
information_set = [ [[]],
                    [[0], [1]], [[2], [3]], [[4], [5]],
                    [[0, 0], [5, 0]], [[0, 1], [5, 1]], [[1, 0], [3, 0]], [[1, 1], [3, 1]], [[2, 0], [4, 0]], [[2, 1], [4, 1]],
                    [[0, 0, 1], [1, 0, 1]], [[2, 0, 1], [3, 0, 1]], [[4, 0, 1], [5, 0, 1]] ]
node_player = [ 3,
                0, 0, 0,
                1, 1, 1, 1, 1, 1,
                0, 0, 0, ]
node_action = [ [0, 1, 2, 3, 4, 5],
                [0, 1], [0, 1], [0, 1],
                [0, 1], [2, 3], [0, 1], [2, 3], [0, 1], [2, 3],
                [2, 3], [2, 3], [2, 3], ]
chance_node = [ [] ]

sigma = [ [1/6, 1/6, 1/6, 1/6, 1/6, 1/6],
          [1/2, 1/2, 0, 0], [1/2, 1/2, 0, 0], [1/2, 1/2, 0, 0],
          [1/2, 1/2, 0, 0], [0, 0, 1/2, 1/2], [1/2, 1/2, 0, 0], [0, 0, 1/2, 1/2], [1/2, 1/2, 0, 0], [0, 0, 1/2, 1/2],
          [0, 0, 1/2, 1/2], [0, 0, 1/2, 1/2], [0, 0, 1/2, 1/2], ]
nu_sigma_list = [ [0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                  [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
                  [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
sigma_sum = [ [0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
              [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0],
              [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
Regret = [ [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],
           [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0],[0, 0, 0, 0],
           [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ]
pi_i_sum = [ 0,
             0, 0, 0,
             0, 0, 0, 0, 0, 0,
             0, 0, 0, ]


def CFR(h, i, t, pi_i, pi_other):

    for c in information_set:
        if h in c:
            info_index = information_set.index(c)

    if h in terminal:
        if i == 0:
            return  paypff[ terminal.index(h) ]
        else:
            return -paypff[ terminal.index(h) ]
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
            #print ("%s : %d : %d : %f : %f" % (h, i, t, sigma[info_index][a]*pi_i, pi_other))
            nu_sigma_list[info_index][a] = CFR(dummy, i, t, sigma[info_index][a]*pi_i, pi_other)
        else:
            dummy = copy.copy(h)
            dummy.append(a)
            #print ("%s : %d : %d : %f : %f" % (h, i, t, pi_i, sigma[info_index][a]*pi_other))
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

for i in range(len(sigma_sum)):
    if i == 0:
        continue
    print ("===")
    for j in action:
        if sigma_sum[i][j] == 0:
            print ("N/A")
        else:
            print ( "Info_set: %d   Action: %d  Prob: %f" % (i, j, sigma_sum[i][j] / pi_i_sum[i]) )

print ("")
print ("実行時間: %f" % (finish-start))
