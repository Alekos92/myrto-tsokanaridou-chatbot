import sqlite3
import random

new_data_path = '/data/data1/users/amandalios/myrto-tsokanaridou-chatbot/new_data/'
database_path = '/data/data1/users/amandalios/reddit_dataset/reddit_sqlite_database.db'

sql_t = []
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute("""SELECT * FROM parents""")
ps = cursor.fetchall()

politics_train_from = open(new_data_path + 'politics_train.from', 'w', buffering=10000, encoding='utf8')
politics_train_to = open(new_data_path + 'politics_train.to', 'w', buffering=10000, encoding='utf8')

sports_train_from = open(new_data_path + 'sports_train.from', 'w', buffering=10000, encoding='utf8')
sports_train_to = open(new_data_path + 'sports_train.to', 'w', buffering=10000, encoding='utf8')

movies_train_from = open(new_data_path + 'movies_train.from', 'w', buffering=10000, encoding='utf8')
movies_train_to = open(new_data_path + 'movies_train.to', 'w', buffering=10000, encoding='utf8')

parents_validate_file = open(new_data_path + 'validate_mixed_subreddits.from', 'w', buffering=10000, encoding='utf8')
replies_validate_file = open(new_data_path + 'validate_mixed_subreddits.to', 'w', buffering=10000, encoding='utf8')

parents_test_file = open(new_data_path + 'test_mixed_subreddits.from', 'w', buffering=10000, encoding='utf8')
replies_test_file = open(new_data_path + 'test_mixed_subreddits.to', 'w', buffering=10000, encoding='utf8')

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

    if parent_subreddit in ['politics', 'nba', 'soccer', 'nfl', 'hockey', 'movies']:

        count += 1
        if count % 10000 == 0:
            print('Working on pair {}'.format(count))
        cursor.execute("""SELECT * FROM replies WHERE id='{}'""".format(reply_id))
        reply = cursor.fetchone()
        if reply:
            reply_id, reply_body, reply_subreddit, reply_utc_time, reply_score = reply

            assert reply_subreddit == parent_subreddit

            destination = file_chooser(0.8, 0.1, 0.1)
            if destination == 'train':
                if parent_subreddit == 'politics':
                    politics_train_from.write(parent_body + '\n')
                    politics_train_to.write(reply_body + '\n')
                elif parent_subreddit in ['nba', 'soccer', 'nfl', 'hockey']:
                    sports_train_from.write(parent_body + '\n')
                    sports_train_to.write(reply_body + '\n')
                else:
                    movies_train_from.write(parent_body + '\n')
                    movies_train_to.write(reply_body + '\n')
            elif destination == 'validate':
                parents_validate_file.write(parent_body + '\n')
                replies_validate_file.write(reply_body + '\n')
            else:
                parents_test_file.write(parent_body + '\n')
                replies_test_file.write(reply_body + '\n')

politics_train_from.close()
politics_train_to.close()

sports_train_from.close()
sports_train_to.close()

movies_train_from.close()
movies_train_to.close()

parents_validate_file.close()
replies_validate_file.close()

parents_test_file.close()
replies_test_file.close()
