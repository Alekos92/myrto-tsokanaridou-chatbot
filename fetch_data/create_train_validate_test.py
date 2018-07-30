import sqlite3
import random

new_data_path = '/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/'
database_path = '/data/data1/users/amandalios/reddit_dataset/reddit_sqlite_database.db'

sql_t = []
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

print('\n\n     CONVERT TO TRAINING DATA      \n\n')

cursor.execute("""SELECT * FROM parents WHERE score > 100""")
ps = cursor.fetchall()

parents_train_file = open(new_data_path + 'train.from', 'w', buffering=10000, encoding='utf8')
replies_train_file = open(new_data_path + 'train.to', 'w', buffering=10000, encoding='utf8')

parents_validate_file = open(new_data_path + 'validate.from', 'w', buffering=10000, encoding='utf8')
replies_validate_file = open(new_data_path + 'validate.to', 'w', buffering=10000, encoding='utf8')

parents_test_file = open(new_data_path + 'test.from', 'w', buffering=10000, encoding='utf8')
replies_test_file = open(new_data_path + 'test.to', 'w', buffering=10000, encoding='utf8')

count = 0


def file_chooser(train_prob, validate_prob, test_prob):
    assert train_prob + validate_prob + test_prob == 1.0

    r = random.uniform(0, 1)

    if (0 <= r < train_prob):
        return 'train'
    elif (train_prob <= r < train_prob + validate_prob):
        return 'validate'
    else:
        return 'test'


for parent_id, reply_id, parent_body, parent_subreddit, parent_utc_time, parent_score in ps:
    count += 1
    if count % 10000 == 0:
        print('Working on pair {}'.format(count))
    cursor.execute("""SELECT * FROM replies WHERE id='{}'""".format(reply_id))
    reply = cursor.fetchone()
    if reply:
        reply_id, reply_body, reply_subreddit, reply_utc_time, reply_score = reply
        destination = file_chooser(0.8, 0.1, 0.1)
        if destination == 'train':
            parents_train_file.write(parent_body + '\n')
            replies_train_file.write(reply_body + '\n')
        elif destination == 'validate':
            parents_validate_file.write(parent_body + '\n')
            replies_validate_file.write(reply_body + '\n')
        else:
            parents_test_file.write(parent_body + '\n')
            replies_test_file.write(reply_body + '\n')

parents_train_file.close()
replies_train_file.close()
parents_validate_file.close()
replies_validate_file.close()
parents_test_file.close()
replies_test_file.close()
