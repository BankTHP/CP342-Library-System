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
book_id = 4
publisher = '2021-04-01'
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
category= ''.split('-')
statusBook = 0 
stock = 10
books = '34-36'.split('-')
insertbook = """ SELECT cat_id FROM  categorylist WHERE cat_id NOT IN (SELECT cat_id FROM category WHERE book_id = 4)"""
cur.execute(insertbook)
x = cur.fetchall()
countrow = """select cat_id from category WHERE book_id = 1"""
cur.execute(countrow)
xp = cur.fetchall()
# print(x)
# print(type(category[0]))
# print(xp)
# print(x  in category)
# if xp > len(x):
#     print("yes")
#     # for  i in range(len(x)) :
# else :
#     print("no")
# print(len(x)+xp[0][0])
# for i in range(len(x)+xp[0][0]):
# print("เช็คว่าอันไหนไม่มี",list(x))
test = list()
for i in range(len(xp)):
    test.append(str(xp[i][0]))
print("ที่ js ส่งมา ",category)
print("ค่าของหนังสือ",test)
if len(category) > len(test):#insert 
    x = list(set(category)- set(test)) 
    for i in x :
        xinsert = """INSERT INTO category values(%s,%s)"""
        cur.execute(xinsert,(x[0],book_id))
        con.commit()
elif len(category) < len(test): #ต้องdel ออก
    x  = list(set(test)- set(category))
    for i in x :
        xtest = """DELETE FROM category WHERE cat_id = %s AND book_id = %s"""
        cur.execute(xtest,(x[0],book_id))
        con.commit()

elif len(category) == len(test):
    print("==")
# x1 = list(set(category)- set(test)) 
# print(x1)


