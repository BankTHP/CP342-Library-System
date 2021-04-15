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
for i in range(len(books)) :
    print(books[1])
id = 9
addborrower = """DELETE FROM borrower where borrower_id = %s """
cur.execute(addborrower,str(id))
test = """ALTER SEQUENCE author_author_id_seq RESTART WITH {}""".format(id-1)
cur.execute(test)
con.commit()


    


