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
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
statusBook = 0 
books = '34-36'.split('-')
id = 16
delbook = """DELETE FROM borrowers_books WHERE borrower_id = %s RETURNING book_id"""
cur.execute(delbook,(id,))
book = cur.fetchall()
for i  in range(len(books)+1):
    selbook = "SELECT * FROM book WHERE book_id = %s "
    cur.execute(selbook,(book[i][0],))
    stock = cur.fetchall()[0][5]
    updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
    cur.execute(updatebook,((stock+1),book[i][0]))
    con.commit()

