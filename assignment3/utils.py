import queue as q

def sort_dict_by_value(freq, max_val):
    pq = q.PriorityQueue()
    for ip in freq:
        # This is a trick to store frequencies in descending order:
        # subtract the actual frequency of the maximum size of the sample.
        pq.put((max_val - freq[ip], ip))
    res = dict()
    while not pq.empty():
        x = pq.get()
        # Apply correction to get the actual frequencies back.
        res[x[1]] = max_val - x[0]
    return res

def select_first_k(dictionary, k):
    keyset = list(dictionary.keys())
    if len(keyset) < k:
        return dictionary
    res = dict()
    for i in range(k):
        key = keyset[i]
        res[key] = dictionary[key]
    return res

def keys_in_common(dict1, dict2):
    count = 0
    for k in dict1:
        if k in dict2:
            count += 1
    return count

def keys_in_same_position(dict1, dict2):
    count = 0
    keys1, keys2 = list(dict1.keys()), list(dict2.keys())
    for i in range(len(keys1)):
        if i < len(keys2) and keys1[i] == keys2[i]:
            count += 1
    return count

def remove_empty_strings(array):
    res = []
    for x in array:
        if not x == '':
            res.append(x)
    return res