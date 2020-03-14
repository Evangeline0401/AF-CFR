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
        else:
            for k in sample:
                #if payoff[k[0]][k[1]][k[2]] < 10:
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
        for i in sec_initial[1:]:
            initial.append(i)
    
    return initial