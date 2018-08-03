import pickle

with open('../data/cache_data_vocab.pickle', 'rb') as handle:
    d = pickle.load(handle)

print(d)
