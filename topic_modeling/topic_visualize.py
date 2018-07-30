import pickle
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import MDS

with open('words.pickle', 'rb') as handle:
    d = pickle.load(handle)

word_list = [
    'trump',
    'hillary',
    'congress',
    'film',
    'movie',
    'corrupt',
    'goal',
    'athletic',
    'lebron',
    'record',
    'oscar',
    'avengers',
    'law',
    'congress',
    'bafta',
    'best',
    'like',
    'impressive'
]

# pca = PCA(n_components=2)
mds = MDS(n_components=2)

transformed_word_list = mds.fit_transform([d[w] if w in d else [0, 0, 0] for w in word_list])

plt.scatter(transformed_word_list[:, 0], transformed_word_list[:, 1])

for w, p in zip(word_list, transformed_word_list):
    plt.annotate(w, (p[0], p[1]))

plt.savefig('illustration.png')