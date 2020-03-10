"""
Counterfactual Regret
American Football
"""
import time
import copy
import itertools
from decimal import Decimal


def create_info_set(chance_action, action, payoff):
    initial = [ [[]] ]
    ite_action = [chance_action, action[0], action[1]]
    for ite in range(3):
        sample = []
        for i in initial[-1]:
            for j in ite_action[ite]:
                hoge = copy.copy(i)
                hoge.append(j)
                sample.append(hoge)
        if ite != 2:
            initial.append(sample)
        else:
            for k in sample:
                if payoff[k[0]][k[1]][k[2]] < 10:
                    initial.append(k)
    dummy_sec_initial = copy.copy(initial)
    for sec in dummy_sec_initial[3:]:
        sec_initial = [ [sec] ]
        for ite in range(3):
            sample = []
            for i in sec_initial[-1]:
                for j in ite_action[ite]:
                    hoge = copy.copy(i)
                    hoge.append(j)
                    sample.append(hoge)
            if ite != 2:
                sec_initial.append(sample)
            else:
                for k in sample:
                    if payoff[k[0]][k[1]][k[2]]+payoff[k[3]][k[4]][k[5]] < 10:
                        sec_initial.append(k)
        for i in sec_initial[1:]:
            initial.append(i)
    dummy_third_initial = copy.copy(initial)
    for third in dummy_third_initial:
        if len(third) == 6:
            third_initial = [ [third] ]
            for ite in range(2):
                sample = []
                for i in third_initial[-1]:
                    for j in ite_action[ite]:
                        hoge = copy.copy(i)
                        hoge.append(j)
                        sample.append(hoge)
                if ite != 2:
                    third_initial.append(sample)
                else:
                    for k in sample:
                        third_initial.append(k)
            for i in third_initial[1:]:
                initial.append(i)
    
    return initial


itelater = 200
player = [0, 1] #Offence, Defence
chance_action = [0, 1, 2] #low, middle, high
action = [ [0, 1, 2, 3, 4], #inside, outside, short, middle, long
           [0, 1, 2], ] #4men, 5men, 6men
init_sigma = [ [1/3, 1/3, 1/3],
               [1/5, 1/5, 1/5, 1/5, 1/5],
               [1/3, 1/3, 1/3], ]
init_nu_sigma_list = [ [0, 0, 0],
                       [0, 0, 0, 0, 0],
                       [0, 0, 0], ]
init_sigma_sum = [ [0, 0, 0],
                   [0, 0, 0, 0, 0],
                   [0, 0, 0], ]
init_Regret = [ [0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0], ]

payoff = []
m_payoff = [ [3,  2, 2],
             [3,  4, 3],
             [7,  7, 5],
             [8,  9, 7],
             [7, 12, 5] ]
L_p, H_p = [], []
for p1 in m_payoff:
    l_p, h_p = [], []
    for p2 in p1:
        l_p.append(p2-2)
        h_p.append(p2+3)
    L_p.append(l_p)
    H_p.append(h_p)
payoff.append(L_p)
payoff.append(m_payoff)
payoff.append(H_p)

information_set = create_info_set(chance_action, action, payoff)

node_player = []
for i in information_set:
    if len(i) == 1 or (len(i) == 3 and type(i[0]) == int ) or len(i) == 6:
        node_player.append(3)
    elif len(i) == 3 and type(i[0]) != int:
        node_player.append(0)
    else:
        node_player.append(1)

node_action = []
for i in node_player:
    if i == 0:
        node_action.append(action[i])
    elif i == 1:
        node_action.append(action[i])
    else:
        node_action.append(chance_action)

chance_node = []
for i in information_set:
    if len(i) == 1 or (len(i) == 3 and type(i[0]) == int ) or len(i) == 6:
        chance_node.append(i)

sigma = []
for i in node_player:
    if i == 0:
        sigma.append(init_sigma[i+1])
    elif i == 1:
        sigma.append(init_sigma[i+1])
    else:
        sigma.append(init_sigma[0])

nu_sigma_list, sigma_sum, Regret = [], [], []
for i in node_player:
    if i == 0:
        nu_sigma_list.append(init_nu_sigma_list[i+1])
        sigma_sum.append(init_sigma_sum[i+1])
        Regret.append(init_Regret[i+1])
    elif i == 1:
        nu_sigma_list.append(init_nu_sigma_list[i+1])
        sigma_sum.append(init_sigma_sum[i+1])
        Regret.append(init_Regret[i+1])
    else:
        nu_sigma_list.append(init_nu_sigma_list[0])
        sigma_sum.append(init_sigma_sum[0])
        Regret.append(init_Regret[0])

pi_i_sum = []
for i in node_action:
    pi_i_sum.append(0)


def CFR(h, i, t, pi_i, pi_other):

    for c in information_set:
        if (h in c) or (h == c):
            info_index = information_set.index(c)
    
    if len(h) == 3:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return  1
        else:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return  -1
    elif len(h) == 6:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] >= 10:
                return  1
        else:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] >= 10:
                return  -1
    elif len(h) == 9:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] + payoff[h[6]][h[7]][h[8]] >= 10:
                return  1
            else:
                return 0
        else:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] + payoff[h[6]][h[7]][h[8]] >= 10:
                return  -1
            else:
                return 0
    
    if h in chance_node:
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
        #print ("================")
        for a in node_action[info_index]:
            Regret[info_index][a] += pi_other * ( nu_sigma_list[info_index][a] - nu_sigma )
            #print ( "%f  %f  %f" % ( Regret[info_index][a], pi_other, ( nu_sigma_list[info_index][a] - nu_sigma ) ) )
            #print ("=")
            sigma_sum[info_index][a] += pi_i * sigma[info_index][a]
            #print ( "%f  %f  %f" % (sigma_sum[info_index][a], pi_i, sigma[info_index][a] ) )
            #print ("===")
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

#
# pi_iがおそらく桁落ちしている
#

#Result
for i in range(len(sigma_sum)):
    if node_player[i] == 3:
        continue
    print ("===")
    if node_player[i] == 0:
        for a in action[0]:
            #print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a]/pi_i_sum[i]) )
            print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
    elif node_player[i] == 1:
        for a in action[1]:
            #print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a]/pi_i_sum[i]) )
            print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
print ("")
print ("実行時間: %f" % (finish-start))


