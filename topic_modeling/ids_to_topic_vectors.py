from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from unidecode import unidecode

import pickle

st = SnowballStemmer('english')
tokenizer = RegexpTokenizer(r'\w+')
english_stop_words = set(stopwords.words('english'))

from_list = []
to_list = []

with open('../data/vocab_mixed_subreddits.bpe.from') as f:
    for line in f:
        from_list.append(line.strip())

with open('../topic_modeling/words.pickle', 'rb') as handle:
    d = pickle.load(handle)
    for id in range(len(from_list)):
        word = from_list[id]
        word = st.stem(unidecode(word).replace('▁', '').replace('#', '').lower())
        if word not in d:
            to_list.append([0.0, 0.0, 0.0])
        else:
            to_list.append(d[word])

# with open('ids_to_topic_vectors.pickle', 'wb') as h:
#     pickle.dump(to_list, h)

print(from_list[4000])
print(to_list[4000])