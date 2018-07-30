import subprocess
import json
import sqlite3


def download_file(url, path):
    print(subprocess.check_output(['wget', '-P', path, url]).decode())


def extract_file(full_path):
    extension = full_path.split('.')[-1]

    if extension == 'bz2':
        print(subprocess.check_output(['bzip2', '-dk', full_path]).decode())
    elif extension == 'xz':
        print(subprocess.check_output(['unxz', full_path]).decode())


dataset_path = '/data/data1/users/amandalios/reddit_dataset/'
combined_file_path = dataset_path + 'combined_file'
database_path = dataset_path + 'reddit_sqlite_database.db'

urls_list = [
    'http://files.pushshift.io/reddit/comments/RC_2018-03.xz',
    'http://files.pushshift.io/reddit/comments/RC_2018-04.xz'
]

file_list = [dataset_path + url.split('/')[-1] for url in urls_list]
"""
print('\n\n     DOWNLOAD AND EXTRACT FILES      \n\n')

for url, file in zip(urls_list, file_list):
    print('Downloading from url {}...'.format(url))
    download_file(url, dataset_path)

    print('Extracting file {}...'.format(file))
    extract_file(file)

print('\n\n     COMBINE FILES INTO ONE      \n\n')
print(subprocess.check_output(['cat'] + file_list + ['>', combined_file_path]).decode())
"""
print('\n\n     CREATING SQLITE DATABASE      \n\n')

sql_t = []
conn = sqlite3.connect(database_path)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS parents(id TEXT PRIMARY KEY,
                                                          reply_id TEXT,
                                                          post_body TEXT,
                                                          subreddit TEXT,
                                                          created_utc INT,
                                                          score INT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS replies(id TEXT PRIMARY KEY,
                                                          post_body TEXT,
                                                          subreddit TEXT,
                                                          created_utc INT,
                                                          score INT)""")

# go through the data

row_counter = 0  # counter for the rows
paired_rows = 0  # counter for rows that are paired, as in question-answer


def sanitize_body(body):
    """sanitize body of reddit posts"""
    body = body.replace('\n', ' newlinechar ')
    body = body.replace('\r', ' newlinechar ')
    body = body.replace('"', "'")
    return body


def acceptable_comment(body):
    """basic test to see if comment is not too short or too long"""
    """some of these constraints are not applied, maybe a decoding issue?"""
    if (len(body.split(' ')) > 50) or (len(body) < 1):
        return False
    elif len(body) > 3000:
        return False
    elif (body == '[deleted]' or body == '[removed]'):
        return False
    elif 'htt' in body:
        return False
    else:
        return True


def transaction_bldr(sql):
    global sql_t
    sql_t.append(sql)
    if len(sql_t) > 10000:
        cursor.execute('BEGIN TRANSACTION')
        for s in sql_t:
            cursor.execute(s)
        conn.commit()
        sql_t = []


def sql_insert_parent(id, reply_id, post_body, subreddit, created_utc, score):
    sql = """INSERT INTO parents (id, reply_id, post_body, subreddit, created_utc, score) VALUES ("{}","{}","{}","{}",{},{});""".format(
        id, reply_id, post_body, subreddit, created_utc, score)
    transaction_bldr(sql)


def sql_insert_reply(id, post_body, subreddit, created_utc, score):
    sql = """INSERT INTO replies (id, post_body, subreddit, created_utc, score) VALUES ("{}","{}","{}",{},{});""".format(
        id, post_body, subreddit, created_utc, score)
    transaction_bldr(sql)


# dictionary that matches each post to its highest score response
post_pairs = {}

with open(combined_file_path, buffering=1000000) as f:
    for row in f:
        row_counter += 1
        if row_counter % 1000000 == 0:
            print('Working on row {}'.format(row_counter))
        row = json.loads(row)
        id = row['id']
        parent_id = row['parent_id'].split('_')[1]
        comment_body = sanitize_body(row['body'])
        score = row['score']

        # we create a threshold for insertion in our database
        # Also, for each post we should keep only the highest score response
        # That means we need to keep checking for responses to the same comment

        if acceptable_comment(comment_body):

            if parent_id not in post_pairs:
                post_pairs[parent_id] = (id, score)
            else:
                other_id, other_score = post_pairs[parent_id]
                if score > other_score:
                    post_pairs[parent_id] = (id, score)

print('\n\nWe have {} post pairs\n\n'.format(len(post_pairs)))

print('\n\n     DATABASE INSERTION      \n\n')

parent_ids = set(post_pairs.keys())
reply_ids = set(x[0] for x in post_pairs.values())

row_counter = 0

with open(combined_file_path, buffering=1000000) as f:
    for row in f:
        row_counter += 1
        if row_counter % 10000000 == 0:
            print('Working on row {}'.format(row_counter))
        row = json.loads(row)
        id = row['id']
        post_body = sanitize_body(row['body'])
        subreddit = row['subreddit']
        created_utc = row['created_utc']
        score = row['score']

        if id in parent_ids:
            # it's a parent
            sql_insert_parent(id, post_pairs[id][0], post_body, subreddit,
                              created_utc, score)
        if id in reply_ids:
            # it's a reply
            sql_insert_reply(id, post_body, subreddit, created_utc, score)
