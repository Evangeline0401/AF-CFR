import time
import copy
import itertools
from decimal import Decimal


def create_payoff(master_payoff):
    
    payoff = []

    L_P, H_P = [], []
    for p1 in master_payoff:
        l_p, h_p = [], []
        for p2 in p1:
            l_p.append(p2 - Decimal(str(2)))
            h_p.append(p2 + Decimal(str(3)))
        L_P.append(l_p)
        H_P.append(h_p)
    
    payoff.append(L_P)
    payoff.append(master_payoff)
    payoff.append(H_P)

    return payoff


def create_info_set(action, chance_action, payoff):

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
        # else:
        #     for k in sample:
        #         initial.append(k)
    
    return initial


def create_master_data(action, chance_action):

    # Master Data
    master_sigma = [ [Decimal(str(1))/Decimal(str(3)), Decimal(str(1))/Decimal(str(3)), Decimal(str(1))/Decimal(str(3))],
                    [Decimal(str(1))/Decimal(str(5)), Decimal(str(1))/Decimal(str(5)), Decimal(str(1))/Decimal(str(5)), Decimal(str(1))/Decimal(str(5)), Decimal(str(1))/Decimal(str(5))],
                    [Decimal(str(1))/Decimal(str(3)), Decimal(str(1))/Decimal(str(3)), Decimal(str(1))/Decimal(str(3))] ]
    master_nu_sigma_list = [ [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                            [Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                            [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))] ]
    master_sigma_sum = [ [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                        [Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                        [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))] ]
    master_Regret = [ [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                    [Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0)), Decimal(str(0))],
                    [Decimal(str(0)), Decimal(str(0)), Decimal(str(0))] ]

    # Master Payoff
    master_payoff = [ [Decimal(3),  Decimal(2), Decimal(2)],
                    [Decimal(3),  Decimal(4), Decimal(3)],
                    [Decimal(7),  Decimal(7), Decimal(5)],
                    [Decimal(8),  Decimal(9), Decimal(7)],
                    [Decimal(7), Decimal(12), Decimal(5)], ]
    payoff = create_payoff(master_payoff)

    # Create Information Set
    information_set = create_info_set(action, chance_action, payoff)

    # Create Infomation Set's Player List
    infoset_player = []
    for i in information_set:
        if len(i) == 1 or (len(i) == 3 and type(i[0]) == int) or len(i) == 6:
            infoset_player.append(3)
        elif len(i) == 3 and type(i[0]) != int:
            infoset_player.append(0)
        else:
            infoset_player.append(1)

    # Create Information Set's Action
    infoset_action = []
    for i in infoset_player:
        if i == 0:
            dummy0 = copy.copy(action[i])
            infoset_action.append(dummy0)
        elif i == 1:
            dummy1 = copy.copy(action[i])
            infoset_action.append(dummy1)
        else:
            dummy3 = copy.copy(chance_action)
            infoset_action.append(dummy3)

    # Create Chance Node's Information Set
    infoset_chance = []
    for i in information_set:
        if len(i) == 1 or (len(i) == 3 and type(i[0]) == int ) or len(i) == 6:
            dummyC = copy.copy(i)
            infoset_chance.append(dummyC)

    # Create Sigma
    sigma = []
    for i in infoset_player:
        if i == 0:
            sigma0 = copy.copy(master_sigma[i+1])
            sigma.append(sigma0)
        elif i == 1:
            sigma1 = copy.copy(master_sigma[i+1])
            sigma.append(sigma1)
        else:
            sigma3 = copy.copy(master_sigma[0])
            sigma.append(sigma3)

    # Create Some List
    nu_sigma_list, sigma_sum, Regret = [], [], []
    for i in infoset_player:
        if i == 0:
            dummy0_nu, dummy0_sigma, dummy0_Reg = copy.copy(master_nu_sigma_list[i+1]), copy.copy(master_sigma_sum[i+1]), copy.copy(master_Regret[i+1])
            nu_sigma_list.append(dummy0_nu)
            sigma_sum.append(dummy0_sigma)
            Regret.append(dummy0_Reg)
        elif i == 1:
            dummy1_nu, dummy1_sigma, dummy1_Reg = copy.copy(master_nu_sigma_list[i+1]), copy.copy(master_sigma_sum[i+1]), copy.copy(master_Regret[i+1])
            nu_sigma_list.append(dummy1_nu)
            sigma_sum.append(dummy1_sigma)
            Regret.append(dummy1_Reg)
        else:
            dummy3_nu, dummy3_sigma, dummy3_Reg = copy.copy(master_nu_sigma_list[0]), copy.copy(master_sigma_sum[0]), copy.copy(master_Regret[0])
            nu_sigma_list.append(dummy3_nu)
            sigma_sum.append(dummy3_sigma)
            Regret.append(dummy3_Reg)

    # Create pi_i_sum
    pi_i_sum = []
    for i in infoset_action:
        pi_i_sum.append(Decimal(str(0)))

    return payoff, information_set, infoset_player, infoset_action, infoset_chance, sigma, nu_sigma_list, sigma_sum, Regret, pi_i_sum


def CFR_grandchild(init_payoff, history, itelater, player, action, chance_action):

    payoff, information_set, infoset_player, infoset_action, infoset_chance, sigma, nu_sigma_list, sigma_sum, Regret, pi_i_sum = create_master_data(action, chance_action)


    def CFRCFRCFR(h, i, t, pi_i, pi_other, init_utility):
        
        for c in information_set:
            if (h in c) or (h == c):
                info_index = information_set.index(c)
        
        if len(h) == 3:
            if i == 0:
                if payoff[h[0]][h[1]][h[2]]+init_utility >= 10:
                    return Decimal(str(1))
                else:
                    return Decimal(str(0))
            else:
                if payoff[h[0]][h[1]][h[2]]+init_utility >= 10:
                    return Decimal(str(-1))
                else:
                    return Decimal(str(0))
        
        if h in infoset_chance:
            eu = Decimal(str(0))
            for a in chance_action:
                dummy_eu = copy.copy(h)
                dummy_eu.append(a)
                eu += sigma[info_index][a] * CFRCFRCFR( dummy_eu, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
            return eu
        
        nu_sigma = Decimal(str(0))
        for a in infoset_action[info_index]:
            nu_sigma_list[info_index][a] = Decimal(str(0))
        
        for a in infoset_action[info_index]:
            if infoset_player[info_index] == i:
                Dummy_i = copy.copy(h)
                Dummy_i.append(a)
                nu_sigma_list[info_index][a] = CFRCFRCFR( Dummy_i, i, t, sigma[info_index][a]*pi_i, pi_other, init_utility )
            else:
                Dummy_Not_i = copy.copy(h)
                Dummy_Not_i.append(a)
                nu_sigma_list[info_index][a] = CFRCFRCFR( Dummy_Not_i, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
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

    hogehoge = [0, 0]
    for t in range(itelater):
        for i in player:
            hogehoge[i] = CFRCFRCFR( [], i, t, Decimal(str(1)), Decimal(str(1)), init_payoff )
    
    #Result
    print ("===========================================")
    print (history, init_payoff)
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

    return hogehoge


def CFR_child(init_payoff, history, itelater, player, action, chance_action):

    payoff, information_set, infoset_player, infoset_action, infoset_chance, sigma, nu_sigma_list, sigma_sum, Regret, pi_i_sum = create_master_data(action, chance_action)


    def CFRCFR(h, i, t, pi_i, pi_other, init_utility):
        
        for c in information_set:
            if (h in c) or (h == c):
                info_index = information_set.index(c)
        
        if len(h) == 3:
            if i == 0:
                if payoff[h[0]][h[1]][h[2]]+init_utility >= 10:
                    return Decimal(str(1))
                else:
                    #return Decimal(str(0))
                    EU = CFR_grandchild( payoff[h[0]][h[1]][h[2]]+init_utility, history+h, itelater, player, action, chance_action )
                    return EU[i]
            else:
                if payoff[h[0]][h[1]][h[2]]+init_utility >= 10:
                    return Decimal(str(-1))
                else:
                    #return Decimal(str(0))
                    EU = CFR_grandchild( payoff[h[0]][h[1]][h[2]]+init_utility, history+h, itelater, player, action, chance_action )
                    return EU[i]
        
        if h in infoset_chance:
            eu = Decimal(str(0))
            for a in chance_action:
                dummy_eu = copy.copy(h)
                dummy_eu.append(a)
                eu += sigma[info_index][a] * CFRCFR( dummy_eu, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
            return eu
        
        nu_sigma = Decimal(str(0))
        for a in infoset_action[info_index]:
            nu_sigma_list[info_index][a] = Decimal(str(0))
        
        for a in infoset_action[info_index]:
            if infoset_player[info_index] == i:
                Dummy_i = copy.copy(h)
                Dummy_i.append(a)
                nu_sigma_list[info_index][a] = CFRCFR( Dummy_i, i, t, sigma[info_index][a]*pi_i, pi_other, init_utility )
            else:
                Dummy_Not_i = copy.copy(h)
                Dummy_Not_i.append(a)
                nu_sigma_list[info_index][a] = CFRCFR( Dummy_Not_i, i, t, pi_i, sigma[info_index][a]*pi_other, init_utility )
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

    hogehoge = [0, 0]
    for t in range(itelater):
        for i in player:
            hogehoge[i] = CFRCFR( [], i, t, Decimal(str(1)), Decimal(str(1)), init_payoff )
    
    #Result
    print ("===========================================")
    print (history, init_payoff)
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

    return hogehoge