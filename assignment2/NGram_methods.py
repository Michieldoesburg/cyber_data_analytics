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
            self.dictionary[key] = self.apply_SAX(vals, key)

    def analyze_signal(self, new_signal, new_signal_key):
        signal_discretized = self.apply_SAX(new_signal, new_signal_key)
        return self.apply_ngram_methods(signal_discretized, new_signal_key)

    def apply_SAX(self, signal, key):
        sax = SAX(wordSize=self.wordsizes[key])
        return sax.to_letter_rep(signal)[0]

    def apply_ngram_methods(self, discretized_new_signal, key):
        discretized_original_signal = self.dictionary[key]
        ngram = ng.NGram
        ngram.add(self.ngram.split(discretized_original_signal))
        list_new_signal = ngram.split(discretized_new_signal)
        return self.get_ngram_similarities(ngram, list_new_signal)

    def get_ngram_similarities(self, ngram, list_new):
        comparison_scores = list()
        for x in list_new:
            score = ngram.search(x)[0][1]
            comparison_scores.append(score)
        return comparison_scores

    def overview_scores(self, scores):
        print('Statistical overview of the scores')
        print('Average score: %.5f' % np.mean(scores))
        print('Standard deviation: %.5f' % np.std(scores))
        print('Minimum score: %.5f' % np.min(scores))
        print('Maximum score: %.5f' % np.max(scores))