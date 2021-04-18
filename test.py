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
book_id = 6
publisher = '2021-04-01'
borrowerdate = '2021-04-01'
returndate = '2021-04-02'
category= '1-2-3-4-5'.split('-')
statusBook = 0 
stock = 10
books = '34-36'.split('-')
# insertbook = """ SELECT cat_id FROM  categorylist WHERE cat_id NOT IN (SELECT cat_id FROM category WHERE book_id = 4)"""
# cur.execute(insertbook)
# x = cur.fetchall()
# print(x)
countrow = """select cat_id from category WHERE book_id = 6"""
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
js = list()
for i in range(len(xp)):
    js.append(str(xp[i][0]))
check = list()
for i in range(len(js)) :
    if(js[i] in category) :
        category.remove(js[i]) # เอาที่ต่างกัน
    else :
        check.append(str(js[i]))
for i in range(len(check)):
    delid = """DELETE FROM category WHERE book_id = %s AND cat_id = %s """
    cur.execute(delid,(book_id,check[i]))
    con.commit()
for i in range(len(category)):
    insertid = """INSERT INTO category (book_id,cat_id) VALUES (%s,%s) """
    cur.execute(insertid,(book_id,category[i]))
    con.commit()
