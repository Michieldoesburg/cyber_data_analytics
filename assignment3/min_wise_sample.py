import queue as q
import random as r

class MinWiseSample(object):

    def __init__(self, maxSize):
        self.ms = maxSize
        self.sample = q.PriorityQueue(maxsize=maxSize)

    def add(self, x):
        # Decided to use uniform values between 0 and 100 as opposed to between 0 and 1.
        # Comparisons are easier made this way due to the nature of floating point comparisons.
        score = r.uniform(0, 100)
        tuple = (score, x)
        if self.sample.full():
            # Check if the first item in the queue has a score that is lower than the score of the new tuple.
            first_elem = self.sample.get()
            first_elem_score = first_elem[0]
            # If the score of the first tuple is lower, then remove this tuple and add the new one.
            # Else, put the original tuple back.
            if first_elem_score < score:
                self.sample.put(tuple)
            else:
                self.sample.put(first_elem)
        # If the PQ is not yet full, add the new tuple no matter what.
        else:
            self.sample.put(tuple)

    def count(self):
        count = dict()
        # Count frequencies of sampled IP addresses.
        while not self.sample.empty():
            ip = self.sample.get()[1]
            if ip in count:
                count[ip] += 1
            else:
                count[ip] = 1
        return count

    def count_and_sort(self):
        ip_freq = self.count()
        # Sort by priority queue.
        pq = q.PriorityQueue()
        for ip in ip_freq:
            # This is a trick to store frequencies in descending order:
            # subtract the actual frequency of the maximum size of the sample.
            pq.put((self.ms - ip_freq[ip], ip))
        res = dict()
        while not pq.empty():
            x = pq.get()
            # Apply correction to get the actual frequencies back.
            res[x[1]] = self.ms - x[0]
        return res