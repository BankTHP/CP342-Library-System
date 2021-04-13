id = 62102010169
name = "ธนพัฒน์"
lastname = "เอี่ยมประเสริฐ"
major = "วิทยาการคอมพิวเตอร์"
year = "2"
pg_del = """"SELECT * FROM book WHERE author_firstname LIKE '%{}%'OR author_lastname LIKE '%{}%""".format(name,lastname)
print(pg_del)