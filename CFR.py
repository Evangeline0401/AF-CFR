"""
Counterfactual Regret
American Football
"""

import copy


itelater = 100000
player = [0, 1]
action = [0, 1]
paypff = [ [1, 1],
           [1, 1] ] #zero sum game
terminal = [ [0, 0], [0, 1],
             [1, 0], [1, 1] ]
information_set = [ [[]],
                    [[0], [1]] ]

sigma = [ [1/2, 1/2],
          [1/2, 1/2] ]
nu_sigma_list = [ [0, 0],
                  [0, 0] ]
sigma_sum = [ [0, 0],
              [0, 0] ]
Regret = [ [0, 0],
           [0, 0] ]
pi_i_sum = [0, 0]


def CFR(h, i, t, pi_i, pi_other):

    if h in terminal:
        if i == 0:
            return paypff[ h[0] ][ h[1] ]
        else:
            return -paypff[ h[0] ][ h[1] ]
    
    for c in information_set:
        if h in c:
            info_index = information_set.index(c)

    nu_sigma = 0
    for a in action:
        nu_sigma_list[info_index][a] = 0
    
    for a in action:
        if info_index == i:
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
    if info_index == i:
        for a in action:
            Regret[info_index][a] += pi_other * ( nu_sigma_list[info_index][a] - nu_sigma )
            sigma_sum[info_index][a] += pi_i * sigma[info_index][a]
        pi_i_sum[info_index] += pi_i

    sum_regret = 0
    for a in action:
        if Regret[info_index][a] > 0:
            sum_regret += Regret[info_index][a]
    for a in action:
        if sum_regret > 0:
            if Regret[info_index][a] > 0:
                sigma[info_index][a] = Regret[info_index][a] / sum_regret
            else:
                sigma[info_index][a] = 0
        else:
            sigma[info_index][a] = 1/len(action)

    return nu_sigma


for t in range(itelater):
    for i in player:
        CFR([], i, t, 1, 1)


for i in range(len(sigma_sum)):
    print ("===")
    for j in action:
        print (sigma_sum[i][j] / pi_i_sum[i])
