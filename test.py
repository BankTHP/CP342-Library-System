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
id = 10
delstd = """DELETE FROM borrowers_books WHERE borrower_id = %s """
cur.execute(delstd,id)
con.commit()
delstd2 = """DELETE FROM borrower WHERE borrower_id = %s """
cur.execute(delstd2,id)
con.commit()

    


