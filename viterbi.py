'''
    Implementation of the Viterbi Algorithm on Python. Example from Wikipedia. Doctor examining a village to see whether each
    person has 'Fever' or is 'Healthy'. Each person is diagnosed by the doctor based on the observations of the patient each day, namely
    'Normal', 'Cold' and 'Dizzy'.
    The doctor assumes that the patient tends to be 'healthy' the first day. So based on the observations the following days, the
    doctor has to diagnose the patient's hidden state, which makes up a hidden Markov Model (HMM).
'''

# specifying the assumptions made by the doctor and the given observations that help in judging the most likely states out of the hidden states
obs = ('normal', 'cold', 'dizzy')       # observations of the patient each day
states = ('healthy', 'fever')           # hidden states which have to be gauged by the doctor using this algo
start_p = {'healthy': 0.6, 'fever': 0.4}    # doctor's belief about which state the HMM is in when the patient first visits
trans_p = {'healthy': {'healthy': 0.7, 'fever': 0.3}, 'fever': {'healthy': 0.4, 'fever': 0.6}}
            # transition probability describing the chance of changing from one state to another the next day
emit_p = {'healthy': {'normal': 0.5, 'cold': 0.4, 'dizzy': 0.1}, 'fever': {'normal': 0.1, 'cold': 0.3, 'dizzy': 0.6}}
            # emission probability describing the probability of observation given the hidden state

# Example: The patient visits for three days in a row and the doctor discovers that he fells normal the first day,
# cold the second day and feels dizzy the third day.
# So the doctor asks "what is the most likely sequence of health conditions that would explain these observations"

# Now we define the Viterbi Algorithm which takes in all these factors into account and outputs the most likely output
def viterbi(obs, states, start_p, trans_p, emit_p):
    V = [{}]        # creating an empty trellis
    for st in states:
        V[0][st] = {"prob": start_p[st] * emit_p[st][obs[0]], "prev": None}     # trellis for first day
    for t in range(1, len(obs)):
        V.append({})
        for st in states:
            max_tr_prob = V[t-1][states[0]]["prob"] * trans_p[states[0]][st] * emit_p[states[0]][obs[t]]
            prev_st_selected = states[0]        # just initialized, these will be driving the final decisions
            for prev_st in states[1:]:
                tr_prob = V[t-1][prev_st]["prob"] * trans_p[prev_st][st] * emit_p[st][obs[t]]
                if tr_prob > max_tr_prob:
                    max_tr_prob = tr_prob
                    prev_st_selected = prev_st

            max_prob = max_tr_prob * emit_p[st][obs[t]]
            V[t][st] = {"prob": max_prob, "prev": prev_st_selected}

    # we have constructed the matrix for probabilities and pointers to previous states
    opt = []
    max_prob = 0.0
    previous = None
    best_st = None

    # get the most likely state in the last trellis and its previous state
    for st, data in V[-1].items():
        if data["prob"] > max_prob:
            max_prob = data["prob"]
            best_st = st
    opt.append(best_st)
    previous = best_st

    # Now we will start backtracking
    for t in range(len(V)-2, -1, -1):
        opt.insert(0, V[t+1][previous]["prev"])
        previous = V[t+1][previous]["prev"]
    print(V)
    print('The steps of states are ' + ' '.join(opt) + ' with highest probability of %s' % max_prob)

def dptable(V):
    pass

viterbi(obs, states, start_p, trans_p, emit_p)
