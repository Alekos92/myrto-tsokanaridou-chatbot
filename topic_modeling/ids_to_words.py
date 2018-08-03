import numpy as np
import tensorflow as tf
import numpy as np

from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from unidecode import unidecode

import pickle

st = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'\w+')
english_stop_words = set(stopwords.words('english'))

#
# def f(id, pos):
#     list = []
#
#     with open('../data/vocab_mixed_subreddits.bpe.from') as f:
#         for line in f:
#             list.append(line.strip())
#
#         word = list[id]
#         word = st.stem(unidecode(word).replace('▁', '').replace('#', '').lower())
#         print(word)
#
#         with open('../topic_modeling/words.pickle', 'rb') as handle:
#             d = pickle.load(handle)
#
#             if word not in d:
#                 return 0.0
#
#             return d[word][pos]


with open('../topic_modeling/ids_to_topic_vectors.pickle', 'rb') as handle:
    mapper = pickle.load(handle)

# def f(id, pos):
#     return mapper[id][pos]


vf = np.vectorize(lambda id, pos: np.float32(mapper[id][pos]))

# def g(x):
#     return np.concatenate((vf(x, 0), vf(x, 1), vf(x, 2)), axis=2)


a = tf.constant([[1, 2, 3], [4000, 7000, 6]], dtype=tf.int32)
a = tf.expand_dims(a, axis=-1)
b = tf.py_func(lambda x: np.concatenate((vf(x, 0), vf(x, 1), vf(x, 2)), axis=2), [a], tf.float32)

with tf.Session() as sess:
    print(sess.run(b))
