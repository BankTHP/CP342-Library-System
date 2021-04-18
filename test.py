import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342-FINALPROJECT',
    user='postgres',
    password='0957132960'
    )

cur=con.cursor()
std_id = 62102010169
author_id = 1
booktitle = "database test เพิ่มค่า"
floor = '3'
book_id = 3
publisher = '2021-04-01'
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
book_id= '3-8-9-12'.split('-')
statusBook = 0 
stock = 10
books = '34-36'.split('-')
borrower_id = 3
# insertbook = """ SELECT cat_id FROM  categorylist WHERE cat_id NOT IN (SELECT cat_id FROM category WHERE book_id = 4)"""
# cur.execute(insertbook)
# x = cur.fetchall()
print(range(len(book_id)-1))
for i in range(len(book_id)) :
    selbook = """SELECT stock FROM book WHERE book_id = %s"""
    cur.execute(selbook,book_id[i][0])
    book = cur.fetchall()
    print(book)
    # updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
    # cur.execute(updatebook,((book-1),books[i][0]))
    # con.commit()
    # borrowbook = """insert into borrowers_books (book_id, borrower_id) values (%s,%s)"""
    # cur.execute(borrowbook,(books[i][0],borrower_id))
    # con.commit()