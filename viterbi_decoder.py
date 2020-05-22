'''
This Conventional Viterbi Decoder is based on Hard Decision Decoding using Hamming Distance as the basis for
comparison. This Decoder is based on the Convolutional Encoder having code rate = 1/2 and constraint
length = 3
Its output includes the trellis diagram for the decoder and the resulting input that will be equal to the output
had the noise been absent
'''

import random

def Hamming_Dist(num1, num2):           # for hard decision decoding
    dist = 0
    for i in range(len(num1)):
        if num1[i] != num2[i]:
            dist += 1
    return dist

def viterbi(obs, start_metric, trellis):
    V = [{}]    # will contain the path metrics and will be used in backtrack
    for st in trellis.keys():
        V[0][st] = {"metric": start_metric[st], "branch": None}     # putting the start metrics in the path for calculations ahead
    for t in range(1, len(obs) + 1):                # iterations for future time-stamps
        V.append({})
        branches = []
        if t == 1:                                  # for first time-stamp
            states = []
            prev_st = '00'                          # we assume our decoder starts from state '00'
            for st in trellis.keys():
                if trellis[st]['b1']['prev_state'] == prev_st:
                    states.append(st)
                    branches.append('b1')
                elif trellis[st]['b2']['prev_state'] == prev_st:
                    states.append(st)
                    branches.append('b2')
            for i in range(len(states)):
                branch_metric = 0 + Hamming_Dist(trellis[states[i]][branches[i]]["outb"], obs[t - 1])
                V[t][states[i]] = {"metric": branch_metric, 'branch': branches[i]}
            V[t]['01'] = {"metric": None}
            V[t]['11'] = {"metric": None}
            continue

        if t == 2:                                  # second time-stamp is also a specific case to be taken care of
            for st in trellis.keys():
                branches = []
                prev_st = None
                for i in range(len(states)):
                    if trellis[st]['b1']['prev_state'] == states[i]:
                        branches.append('b1')
                        prev_st = states[i]

                    elif trellis[st]['b2']['prev_state'] == states[i]:
                        branches.append('b2')
                        prev_st = states[i]

                branch_metric = V[t-1][prev_st]["metric"] + Hamming_Dist(trellis[st][branches[0]]["outb"], obs[t - 1])
                V[t][st] = {"metric": branch_metric, "branch": branches[0]}
            continue

        for st in trellis.keys():
            # Check for least Hamming Distance for the correct branch metric
            prev_st = trellis[st]['b1']['prev_state']
            first_bmetric = V[t - 1][prev_st]["metric"] + Hamming_Dist(trellis[st]['b1']['outb'], obs[t - 1])       # calculating first branch metric
            prev_st = trellis[st]['b2']['prev_state']
            second_bmetric = V[t - 1][prev_st]["metric"] + Hamming_Dist(trellis[st]['b2']['outb'], obs[t - 1])      # calculating second branch metric
            if first_bmetric <= second_bmetric:
                V[t][st] = {"metric": first_bmetric, 'branch': 'b1'}
            else:
                V[t][st] = {"metric": second_bmetric, 'branch': 'b2'}

    for st in trellis.keys():                                       # displaying the complete trellis of the VD
        for t in range(len(V)):
            print(V[t][st]["metric"], end="\t")
        print('\n')

    smaller = min(V[-1][st]["metric"] for st in trellis.keys())     # finding the smallest branch metric
    path = []
    source_states = []
    for st in trellis.keys():                                   # finding all the terminals having smallest metric
        if V[-1][st]["metric"] == smaller:
            source_states.append(st)
    index_source = random.randint(0, len(source_states)-1)      # randomly selecting a state out of the states with smallest metric
    source_state = source_states[index_source]
    for t in range(len(obs), 0, -1):                            # backtracking starts here
        branch = V[t][source_state]["branch"]
        path.insert(0, trellis[source_state][branch]['inb'])
        source_state = trellis[source_state][branch]['prev_state']
    print(path)

if __name__ == '__main__':
    start_metric = {'00': 0, '01': 0, '10': 0, '11': 0}
    obs = ['00', '01', '01', '10', '10']
    trellis = {
        '00': {'b1': {'outb': '00', 'inb': '0', 'prev_state': '00'}, 'b2': {'outb': '11', 'inb': '0', 'prev_state': '01'}},
        '01': {'b1': {'outb': '01', 'inb': '0', 'prev_state': '10'}, 'b2': {'outb': '10', 'inb': '0', 'prev_state': '11'}},
        '10': {'b1': {'outb': '11', 'inb': '1', 'prev_state': '00'}, 'b2': {'outb': '00', 'inb': '1', 'prev_state': '01'}},
        '11': {'b1': {'outb': '10', 'inb': '1', 'prev_state': '10'}, 'b2': {'outb': '01', 'inb': '1', 'prev_state': '11'}},
            }
    viterbi(obs, start_metric, trellis)