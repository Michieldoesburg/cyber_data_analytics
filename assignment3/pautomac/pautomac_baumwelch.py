from numpy.random.mtrand import dirichlet
from numpy import *
from sys import *

numstates = 6
alphabet = 5
ll_bound = 10.0

if len(argv) != 3:
    print "required input: trainfile testfile"
    assert(False)

train_file = argv[1]
test_file = argv[2]

def number(num):
	return float(num)

# Normalize the values in an array to sum to 1.0
def normalize(arr):
 sumarr = number(sum(arr))
 if sumarr != 0.0:
     for i in range(len(arr)):
         arr[i] = arr[i] / sumarr

# A probabilistic non-deterministic finite state automaton model (I,F,S,T)
# I = array of initial state probabilities
# F = array of final probabilities
# S = matrix of symbols probabilities per state
# T = 3D matrix of transition probabilities given a symbol-state pair

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

def writemodel((I,F,S,T)):
    f = stdout
    f.write("I: (state)\n")
    for i in range(numstates):
		if I[i] > 0.0:
			f.write("\t(" + str(i) + ") " + str(I[i]) + "\n")
    f.write("F: (state)\n")
    for i in range(numstates):
		if F[i] > 0.0:
			f.write("\t(" + str(i) + ") " + str(F[i]) + "\n")
    f.write("S: (state,symbol) \n")
    for j in range(numstates):
		for i in range(alphabet):
		   if S[j][i] > 0.0:
			   f.write("\t(" + str(j) + "," + str(i) + ") " + str(S[j][i]) + "\n")
    f.write("T: (state,symbol,state) \n")
    for j in range(numstates):
	   for i in range(alphabet):
	      for k in range(numstates):
			  if T[i][j][k] > 0.0:
			      f.write("\t(" + str(j) + "," + str(i) + "," + str(k) + ") " + str(T[i][j][k]) + "\n")

# Creates a fully connected model with random probabilities
def randommodel(numstates, alphabet):
  I = array(dirichlet([1] * numstates))
  F = array([0.0] * numstates)
  S = []
  # F is treated as an end of string symbol
  for i in range(numstates):
     probs = dirichlet([1] * (alphabet + 1))
     newrow = array(probs[0:alphabet])
     normalize(newrow)
     S.append(newrow)
     F[i] = probs[alphabet]

  T = []
  for i in range(alphabet):
     T.append([])
     for j in range(numstates):
         newrow = array(dirichlet([1] * numstates))
         T[i].append(newrow)

  return (I,F,S,T)

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

# Computes string probabilities backwards using a dict for hashing (recursion)
def computeprobabilityrecursionreverse((I,F,S,T),sequence,index,state,DPdict):
  # Probability = P(initial)
  if index == 0:
      DPdict[tuple([state])] = I[state]
      return I[state]

  # Return the already hashed result
  if DPdict.has_key(tuple([state] + sequence[0:index])):
      return DPdict[tuple([state] + sequence[0:index])]

  # For every possible previous state s:
  # Probability += P(symbol) * P(transition from s) * P(past)
  prob = number(0.0)
  for prevstate in range(len(I)):
      if T[sequence[index-1]][prevstate][state] > 0.0:
          final_prob = F[prevstate]
          symb_prob  = S[prevstate][sequence[index-1]]
          trans_prob = T[sequence[index-1]][prevstate][state]
          past_prob  = computeprobabilityrecursionreverse((I,F,S,T),sequence,index-1,prevstate,DPdict)
          
          prob = prob + ((number(1.0)-final_prob) * symb_prob * trans_prob * past_prob)

  # Hash the result
  DPdict[tuple([state] + sequence[0:index])] = prob
  return prob

# Computes string probabilities backwards using a dict for hashing
def computeprobabilityreverse((I,F,S,T),sequence,DPdict):
  result = number(0.0)

  # For every final state f:
  # Probability += P(end in f) * P(past)
  for state in range(len(I)):
      result = result + F[state] * computeprobabilityrecursionreverse((I,F,S,T),sequence,len(sequence),state,DPdict)
  return result

# Computes all probabilities in a given list of examples
def computeprobabilitiesreverse((I,F,S,T),sett):
 probs = []
 DPdict = dict()
 for sequence in sett:
    probs.append(computeprobabilityreverse((I,F,S,T),sequence,DPdict))
 return probs

def iterateEM((I,F,S,T),sett):
   backward = dict()
   probs = []
   for sequence in sett:
      probs.append(computeprobability((I,F,S,T),sequence,backward))
   # backward = P(s|start(q))

   forward = dict()
   for sequence in sett:
      computeprobabilityreverse((I,F,S,T),sequence,forward)
   # forward = P(s,end(q))

   (Inew,Fnew,Snew,Tnew) = emptymodel(numstates,alphabet)

   # P(I(q)|s) =  P(I(q),s)/P(s)
   # P(I(q)|s) =  P(I(q))*P(s|start(q))/P(s)
   for state in range(len(I)):
      for seq in range(len(sett)):
         sequence = sett[seq]
         prob = probs[seq]
         key = tuple([state] + sequence)
         if backward.has_key(key):
            Inew[state] = Inew[state] + ((I[state] * backward[key]) / prob)
   normalize(Inew)

   # P(F(q)|s) =  P(F(q),s)/P(s)
   # P(F(q)|s) =  P(end(q),s)*P(F(q))/P(s)
   for state in range(len(I)):
      for seq in range(len(sett)):
         sequence = sett[seq]
         prob = probs[seq]
         key = tuple([state] + sequence)
         if forward.has_key(key):
            Fnew[state] = Fnew[state] + ((F[state] * forward[key]) / prob)


   # P(S(q,a)|s) =  P(S(q,a),s)/P(s)
   # P(S(q,a)|s) =  P(end(q),S(q,a),tail(q))/P(s)
   # P(S(q,a)|s) =  P(end(q),head(s))*P(tail(s)|start(q))/P(s)
      Stotal = number(0.0)
      for seq in range(len(sett)):
         sequence = sett[seq]
         prob = probs[seq]
         for index in range(len(sequence)):
            key = tuple([state] + sequence[0:index])
            if forward.has_key(key):
               key2 = tuple([state] + sequence[index:len(sequence)])
               if backward.has_key(key2):
                  symprob = forward[key] * backward[key2]
                  Snew[state][sequence[index]] = Snew[state][sequence[index]] + (symprob / prob)

      if Fnew[state] != 0.0:
         Fnew[state] = Fnew[state] / (Fnew[state] + sum(Snew[state]))
      normalize(Snew[state])
   
   for state in range(len(I)):
      for seq in range(len(sett)):
         sequence = sett[seq]
         prob = probs[seq]
         for index in range(len(sequence)):
            key1 = tuple([state] + sequence[0:index])
            if forward.has_key(key1):
               for state2 in range(len(I)):
                  key2 = tuple([state2] + sequence[(index+1):len(sequence)])
                  if backward.has_key(key2):
                     transprob = (number(1.0) - F[state]) * S[state][sequence[index]] * T[sequence[index]][state][state2]
                     transprob = forward[key1] * transprob * backward[key2]
                     Tnew[sequence[index]][state][state2] = Tnew[sequence[index]][state][state2] + (transprob / prob)

   for a in range(alphabet):
      for state in range(len(I)):
         normalize(Tnew[a][state])

   return (Inew,Fnew,Snew,Tnew)

def loglikelihood(probs):
   sumt = number(0.0)
   log2 = log10(number(2.0))
   for index in range(len(probs)):
       term = log10(probs[index]) / log2
       sumt = sumt + term
   return sumt

def readset(f):
 sett = []
 line = f.readline()
 l = line.split(" ")
 num_strings = int(l[0])
 alphabet_size = int(l[1])
 for n in range(num_strings):
     line = f.readline()
     l = line.split(" ")
     sett = sett + [[int(i) for i in l[1:len(l)]]]
 return alphabet_size, sett

def writeprobs(probs,f):
 f.write(str(len(probs)) + "\n")
 for i in range(len(probs)):
     f.write(str(probs[i]) + "\n")


alphabet, train = readset(open(train_file,"r"))
alphabet, test = readset(open(test_file,"r"))

model = randommodel(numstates,alphabet)
print "loglikelihood:", loglikelihood(computeprobabilities(model,train+test))
writemodel(model)

prev = -1.0
ll = -1.0
while prev == -1.0 or ll - prev > ll_bound:
    prev = ll
    m = iterateEM(model,train+test)
    probs = computeprobabilities(m,train+test)
    ll = loglikelihood(probs)
    model = m
    print "loglikelihood: ", ll
    writemodel(model)

writeprobs(computeprobabilities(m,test),open(test_file+".bm","w"))
