"""
Counterfactual Regret
American Football  by SHIMANO
"""
import time
import copy
import itertools
from decimal import Decimal
import cfr_axu


# Init Information
itelater = 1000
player = (0, 1)
action = ( (0, 1, 2, 3, 4), #InRun, OutRun, ShortPass, MiddlePass, LongPass
           (0, 1, 2) )#4men, 5men, 6men
chance_action = (0, 1, 2)

payoff, information_set, infoset_player, infoset_action, infoset_chance, sigma, nu_sigma_list, sigma_sum, Regret, pi_i_sum = cfr_axu.create_master_data(action, chance_action)

child_EU_dict = {}


def CFR(h, i, t, pi_i, pi_other, init_utility):
    
    for c in information_set:
        if (h in c) or (h == c):
            info_index = information_set.index(c)
    
    if len(h) == 3:
        if i == 0:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return Decimal(str(1))
            else:
                if str(h) in child_EU_dict:
                    return child_EU_dict[str(h)][i]
                else:
                    EU = cfr_axu.CFR_child( Decimal(str(payoff[h[0]][h[1]][h[2]])), h, itelater, player, action, chance_action )
                    dummy_EU1 = copy.copy(EU)
                    child_EU_dict[str(h)] = dummy_EU1
                    return EU[i]
        else:
            if payoff[h[0]][h[1]][h[2]] >= 10:
                return Decimal(str(-1))
            else:
                if str(h) in child_EU_dict:
                    return child_EU_dict[str(h)][i]
                else:
                    EU = cfr_axu.CFR_child( Decimal(str(payoff[h[0]][h[1]][h[2]])), h, itelater, player, action, chance_action )
                    dummy_EU2 = copy.copy(EU)
                    child_EU_dict[str(h)] = dummy_EU2
                    return EU[i]
    
    if h in infoset_chance:
        eu = Decimal(str(0))
        for a in chance_action:
            dummy_eu = copy.copy(h)
            dummy_eu.append(a)
            eu += sigma[info_index][a] * CFR( dummy_eu, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
        return eu
    
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
    if infoset_player[i] == 3:
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