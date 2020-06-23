"""
Counterfactual Regret
American Football  by SHIMANO
"""
import time
import copy
import itertools
from decimal import Decimal
#import v2_cfr_axu
import hogehoge_axu


# Init Information
itelater = 10
player = (0, 1) #Offence, Defence (and Number 2 is Chance Node)
action = ( (0, 1, 2, 3, 4), #InRun, OutRun, ShortPass, MiddlePass, LongPass
           (0, 1, 2) )#4men, 5men, 6men
chance_action = (0, 1)
#pass_sigma = [Decimal(str(3))/Decimal(str(4)), Decimal(str(1))/Decimal(str(4))]

payoff, information_set, infoset_player, infoset_action, infoset_chance, sigma, nu_sigma_list, sigma_sum, Regret, pi_i_sum = hogehoge_axu.create_master_data(action, chance_action)


def CFR(h, i, t, pi_i, pi_other, init_utility):
    
    for c in information_set:
        if (h in c) or (h == c):
            info_index = information_set.index(c)
    
    if h in infoset_chance:
        eu = Decimal(str(0))
        for a in chance_action:
            dummy_eu = copy.copy(h)
            dummy_eu.append(a)
            #if h[0] != 0 and h[0] != 1:
                #eu += pass_sigma[a] * CFR( dummy_eu, i, t, pi_i, pass_sigma[a]*pi_other, init_utility )
            #else:
            eu += sigma[info_index][a] * CFR( dummy_eu, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
        return eu

    if len(h) == 3:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return Decimal(str(1))
        else:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return Decimal(str(-1))
    if len(h) == 6:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] >= 10:
                return Decimal(str(1))
            else:
                return Decimal(str(-1))
        else:
            if payoff[h[0]][h[1]][h[2]] + payoff[h[3]][h[4]][h[5]] >= 10:
                return Decimal(str(-1))
            else:
                return Decimal(str(1))

    nu_sigma = Decimal(str(0))
    for a in infoset_action[info_index]:
        nu_sigma_list[info_index][a] = Decimal(str(0))
    
    for a in infoset_action[info_index]:
        if infoset_player[info_index] == i:
            Dummy_i = copy.copy(h)
            Dummy_i.append(a)
            nu_sigma_list[info_index][a] = CFR( Dummy_i, i, t, sigma[info_index][a]*pi_i, pi_other, init_utility )
        else:
            Dummy_Not_i = copy.copy(h)
            Dummy_Not_i.append(a)
            nu_sigma_list[info_index][a] = CFR( Dummy_Not_i, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
        nu_sigma += sigma[info_index][a] * nu_sigma_list[info_index][a]
    
    if infoset_player[info_index] == i:
        for a in infoset_action[info_index]:
            Regret[info_index][a] += pi_other * ( nu_sigma_list[info_index][a] - nu_sigma )
            sigma_sum[info_index][a] += pi_i * sigma[info_index][a]
        pi_i_sum[info_index] += pi_i
    
    sum_regret = Decimal(str(0))
    for a in infoset_action[info_index]:
        if Regret[info_index][a] > 0:
            sum_regret += Regret[info_index][a]
    for a in infoset_action[info_index]:
        if sum_regret > 0:
            if Regret[info_index][a] > 0:
                sigma[info_index][a] = Regret[info_index][a] / sum_regret
            else:
                sigma[info_index][a] = Decimal(str(0))
        else:
            sigma[info_index][a] = Decimal(str(1)) / Decimal(str(len(infoset_action[info_index])))
    
    return nu_sigma


start = time.time()
for t in range(itelater):
    for i in player:
        CFR( [], i, t, Decimal(str(1)), Decimal(str(1)), Decimal(str(0)) )
finish = time.time()


#Result
for i in range(len(information_set)):
    if infoset_player[i] == 2:
        continue
    print ("===")
    if infoset_player[i] == 0:
        print (information_set[i])
        for a in action[0]:
            if pi_i_sum[i] > 0:
                print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a]/pi_i_sum[i]) )
            else:
                print ( "Info_set: %d   Action: %d  Prob: N/A" % (i, a) )
                #print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
    elif infoset_player[i] == 1:
        print (information_set[i])
        for a in action[1]:
            if pi_i_sum[i] > 0:
                print ( "Info_set: %d   Action: %d  Prob: %f" % (i, a, sigma_sum[i][a]/pi_i_sum[i]) )
            else:
                print ( "Info_set: %d   Action: %d  Prob: N/A" % (i, a) )
                #print ( "Info_set: %d   sigma_sum: %f  pi_i_sum: %f" % (i, sigma_sum[i][a], pi_i_sum[i]) )
        print ("")
print ("")
print ("実行時間: %f" % (finish-start))