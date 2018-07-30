from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from unidecode import unidecode
import numpy as np
import pickle

"""
position 0: politics
position 1: sports
position 2: movies
"""

st = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'\w+')
english_stop_words = set(stopwords.words('english'))

d = {}

counter = 0

for f, g, vector in [
    [open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/politics_train.from', 'r'),
     open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/politics_train.to', 'r'),
     [1, 0, 0]],
    [open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/sports_train.from', 'r'),
     open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/sports_train.to', 'r'),
     [0, 1, 0]],
    [open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/movies_train.from', 'r'),
     open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/movies_train.to', 'r'),
     [0, 0, 1]]
]:

    for (x, y) in zip(f, g):
        counter += 1
        if counter % 10000 == 0:
            print('Working on line {}'.format(counter))
        for z in x, y:
            lower_no_accents = unidecode(z).lower()
            words = tokenizer.tokenize(lower_no_accents)
            words_no_stopwords = [w for w in words if w not in english_stop_words]
            stemmed_words_no_stopwords = [st.stem(w) for w in words_no_stopwords]

            for w in stemmed_words_no_stopwords:
                if w not in d:
                    d[w] = [vector]
                else:
                    d[w].append(vector)

    f.close()
    g.close()

for key, value in d.items():
    d[key] = np.mean(value, axis=0)

print(len(d.items()))
print(d['trump'])

with open('words.pickle', 'wb') as h:
    pickle.dump(d, h)
