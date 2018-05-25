import ngram as ng
from assignment2.SAX import *

class NGram_methods(object):

    def __init__(self, df, word_sizes):
        self.dataframe = df
        self.wordsizes = word_sizes
        self.dictionary = dict()
        self.discretize_data()

    def discretize_data(self):
        keys = self.dataframe.keys()
        for key in keys:
            vals = self.dataframe[key]
            self.dictionary[key] = self.apply_SAX(vals, key)[0]

    def analyze_signal(self, new_signal, new_signal_key):
        signal_discretized = self.apply_SAX(new_signal, new_signal_key)
        return self.apply_ngram_methods(signal_discretized, new_signal_key)

    def apply_SAX(self, signal, key):
        sax = SAX(wordSize=self.wordsizes[key])
        return sax.to_letter_rep(signal)

    def apply_ngram_methods(self, discretized_new_signal, key):
        discretized_original_signal = self.dictionary[key]
        ngram = ng.NGram()
        splits = list(ngram.split(discretized_original_signal))
        for x in splits:
            ngram.add(x)
        list_new_signal = ngram.split(discretized_new_signal[0])
        scores = self.get_ngram_similarities(ngram, list_new_signal)
        index_list = discretized_new_signal[1]
        res = dict()
        for i in range(len(index_list)):
            tuple = index_list[i]
            res[tuple] = scores[i]
        return res

    def get_ngram_similarities(self, ngram, list_new):
        comparison_scores = list()
        for x in list_new:
            score = ngram.search(x)[0][1]
            comparison_scores.append(score)
        return comparison_scores

    def compare_complete_string(self, new_signal, new_signal_key):
        discretized_new_signal = self.apply_SAX(new_signal, new_signal_key)
        discretized_original_signal = self.dictionary[new_signal_key]
        return ng.NGram.compare(discretized_new_signal, discretized_original_signal)

    def overview_scores(self, scores):
        mean, std, min, max = self.get_scores(scores)
        print('Statistical overview of the scores')
        print('Average score: %.5f' % mean)
        print('Standard deviation: %.5f' % std)
        print('Minimum score: %.5f' % min)
        print('Maximum score: %.5f' % max)

    def get_scores(self, scores):
        return np.mean(scores), np.std(scores), np.min(scores), np.max(scores)