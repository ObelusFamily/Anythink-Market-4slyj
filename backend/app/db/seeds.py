import psycopg2
import os
from sqlalchemy import *
from faker import Faker
from urllib.parse import urlparse

print('Please fill the seeds file')
db_uri = os.environ['DATABASE_URL']
engine = create_engine(db_uri)
connection = engine.connect()
trans = connection.begin()

Faker.seed(1234)
fake = Faker()
for i in range(100):
    user_insert_query = """ INSERT INTO users (username, email, salt) VALUES (%s,%s,%s)"""
    user_to_insert = (
        fake.unique.first_name(), fake.ascii_company_email(), fake.hexify(text='salting^^:^^:^^:^^:^^:^^'))
    connection.execute(user_insert_query, user_to_insert)
    print(i, "Record inserted successfully into users table")


# get seller_id from users table
query = f'SELECT id FROM users ;'
result = connection.execute(query)
seller_id_list = result.fetchall()

for i in range(100):
    items_insert_query = """ INSERT INTO items (slug, title, description, body, image, seller_id) VALUES (%s,%s,%s,%s,%s,%s);
    """
    items_to_insert = (fake.unique.slug(), fake.catch_phrase(), fake.catch_phrase(), "", "", seller_id_list[i][0])
    connection.execute(items_insert_query, items_to_insert)
    print(1+i, "Record inserted successfully into items table")
#
# get item_id from items table
query = f'SELECT id FROM items ;'
result = connection.execute(query)
item_id_list = result.fetchall()

for i in range(100):
    comments_insert_query = """ INSERT INTO comments (body, seller_id, item_id) VALUES (%s, %s,%s)"""
    comments_to_insert = (fake.sentence(nb_words=10), seller_id_list[i][0], item_id_list[i][0])
    connection.execute(comments_insert_query, comments_to_insert)
    print(1+i, "Record inserted successfully into comments table")

trans.commit()
if connection:
    connection.close()
    print("Postgre connection is closed")

