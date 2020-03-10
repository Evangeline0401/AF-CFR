"""
Gale-Shapley Algorithm
"""

import random

def shuffled(lst):
    tmp = lst[:]
    random.shuffle(tmp)
    return tmp

n = 10
men = ["M" + str(i) for i in range(n)]
women = ["W" + str(i) for i in range(n)]

men_preference = {m: shuffled(women) for m in men}
women_preference = {w: shuffled(men) for w in women}

print ("men_preference:")
print (men_preference)

print ("women_preference:")
print (women_preference)

m_to_w = {}
w_to_m = {}

while len(m_to_w) < n:
    man = [m for m in men if m not in m_to_w][0]
    woman = men_preference[man][0]
    if woman in w_to_m:
        # Not first propose for woman
        another_man = w_to_m[woman]
        if women_preference[woman].index(man) < women_preference[woman].index(another_man):
            # Win
            del m_to_w[another_man]
            m_to_w[man] = woman
            w_to_m[woman] = man
            men_preference[another_man].pop(0)
        else:
            # Lose
            men_preference[man].pop(0)
    else:
        # First propose for woman
        m_to_w[man] = woman
        w_to_m[woman] = man

print ("matching:")
print (m_to_w)