f = open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/sports_train.from', 'r')
g = open('/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/sports_train.to', 'r')

limit = 100
count = 0

for (x, y) in zip(f, g):
    count += 1
    print('Q: {}'.format(x))
    print('A: {}'.format(y))
    print('\n')

    if count == limit:
        break

f.close()
g.close()
