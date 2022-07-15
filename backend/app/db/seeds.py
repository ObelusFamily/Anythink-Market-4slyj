import psycopg2
from faker import Faker
#from app.models.domain import items, comments, users, profiles


print('Please fill the seeds file')

connection = psycopg2.connect(user="postgres",
                                  password="postgres",
                                  host="postgres",
                                  port="5432",
                                  database="anythink-market")
cursor = connection.cursor()

# Faker.seed(1234)
fake = Faker()
# TODO: user faker to generate 100 items
for i in range(100):
    user_insert_query = """ INSERT INTO users (username, email, salt) VALUES (%s,%s,%s)"""
    user_to_insert = (
    fake.unique.first_name(), fake.ascii_company_email(), fake.hexify(text='salting^^:^^:^^:^^:^^:^^'))
    cursor.execute(user_insert_query, user_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into users table")

# get seller_id from users table
query = f'SELECT id FROM users ;'
cursor.execute(query)
seller_id_list = cursor.fetchall()

for i in range(100):
    items_insert_query = """ INSERT INTO items (slug, title, description, body, image, seller_id) VALUES (%s,%s,%s,%s,%s,%s);
    """
    items_to_insert = (fake.unique.slug(), fake.catch_phrase(), fake.catch_phrase(), "", "", seller_id_list[i])
    cursor.execute(items_insert_query, items_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into items table")

# get item_id from items table
query = f'SELECT id FROM items ;'
cursor.execute(query)
item_id_list = cursor.fetchall()

for i in range(100):
    comments_insert_query = """ INSERT INTO comments (body, seller_id, item_id) VALUES (%s, %s,%s)"""
    comments_to_insert = (fake.sentence(nb_words=10), seller_id_list[i], item_id_list[i])
    cursor.execute(comments_insert_query, comments_to_insert)
    connection.commit()
    count = cursor.rowcount
    print(count, "Record inserted successfully into comments table")

if connection:
    cursor.close()
    connection.close()
    print("Postgre connection is closed")

# s.add(comment0)
# s.commit()







