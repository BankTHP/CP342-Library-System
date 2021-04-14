import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342',
    user='postgres',
    password='0957132960'
    )

cur=con.cursor()

author_id = 1
booktitle = "database"
floor = '3'
book_publisher = '2021-04-01'
statusBook = 0 
info = '1-2-3'.split('-')
pginsert = """INSERT INTO book (author_id,booktitle,floor,book_publisher,"BookStatus") values (%s,%s,%s,%s,%s) RETURNING book_id """
cur.execute(pginsert, (author_id,booktitle,floor,book_publisher,statusBook))
con.commit()
x = cur.fetchone()[0]
for i in range(1,len(info)+1) :
    goryinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
    cur.execute(goryinsert, (x,i))
    con.commit()

    


