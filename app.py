from typing import final
from flask import Flask,render_template,request,redirect,g,session,url_for,flash
import os 
import psycopg2




con=psycopg2.connect(
    host='localhost',
    database='CP342-FINALPROJECT',
    user='postgres',
    password='0957132960'
    )


app = Flask(__name__)
app.secret_key = os.urandom(24)


@app.route('/')
def index():
    return render_template("home.html",title = "WELCOME TO BK PROJECT")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        session.pop('user',None)
        
        if request.form['password'] == 'admin' :
            session['user']  = request.form["username"]
            return redirect(url_for('adminpages'))
        else :
            errorflash = flash("โปรดตรวจสอบความถูกต้อง", "info")
            return render_template("login.html",error = errorflash)


    return render_template("login.html",title = "LOGIN")

@app.before_request
def before_login():
    g.user = None 
    if 'user' in session :
        g.user = session['user']
@app.route('/logout')
def logout():
   session.pop('user', None)
   return redirect(url_for('login'))

@app.route('/adminpages')
def adminpages():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template("admin.html",title = "หน้าจัดการระบบ")


@app.route('/addstudent', methods=["POST","GET"])
def home():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST' :
        try : 
            cur=con.cursor()
            id = request.form["s_id"]            
            name = request.form["fname"]          
            lastname = request.form["lname"]        
            major = request.form["major"]           
            year = request.form["year"]
            addstudent = """insert into student values (%s,%s,%s,%s,%s)"""
            cur.execute(addstudent,(id,name,lastname,major,year))
        except (Exception, psycopg2.Error) as error:     
            flash("นิสิตคนนี้ยังมีชื่อในระบบแล้ว", "info")
        finally : 
            con.commit()
            cur.close() 
            return redirect('/addstudent') 

    if request.method == 'GET' : 

        cur=con.cursor() 
        cur.execute("SELECT * FROM student ORDER BY std_id")
        result = cur.fetchall()

    return render_template("add.html",data = result,title = "CRUD STUDENT")   


@app.route('/update/<string:id>',methods=["GET", "POST"])
def update(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor()
        stdselect = """SELECT * FROM student WHERE std_id = %s"""
        cur.execute(stdselect,(id,))
        update = cur.fetchall()
        return render_template("update.html",data = update,title = "แก้ไขข้อมูลนิสิต")
    if request.method == 'POST':
        try : 
            cur=con.cursor()
            id = request.form["std_id"] 
            name = request.form["std_firstname"] 
            lname = request.form["std_lastname"] 
            major = request.form["major"]
            year = request.form["Year"]
            pg_update = """Update student set std_firstname = %s , std_lastname = %s ,std_major = %s ,std_year = %s where std_id = %s"""
            cur.execute(pg_update, (name,lname,major,year, id))
        except (Exception, psycopg2.Error) as error:
            print("Error selecting data from table book", error)
            return redirect('/addstudent')
        finally:
            con.commit()
            cur.close()
            return redirect('/addstudent')

@app.route('/delete/<string:id>')
def delete(id):
    if not g.user:
        return redirect(url_for('login'))
    try :  
        cur=con.cursor()
        delstdid = """DELETE FROM student WHERE std_id = %s"""
        cur.execute(delstdid,(id,))
    except (Exception, psycopg2.Error) as error:
        flash("นิสิตคนนี้ยังมีชื่อในระบบ borrower ", "info")
    finally:
        con.commit()
        cur.close()
        return  redirect('/addstudent')


##############################################################################################################################AUTHOR

@app.route('/addauthor', methods=["POST","GET"])
def addauthor():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST' :
        cur=con.cursor() 
        name = request.form["name"] 
        lastname = request.form["lname"] 
        cur.execute('insert into author (author_firstname,author_lastname) values (%s,%s)',(name,lastname))
        con.commit()
        cur.close()
        return redirect('/addauthor')
    if request.method == 'GET' :
        cur=con.cursor() 
        cur.execute("SELECT * FROM author order by author_id ")
        result = cur.fetchall()
        return render_template("addauthor.html",data = result,title = "CRUD AUTHOR")

    
    

@app.route('/updateauthor/<string:id>',methods=["GET", "POST"])
def updateauthor(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        updateathor = """SELECT * FROM author WHERE author_id = %s ORDER BY author_id"""
        cur.execute(updateathor,id)
        update = cur.fetchall()
        return render_template("updateauthor.html",data = update,title = "แก้ไขข้อมูลนักแต่ง")
    if request.method == 'POST':
        id = request.form["id"] 
        name = request.form["firstname"] 
        lname = request.form["lastname"] 
        try : 
            cur=con.cursor() 
            pg_update = """Update author set author_firstname = %s , author_lastname = %s  where author_id = %s"""
            cur.execute(pg_update, (name,lname,id))
            con.commit()
            cur.close()
        except (Exception, psycopg2.Error) as error: 
            print(error)
        finally : 
            return redirect('/addauthor')
       
        

@app.route('/deleteauthor/<string:id>')
def deleteauthor(id):
    if not g.user:
        return redirect(url_for('login'))
    try :
        cur=con.cursor() 
        delauthor = """DELETE FROM author WHERE author_id= %s"""
        cur.execute(delauthor,id)  
    except (Exception, psycopg2.Error) as error:
        flash("นักแต่งคนนี้ยังมีหนังสืออยู่ในระบบ", "info")
    finally :
        con.commit()
        cur.close()
        return redirect('/addauthor')

##############################################################################################################################

@app.route('/addbook', methods=["POST","GET"])
def addbook(): 
    if not g.user:
        return redirect(url_for('login'))    
    if request.method == 'GET' :
        cur=con.cursor() 
        cur.execute("SELECT * FROM author NATURAL JOIN book ORDER BY book_id") 
        result = cur.fetchall()
        cur.execute("SELECT * FROM author order by author_id")
        authorresult = cur.fetchall() 
        cur.execute("SELECT * FROM categorylist ORDER BY cat_id")
        categoryresult = cur.fetchall()
        return render_template("addbook.html",data = result,data2 = authorresult,data3 = categoryresult,title = "CRUD BOOK")
        

    if request.method == 'POST' : 
        try: 
            cur=con.cursor() 
            author_id = request.form["author_id"]
            title = request.form["title"] 
            floor = request.form["floor"]
            publisher = request.form["publisher"]
            category = request.form["c_id"].split("-")
            stock = request.form["stock"]
            insertbook = """INSERT INTO book (author_id,booktitle,floor,book_publisher,stock) values (%s,%s,%s,%s,%s) RETURNING book_id """
            cur.execute(insertbook, (author_id,title,floor,publisher,stock))
            con.commit()
            x= cur.fetchall()[0][0]
            for i in range(len(category)):
                cateinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
                cur.execute(cateinsert, (x,category[i]))
            con.commit()
        except (Exception, psycopg2.Error) as error:
            flash("เพิ่มหนังสือไม่สำเร็จ")
        finally:
            return redirect('addbook')
    return redirect('/addbook')

def adddbook() :
    try: 
        cur=con.cursor() 
        author_id = request.form["author_id"]
        title = request.form["title"] 
        floor = request.form["floor"]
        publisher = request.form["publisher"]
        category = request.form["c_id"].split("-")
        stock = request.form["stock"]
        insertbook = """INSERT INTO book (author_id,booktitle,floor,book_publisher,stock) values (%s,%s,%s,%s,%s) RETURNING book_id """
        cur.execute(insertbook, (author_id,title,floor,publisher,stock))
        con.commit()
        x= cur.fetchall()[0][0]
        for i in range(len(category)):
            cateinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
            cur.execute(cateinsert, (x,category[i]))
            con.commit()
    except (Exception, psycopg2.Error) as error:
        flash("เพิ่มหนังสือไม่สำเร็จ")

@app.route('/updatebook/<string:id>',methods=["GET", "POST"])
def updatebook(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':

        cur=con.cursor() 
        updateshow = """SELECT * FROM book NATURAL JOIN category NATURAL JOIN categorylist  WHERE book_id = %s ORDER BY book_id"""
        cur.execute(updateshow,(id,))
        update = cur.fetchall()


        updateauthor = """SELECT * FROM author NATURAL JOIN book WHERE book_id = %s """
        cur.execute(updateauthor,(id,))
        author = cur.fetchall()


        cur.execute("SELECT * FROM author book")
        authorupdate = cur.fetchall()
        updatecategory = """SELECT * FROM categorylist order by cat_id"""
        cur.execute(updatecategory)
        category = cur.fetchall()


        notselect = list()
        choicefromdb = list()
        for i in range(len(update)) :
            choicefromdb.append(update[i][0])


        for i in range(len(category)) : 
            if category[i][0] not in choicefromdb :
                notselect.append(category[i])

        cur.close()
        return render_template("updatebook.html",data = update,data2 = author,data3 = authorupdate,data4 = notselect,title = "แก้ไขข้อมูลหนังสือ")

    if request.method == 'POST':
        try:
            cur=con.cursor() 
            bookid = request.form["book_id"] 
            title = request.form["title"] 
            author_id = request.form["author_id"] 
            floor = request.form["floor"] 
            publisher = request.form["publisher"] 
            stock = request.form["stock"]
            category = request.form["c_id"].split('-')
            
            pg_update = """Update book set author_id = %s , booktitle = %s , floor = %s , book_publisher = %s , stock = %s where book_id = %s"""
            cur.execute(pg_update, (author_id,title,floor,publisher,stock,bookid))            
            con.commit()
            selbook = """select cat_id from category WHERE book_id = %s"""
            cur.execute(selbook,(bookid,))
            xp = cur.fetchall()
            js = list()
            categorytest = list(dict.fromkeys(category))
            for i in range(len(xp)):
                js.append(str(xp[i][0]))
            check = list()
            for i in range(len(js)) :
                if(js[i] in categorytest) :
                    categorytest.remove(js[i])
                else :
                    check.append(str(js[i]))
            for j in range(len(check)):
                delid = """DELETE FROM category WHERE book_id = %s AND cat_id = %s """
                cur.execute(delid,(bookid,check[j]))        
            for k in range(len(categorytest)):
                insertid = """INSERT INTO category (book_id,cat_id) VALUES (%s,%s) """
                cur.execute(insertid,(bookid,categorytest[k]))

        except (Exception, psycopg2.Error) as error:
            print(error)
        finally : 
            con.commit() 
            cur.close()  
            return redirect('/addbook')
        

@app.route('/deletebook/<string:id>')
def deletebook(id):
    if not g.user:
        return redirect(url_for('login'))
    try : 
        cur=con.cursor() 
        deletebook = """DELETE FROM book WHERE book_id= %s"""
        cur.execute(deletebook,(id,))
    except (Exception, psycopg2.Error) as error: 
        flash("ERROR ยังมีหนังสืออยู่ในระบบborrower", "info")
    finally :  
        con.commit()
        cur.close()
        return  redirect('/addbook')

@app.route('/searchborrower', methods=["POST","GET"])
def searchborrower():  
    if request.method == 'POST':
        cur =con.cursor()
        try :
            x = request.form["stdid"]
            selborrower = """SELECT borrower_id,ARRAY_TO_STRING(ARRAY_AGG(book.booktitle), ', '),returndate FROM borrower NATURAL JOIN borrowers_books 
            NATURAL JOIN book WHERE std_id = %s GROUP BY borrower_id,returndate """
            cur.execute(selborrower,(x,))
            result = cur.fetchall()
            if (result == []) :
                test = flash("ไม่พบข้อมูล")
                return render_template("searchborrower.html",data = test)
            else :
                return render_template("searchborrower.html",data = result)

        except (Exception, psycopg2.Error) as error:
            flash("ไม่พบข้อมูล")
            return redirect('/searchborrower')
        finally : 
            con.commit()
    return render_template("searchborrower.html",title = "ตรวจสอบผู้ยืม")
    

@app.route('/searchbooks')

def searchbooks():   

    cur=con.cursor() 

    searchbooks = """SELECT booktitle,ARRAY_TO_STRING(ARRAY_AGG(categorylist.des), ' , ') as หมวดหมู่หนังสือ,author_firstname,author_lastname,stock 
    FROM book NATURAL JOIN category NATURAL JOIN categorylist NATURAL JOIN author  GROUP BY booktitle,author_firstname,author_lastname,stock;"""

    cur.execute(searchbooks)
    result = cur.fetchall()
    return render_template("searchbook.html",data = result,title = "ค้นหาหนังสือ")

@app.route('/addcategory', methods=["POST","GET"])
def addcaterory():
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'POST' :
        try : 
            cur=con.cursor() 
            name = request.form["name"] 
            des = request.form["des"] 
            addstudent = """insert into categorylist (categoryname,des) values (%s,%s)"""
            cur.execute(addstudent,(name,des))
            con.commit()
            cur.close()
        except (Exception, psycopg2.Error) as error:     
            print(error)
        finally : 
            return redirect('/addcategory') 
    

    if request.method == 'GET' : 
        cur=con.cursor() 
        cur.execute("SELECT * FROM categorylist")

        result = cur.fetchall()

    return render_template("addcategory.html",data = result,title = "CRUD CATEGORY")   

@app.route('/updatecategory/<string:id>',methods=["GET", "POST"])
def updatecategory(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        updatecategory = """SELECT * FROM categorylist WHERE cat_id = %s """
        cur.execute(updatecategory,id)
        update = cur.fetchall()
        return render_template("updatecategory.html",data = update,title = "หน้าแก้ไขข้อมูล Category")
    if request.method == 'POST':
        try : 
            cur=con.cursor() 
            name= request.form["name"] 
            des = request.form["des"] 
            pg_update = """Update categorylist set categoryname = %s , des = %s where cat_id = %s"""
            cur.execute(pg_update, (name,des,id))
            con.commit()
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally:
            cur.close()
            return redirect('/addcategory')

@app.route('/deletecategory/<string:id>')
def deletecategory(id):
    if not g.user:
        return redirect(url_for('login'))
    try :
        cur=con.cursor() 
        catedel = """DELETE FROM categorylist WHERE cat_id = %s"""        
        cur.execute(catedel,id)        
    except (Exception, psycopg2.Error) as error:
        flash("ERROR หมวดหมู่ยังเป็นประเภทของหนังสืออยู่!", "info")
    finally:
        con.commit()
        cur.close()
        return  redirect('/addcategory')

@app.route('/addborrowers', methods=["POST","GET"])
def addborrowers():
    if not g.user:
        return redirect(url_for('login'))
    
    if request.method == 'POST' :
        try : 
            cur=con.cursor() 
            std_id = request.form["std_id"]        
            borrowerdate = request.form["borrowerdate"]             
            returndate = request.form["returndate"]  
            books = request.form["book"].split('-')
            addborrower = """insert into borrower (std_id,returndate,borrowerdate) values (%s,%s,%s) RETURNING borrower_id"""
            cur.execute(addborrower,(std_id,borrowerdate,returndate))
            x = cur.fetchone()[0]
            for i in range(len(books)) :
                selbook = """SELECT * FROM book WHERE book_id = %s"""
                cur.execute(selbook,(books[i],))
                book = cur.fetchall()[0][5] #stock
                if book == 0 :  
                    con.rollback()
                else :
                    updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
                    cur.execute(updatebook,(book-1,(books[i])))
                    borrowbook = """insert into borrowers_books (book_id, borrower_id) values (%s,%s)"""
                    cur.execute(borrowbook,(books[i],x))
                    con.commit()
        except (Exception, psycopg2.Error) as error:     
            flash('เกิดข้อผิดพลาดทางระบบ')
            print(error)            
        finally : 
            cur.close()
            return redirect('/addborrowers') 
    if request.method == 'GET' :
        try:
            cur=con.cursor() 
            cur.execute("SELECT * FROM borrower ORDER BY borrower_id")
            result = cur.fetchall()
            cur.execute("SELECT * FROM student ORDER by std_id")
            stdresult = cur.fetchall()
            cur.execute("SELECT * FROM book NATURAL JOIN author ORDER by book_id")
            bookresult = cur.fetchall()
        except (Exception, psycopg2.Error) as error:
            print(error)
            return redirect('/addborrowers')

    return render_template("addborrower.html",data = result,data2 = stdresult,data3 =bookresult,title = "CRUD BORROWER")   


@app.route('/updateborrower/<string:id>',methods=["GET", "POST"])
def updateborrower(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        selborrower = """SELECT * FROM borrower NATURAL JOIN student NATURAL JOIN borrowers_books natural join book WHERE borrower_id = %s """
        cur.execute(selborrower,(id,))
        update = cur.fetchall()       



        selborrower1 = """SELECT * FROM book"""
        cur.execute(selborrower1)
        choice= cur.fetchall()


        notselect = list()
        choicefromdb = list()
        for i in range(len(update)) :
            choicefromdb.append(update[i][0])


        for i in range(len(choice)) : 
            if choice[i][0] not in choicefromdb :
                notselect.append(choice[i])

        
        return render_template("updateborrower.html",data = update,data2 = notselect,title = "แก้ไขข้อมูลผู้ยืม")

    if request.method == 'POST':
        try : 
            cur=con.cursor() 
            borrower_id = request.form['borrower_id']
            book_id = request.form["book_id"].split('-')
            borrowerdate = request.form["borrowerdate"]
            returndate = request.form["returndate"]
            updateborrower = """UPDATE borrower SET returndate=%s, borrowerdate= %s WHERE borrower_id = %s;"""
            cur.execute(updateborrower,(returndate,borrowerdate,borrower_id))
            book = """SELECT * FROM borrowers_books where borrower_id = %s"""
            cur.execute(book,(borrower_id,))
            xp = cur.fetchall()
            js = list()
            categorytest = list(dict.fromkeys(book_id))    
            for i in range(len(xp)):
                js.append(str(xp[i][0]))
            check = list()
            for i in range(len(js)) :
                if(js[i] in categorytest) :
                    categorytest.remove(js[i]) # เอาที่ต่างกัน
                else :
                    check.append(str(js[i]))
            for i in range(len(check)):
                delid = """DELETE FROM borrowers_books WHERE borrower_id = %s AND book_id = %s """
                cur.execute(delid,(borrower_id,check[i]))
                selbook = """SELECT stock FROM book WHERE book_id = %s"""
                cur.execute(selbook,(check[i],))
                book = cur.fetchall()[0][0]
                updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
                cur.execute(updatebook,(book+1,(check[i])))
            for i in range(len(categorytest)):
                insertid = """INSERT INTO borrowers_books (book_id,borrower_id) VALUES (%s,%s) """
                cur.execute(insertid,(categorytest[i],borrower_id))
                selbook = """SELECT stock FROM book WHERE book_id = %s"""
                cur.execute(selbook,(categorytest[i],))
                book = cur.fetchall()[0][0]
                updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
                cur.execute(updatebook,(book-1,(categorytest[i])))
        except (Exception, psycopg2.Error) as error:
            print(error)
            return redirect('/addborrowers')
        finally:
            con.commit()
            cur.close()
            return redirect('/addborrowers')

@app.route('/deleteborrower/<string:id>')
def deleteborrower(id):
    if not g.user:
        return redirect(url_for('login'))
    try :
        cur=con.cursor() 
        selborrower = """SELECT * FROM borrowers_books natural join book WHERE borrower_id = %s"""  #53
        cur.execute(selborrower,(id,))
        book = cur.fetchall()
        for i in range(len(book)):
            updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
            cur.execute(updatebook,((book[i][6]+1),book[i][0]))
            con.commit()
            delstd2 = """DELETE FROM borrower WHERE borrower_id = %s returning borrower_id"""
            cur.execute(delstd2,(id,))
    except (Exception, psycopg2.Error) as error:
        flash("ERROR! ", "info")
    finally:
        con.commit()
        cur.close()
        return  redirect('/addborrowers')
app.run(debug=True,use_reloader=True)

