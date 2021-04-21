import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342-FINALPROJECT',
    user='postgres',
    password='0957132960'
    )

cur=con.cursor()
std_id = 6210201010168
author_id = 1
booktitle = "database test เพิ่มค่า"
floor = '3'
book_id = 3
publisher = '2021-04-01'
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
book_id= '13-14-3-8-9'.split('-')
statusBook = 0 
stock = 10
books = '34-36'.split('-')
borrower_id = 34

# insertbook = """ SELECT cat_id FROM  categorylist WHERE cat_id NOT IN (SELECT cat_id FROM category WHERE book_id = 4)"""
# cur.execute(insertbook)
# x = cur.fetchall()
cur=con.cursor() 
# selborrower = """SELECT * FROM borrowers_books natural join book WHERE borrower_id = %s"""
# cur.execute(selborrower,(borrower_id,))
# book = cur.fetchall()

# for i in range(len(book)):
#     updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
#     cur.execute(updatebook,((book[i][6]+1),book[i][0]))
#     con.commit()
# delstd2 = """DELETE FROM borrower WHERE borrower_id = %s returning borrower_id"""
# cur.execute(delstd2,(borrower_id,))
# con.commit()
SQL  = """SELECT book_id,ARRAY_TO_STRING(ARRAY_AGG(categorylist.cat_id), ',') as หมวดหมู่หนังสือ FROM book NATURAL JOIN category NATURAL JOIN categorylist GROUP BY book_id"""
cur.execute(SQL)
