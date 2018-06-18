from numpy import *
from decimal import *

# A probabilistic non-deterministic finite state automaton model (I,S,T)
# I = array of initial state probabilities
# F = array of final probabilities
# S = matrix of symbols probabilities per state
# T = 3D matrix of transition probabilities given a symbol-state pair

# Two numeric representations: Decimal (accurate but slow), floats (fast but sloppy)
USE_DECIMAL = False
getcontext().prec = 250

def number(num):
    if USE_DECIMAL:
        return Decimal(num)
    else:
        return float(num)

# Normalize the values in an array to sum to 1.0
def normalize(arr):
 sumarr = number(sum(arr))
 if sumarr != 0.0:
     for i in range(len(arr)):
         arr[i] = arr[i] / sumarr

# Gets a random index in an array, assuming it sums up to 1.0
def getindex(arr):
 numb = random.random()
 sumn = number(0)
 for i in range(len(arr)):
     sumn = sumn + arr[i]
     if sumn >= numb:
         return i
 return len(arr) - 1

# Creates an model filled with 0 probabilities
def emptymodel(numstates,alphabet):
  I = array([number(0.0)] * numstates)
  F = array([number(0.0)] * numstates)
  S = []
  for i in range(numstates):
     newrow = array([number(0.0)] * alphabet)
     S.append(newrow)

  T = []
  for i in range(alphabet):
     T.append([])
     for j in range(numstates):
         newrow = array([number(0.0)] * numstates)
         T[i].append(newrow)

  return (I,F,S,T)

# Generate a random string from a model
def generate((I,F,S,T)):
 state = getindex(I)
 sequence = []
 while True:
     index = getindex(S[state].tolist())
     assert(S[state][index] != 0)
     if F[state] >= random.random() or len(sequence) > 1000:
         return sequence
     symbol = getindex(S[state])
     nextstate = getindex(T[symbol][state])
     assert(T[symbol][state][nextstate] != 0)
     sequence.append(symbol)
     state = nextstate
 return []

# Generate a list of random strings from a model
def generateset((I,F,S,T), num):
  train = []
  for i in range(num):
     state = getindex(I)
     sequence = generate((I,F,S,T))
     train.append(sequence)
  return train

# Computes string probabilities forwards using a dict for hashing (recursion)
def computeprobabilityrecursion((I,F,S,T),sequence,index,state,DPdict):
  # Probability = P(final)
  if index == len(sequence):
      DPdict[tuple([state])] = F[state]
      return F[state]

  # Return the already hashed result
  if DPdict.has_key(tuple([state] + sequence[index:len(sequence)])):
      return DPdict[tuple([state] + sequence[index:len(sequence)])]

  # For every possible next state s:
  # Probability += P(symbol) * P(transition to s) * P(future)
  symb_prob  = S[state][sequence[index]]
  final_prob = F[state]
  prob  = number(0.0)
  for nextstate in range(len(T[sequence[index]][state])):
      if T[sequence[index]][state][nextstate] > 0.0:
          trans_prob = T[sequence[index]][state][nextstate]
          future_prob = computeprobabilityrecursion((I,F,S,T),sequence,index+1,nextstate,DPdict)
          prob = prob + (number(1.0)-final_prob) * symb_prob * trans_prob * future_prob

  # Hash the result
  DPdict[tuple([state] + sequence[index:len(sequence)])] = prob
  return prob

# Computes string probabilities forwards using a dict for hashing
def computeprobability((I,F,S,T),sequence,DPdict):
  result = number(0.0)

  for state in range(len(I)):
      if I[state] > 0.0:
          result = result + I[state] * computeprobabilityrecursion((I,F,S,T),sequence,0,state,DPdict)
  return result

# Computes all probabilities in a given list of examples
def computeprobabilities((I,F,S,T),sett):
 probs = []
 DPdict = dict()
 for sequence in sett:
    probs.append(computeprobability((I,F,S,T),sequence,DPdict))
 return probs
