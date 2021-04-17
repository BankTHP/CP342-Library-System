import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342',
    user='postgres',
    password='0957132960'
    )

cur=con.cursor()
std_id = 62102010169
author_id = 1
booktitle = "database test เพิ่มค่า"
floor = '3'
publisher = '2021-04-01'
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
category= '1-2-3-4'.split('-')
statusBook = 0 
stock = 10
books = '34-36'.split('-')
insertbook = """INSERT INTO book (author_id,booktitle,floor,book_publisher,stock) values (%s,%s,%s,%s,%s) RETURNING book_id """
cur.execute(insertbook, (author_id,booktitle,floor,publisher,stock))
con.commit()
x = cur.fetchone()[0]   
for i in range():
    goryinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
    cur.execute(goryinsert, (x,category[i]))
    con.commit()

