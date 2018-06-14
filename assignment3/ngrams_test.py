import nltk
from nltk.tokenize import word_tokenize
from nltk.util import ngrams
from nltk.probability import *

str = 'abcdefgacdheekanmskfhudsuifbgxzbfesbfzxcmfuxdbgfnm'

trigrams = nltk.trigrams(str)
condition_pairs = (((w0, w1), w2) for w0, w1, w2 in trigrams)
cfd = nltk.ConditionalFreqDist(condition_pairs)
for k in cfd.keys():
    print('Key:')
    print(k)
    print('Value:')
    cfd[k].tabulate()