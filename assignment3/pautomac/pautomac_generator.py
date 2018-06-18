from numpy import *
from decimal import *
from pickle import *
from numpy.random.mtrand import dirichlet

from pautomac_model import *

numstates  = int((random.random()*70.0) + 5.0)
alphabet  = int((random.random()*40.0) + 4.0)

symbolsparsity = (random.random()*0.8) + 0.1
transitionsparsity = (random.random()*0.8) + 0.1
transitionsparsity = min(transitionsparsity,(random.random()*0.9)+0.05)
numinitial = int(transitionsparsity * float(numstates))
numfinal = int(symbolsparsity * float(numstates))

#numstates = 3
#alphabet = 2

#symbolsparsity = 0.8
#transitionsparsity = 0.8
#numinitial = 1
#numfinal   = 2

numtrain = 20000
if random.random() > 0.8:
    numtrain = 100000
numtest  = 1000

minavglength = 5.0
maxavglength = 50.0
maxlength = 250

# randomly fill num 1.0's in place of 0.0's in an array
def fillarray(arr, num):
 if sum(arr == 0.0) == 0:
     return

# zeros = sum(arr == 0.0)
# mod = int(numb * zeros)
# count = 0
# for i in range(len(arr)):
#    if arr[i] == 0.0:
#       if count == mod:
#         arr[i] = number(1.0)
#         break
#       else:
#         count = count + 1
 while sum(arr > 0.0) < num:
     numb = random.random()
     index = int(len(arr) * numb)
     if arr[index] == 0.0:
         arr[index] = number(1.0)

# randomly fill num 1.0's in place of 0.0's in a matrix
def fillmatrix(matr, num):
 if sum([matr[i] == 0.0 for i in range(len(matr))]) == 0:
     return
 zeros = 0
 for i in range(len(matr)):
     if sum(matr[i] == 0.0) != 0:
        zeros = zeros + 1

# numb = random.random()
# mod = int(numb * zeros)
# count = 0
# for i in range(len(matr)):
#    if sum(matr[i] == 0.0) != 0:
#       if count == mod:
#         fillarray(matr[i], 1)
#         break
#       else:
#         count = count + 1

 while sum([matr[i] > 0.0 for i in range(len(matr))]) < num:
     numb = random.random()
     x = int(len(matr) * numb)
     fillarray(matr[x],sum(matr[x] > 0.0)+1)

     #numb = random.random()
     #y = int(len(matr[x]) * numb)
     #if matr[x][y] == 0.0:
     #    matr[x][y] = number(1.0)

# randomly fill num 1.0's in place of 0.0's in a 3D matrix
def fill3Dmatrix(matr, num):
 full = False
 oldsum = 0
 tries = 0
 while not full:
     sumf = number(0)
     for i in range(len(matr)):
         for j in range(len(matr[i])):
             sumf = sumf + sum(matr[i][j] > 0.0)
     full = (sumf == num | tries > 100)
     if sumf > num:
        return
     if sumf == oldsum:
        tries = tries + 1
     else:
        tries = 0
     #print sumf, num
     
#     zeros = 0
#     for i in range(len(matr)):
#         if sum([matr[i][j] == 0.0 for j in range(len(matr[i]))]) != 0:
#            zeros = zeros + 1

#     mod = int(numb * zeros)
#     count = 0
#     for i in range(len(matr)):
#        if sum([matr[i][j] == 0.0 for j in range(len(matr[i]))]) != 0:
#           if count == mod:
#             fillmatrix(matr[i], 1)
#             break
#           else:
#             count = count + 1
#     numb = random.random()

     numb = random.random()
     x = int(len(matr) * numb)
     #numb = random.random()
     fillmatrix(matr[x], sum([matr[x][i] > 0.0 for i in range(len(matr[x]))])+1)
     oldsum = sumf
     #y = int(len(matr[x]) * numb)
     #numb = random.random()
     #z = int(len(matr[x][y]) * numb)
     #if matr[x][y][z] == 0.0:
     #    matr[x][y][z] = number(1.0)

# replaces 1.0 with values from a Dirichlet distribution
def filldirichlet(arr):
  probs = dirichlet([1] * sum(arr))
  j = 0
  for i in range(len(arr)):
      if arr[i] == 1.0:
          arr[i] = number(probs[j])
          j = j + 1

# ----------- Generating the different models

# PNFA
def generatePNFA():
  I = array([0.0] * numstates)
  fillarray(I,numinitial)
  filldirichlet(I)

  F = array([0.0] * numstates)
  fillarray(F,numfinal)
  S = []
  for i in range(numstates):
     newrow = array([0.0] * alphabet)
     fillarray(newrow,1)
     S.append(newrow)
  fillmatrix(S,int(round(symbolsparsity*numstates*alphabet)))
  for i in range(numstates):
     probs = array(S[i].tolist() + [F[i]])
     filldirichlet(probs)
     S[i] = probs[0:len(S[i])]
     F[i] = probs[len(S[i])]
     normalize(S[i])

  T = []
  numempty = 0
  for i in range(alphabet):
     T.append([])
     for j in range(numstates):
         newrow = array([number(0.0)] * numstates)
         fillarray(newrow,1)
         if S[j][i] == 0.0:
             numempty = numempty + 1
             newrow = array([number(-1.0)] * numstates)
         T[i].append(newrow)
  fill3Dmatrix(T,int(round(transitionsparsity*((alphabet*numstates) - numempty)*numstates)))
  for i in range(alphabet):
      for j in range(numstates):
          if S[j][i] != 0:
              filldirichlet(T[i][j])

  return (I,F,S,T)

# HMM
def generateHMM():
  (I,F,S,T) = generatePNFA()

  Ts = []
  T = []
  numempty = 0
  for i in range(numstates):
     newrow = array([number(0.0)] * numstates)
     fillarray(newrow,1)
     Ts.append(newrow)
  fillmatrix(Ts,int(round(transitionsparsity*numstates*numstates)))
  for i in range(numstates):
     filldirichlet(Ts[i])
  for i in range(alphabet):
     T.append(copy(Ts))

  return (I,F,S,T)

# PDFA
def generatePDFA():
  (I,F,S,T) = generatePNFA()

  I = array([number(0.0)] * numstates)
  fillarray(I,1)

  T = []
  numempty = 0
  for i in range(alphabet):
     T.append([])
     for j in range(numstates):
         newrow = array([number(0.0)] * numstates)
         fillarray(newrow,1)
         if S[j][i] == 0.0:
             numempty = numempty + 1
             newrow = array([number(-1.0)] * numstates)
         T[i].append(newrow)

  return (I,F,S,T)

# MC
def generateMC():
  global numstates
  numstates = alphabet

  (I,F,S,T) = generatePNFA()

  I = array([number(1.0)] * numstates)
  normalize(I)

  T = []
  numempty = 0
  for i in range(alphabet):
     T.append([])
     for j in range(numstates):
         newrow = array([number(0.0)] * numstates)
         newrow[i] = 1.0
         if S[j][i] == 0.0:
             numempty = numempty + 1
             newrow = array([number(-1.0)] * numstates)
         T[i].append(newrow)

  return (I,F,S,T)

# --------------------

def testconsistency((I,F,S,T)):
    inconsistent = []
    for i in range(len(F)):
        if F[i] == 0.0:
            inconsistent = inconsistent + [i]

    while(inconsistent != []):
        found = False
        for i in copy(inconsistent):
            for s in range(len(S[i])):
                for t in range(len(T[s][i])):
                    if T[s][i][t] != 0.0 and t not in inconsistent:
                        found = True
            if found:
                inconsistent.remove(i)

        if found == False:
            return False
    return True

def testaveragelength((I,F,S,T)):
     sumlen  = 0
     maxlen = 0
     for i in range(100):
         sequence = generate((I,F,S,T))
         if len(sequence) > 250:
             return 250, 250
         sumlen = sumlen + len(sequence)
         maxlen = max(maxlen,len(sequence))
     avglen = float(sumlen) / 100.0
     return avglen, maxlen

def writeset(sett,f):
 f.write(str(len(sett)) + " " + str(alphabet) + "\n")
 for i in range(len(sett)):
     string = ""
     for j in range(len(sett[i])):
        string = string + " " + str(sett[i][j])
     f.write(str(len(sett[i])) + string + "\n")

def writeprobs(probs,f):
 f.write(str(len(probs)) + "\n")
 for i in range(len(probs)):
     f.write(str(probs[i]) + "\n")

def writemodel((I,F,S,T),f):
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

def uniquelist(l):
   seen = [] 
   return [c for c in l if not (c in seen or seen.append(c))]

def generatemodel(t):
   if t == 1:
     return generatePDFA()
   if t == 2:
     return generateHMM()
   if t == 3:
     return generatePNFA()
   return 0

def rungenerator(t,n):
   model = generatemodel(t)
   consistency = testconsistency(model)
   length = 0.0
   max_length = 0
   if consistency:
       length, max_length = testaveragelength(model)

   print "generated new ", t
   print "size:", numstates, "alphabet:", alphabet, "symbol sparsity:", symbolsparsity, "transition sparsity:", transitionsparsity
   print "average length: ", length, "maximum length:", max_length, "consistency:", consistency

   tries = 1
   while consistency == False or length < minavglength or length >= maxavglength or max_length >= maxlength:
       if tries > 5:
           return
       tries = tries + 1
       
       model = generatemodel(t)
       consistency = testconsistency(model)
       if consistency:
           length, max_length = testaveragelength(model)

       print "generated new ", t
       print "size:", numstates, "alphabet:", alphabet, "symbol sparsity:", symbolsparsity, "transition sparsity:", transitionsparsity
       print "average length: ", length, "maximum length:", max_length, "consistency:", consistency


   test = generateset(model,numtest)
   test = uniquelist(test)
   tries = 0
   while len(test) < 1000:
      newtest = generateset(model,numtest)
      test = uniquelist(test+newtest)
      if len(test) > 1000:
        test = test[0:1000]
      tries = tries + 1
      if tries > 25:
         return
   train = generateset(model,numtrain)

   print "generated test and train sets"
   print "lengths of train:"
   print bincount([len(string) for string in train])
   print "lengths of test:"
   print bincount([len(string) for string in test])

   writeset(train,open(str(n) + "-" + str(t) + "pautomac.train","w"))
   writeset(test,open(str(n) + "-" + str(t) + "pautomac.test","w"))
   dump(model,open(str(n) + "-" + str(t) + "pautomac_model.dump","w"))
   writemodel(model,open(str(n) + "-" + str(t) + "pautomac_model.txt","w"))

   solution = computeprobabilities(model,test)
   normalize(solution)
   writeprobs(solution,open(str(n) + "-" + str(t) + "pautomac_solution.txt","w"))

for i in range(100000):

   numstates = int((random.random()*70.0) + 5.0)
   alphabet = int((random.random()*20.0) + 4.0)

   symbolsparsity = (random.random()*0.6) + 0.2
   transitionsparsity = (random.random()*(0.2 - (1.0 / float(numstates)))) + (1.0 / float(numstates))
   numinitial = int(transitionsparsity * float(numstates))
   numfinal   = int(symbolsparsity * float(numstates))

   numtrain = 20000
   if random.random() > 0.8:
       numtrain = 100000
   numtest  = 1000

   minavglength = 5.0
   maxavglength = 50.0
   maxlength = 100

   rungenerator(2,i)


