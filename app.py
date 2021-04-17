from typing import final
from flask import Flask,render_template,request,redirect,g,session,url_for
import os 
import psycopg2

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'
users = []
users.append(User(id=1, username='admin', password='admin'))
users.append(User(id=2, username='bank', password='bank'))
users.append(User(id=3, username='kae', password='kae'))


con=psycopg2.connect(
    host='localhost',
    database='CP342',
    user='postgres',
    password='0957132960'
    )


app = Flask(__name__)
app.secret_key = "kaebank"

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user

@app.route('/')
def index():
    return render_template("home.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('adminpages'))

        return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/adminpages')
def adminpages():
    if not g.user:
        return redirect(url_for('login'))
    
    return render_template("admin.html")


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
            print("Error จ้า", error)
        finally : 
            con.commit()
            cur.close() 
            return redirect('/addstudent') 

    if request.method == 'GET' : 

        cur=con.cursor() 
        cur.execute("SELECT * FROM student ORDER BY std_id")
        result = cur.fetchall()

    return render_template("add.html",data = result)   


@app.route('/update/<string:id>',methods=["GET", "POST"])
def update(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor()
        stdselect = """SELECT * FROM student WHERE std_id = %s"""
        cur.execute(stdselect,(id,))
        update = cur.fetchall()
        return render_template("update.html",data = update)
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
        selectbor ="""SELECT * FROM borrower WHERE std_id = %s"""
        cur.execute(selectbor,(id,))
        x = cur.fetchall()
        for i in range(len(x)):
            delbor = """DELETE FROM borrowers_books WHERE borrower_id = %s"""
            cur.execute (delbor,(x[i][0],))
            con.commit()
        delborid = """DELETE FROM borrower WHERE std_id = %s """
        cur.execute(delborid,(id,))
        delstdid = """DELETE FROM student WHERE std_id = %s"""
        cur.execute(delstdid,(id,))
    except (Exception, psycopg2.Error) as error:
        print(error)
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
        return render_template("addauthor.html",data = result)

    
    

@app.route('/updateauthor/<string:id>',methods=["GET", "POST"])
def updateauthor(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        updateathor = """SELECT * FROM author WHERE author_id = %s ORDER BY author_id"""
        cur.execute(updateathor,id)
        update = cur.fetchall()
        return render_template("updateauthor.html",data = update)
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
        con.commit()
        cur.close()
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally :
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
        cur.execute("SELECT * FROM author")
        authorresult = cur.fetchall() 
        cur.execute("SELECT * FROM categorylist ORDER BY cat_id")
        categoryresult = cur.fetchall()
        return render_template("addbook.html",data = result,data2 = authorresult,data3 = categoryresult)

    if request.method == 'POST' :
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
        x = cur.fetchone()[0]   
        for i in range(category):
            goryinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
            cur.execute(goryinsert, (x,category[i]))
            con.commit()
        cur.close()
    return redirect('/addbook')
    

@app.route('/updatebook/<string:id>',methods=["GET", "POST"])
def updatebook(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        updateshow = """SELECT * FROM book WHERE book_id = %s ORDER BY book_id"""
        cur.execute(updateshow,id)
        update = cur.fetchall()
        updateauthor = """SELECT * FROM author NATURAL JOIN book WHERE book_id = %s """
        cur.execute(updateauthor,id)
        author = cur.fetchall()
        cur.execute("SELECT * FROM author book")
        authorupdate = cur.fetchall()
        return render_template("updatebook.html",data = update,data2 = author,data3 = authorupdate)

    if request.method == 'POST':
        try:
            cur=con.cursor() 
            bookid = request.form["book_id"] 
            title = request.form["title"] 
            author_id = request.form["author_id"] 
            floor = request.form["floor"] 
            publisher = request.form["year"] 
            stock = request.form["stock"]
            pg_update = """Update book set author_id = %s , booktitle = %s , floor = %s , book_publisher = %s , stock = %s where book_id = %s"""
            cur.execute(pg_update, (author_id,title,floor,publisher,stock,bookid))
            con.commit()
            cur.close()
        except (Exception, psycopg2.Error) as error:
            print(error)
        finally :       
            return redirect('/addbook')
        

@app.route('/deletebook/<string:id>')
def deletebook(id):
    if not g.user:
        return redirect(url_for('login'))
    try : 
        cur=con.cursor() 
        deletebook = """DELETE FROM book WHERE book_id= %s"""
        cur.execute(deletebook,id)
        con.commit()
        cur.close()
    except (Exception, psycopg2.Error) as error: 
        print(error)
    finally :  
        return  redirect('/addbook')

@app.route('/searchbooks')
def searchbooks():   
    cur=con.cursor() 
    searchbooks = """SELECT * FROM  book natural join author order by book_id;"""
    cur.execute(searchbooks)
    result = cur.fetchall()
    return render_template("searchbook.html",data = result)

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

    return render_template("addcategory.html",data = result)   

@app.route('/updatecategory/<string:id>',methods=["GET", "POST"])
def updatecategory(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        updatecategory = """SELECT * FROM categorylist WHERE cat_id = %s """
        cur.execute(updatecategory,id)
        update = cur.fetchall()
        return render_template("updatecategory.html",data = update)
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
        con.commit()
        cur.execute(catedel,id)        
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
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
            updatebook(books,x)
        except (Exception, psycopg2.Error) as error:     
            print(error)
        finally : 
            con.commit()
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

    return render_template("addborrower.html",data = result,data2 = stdresult,data3 =bookresult)   

def updatebook(books,x) :
    cur=con.cursor()
    for i in range(len(books)) :
        selbook = """SELECT * FROM book WHERE book_id = %s """
        cur.execute(selbook,books[i][0])
        book = cur.fetchall()[0][5]
        updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
        cur.execute(updatebook,((book-1),books[i][0]))
        con.commit()
        borrowbook = """insert into borrowers_books (book_id, borrower_id) values (%s,%s)"""
        cur.execute(borrowbook,(books[i][0],x))
        con.commit()


@app.route('/updateborrower/<string:id>',methods=["GET", "POST"])
def updateborrower(id):
    if not g.user:
        return redirect(url_for('login'))
    if request.method == 'GET':
        cur=con.cursor() 
        cur.execute("SELECT * FROM student WHERE std_id ="+id+"")
        update = cur.fetchall()
        return render_template("update.html",data = update)
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
        selborrower = """SELECT * FROM borrowers_books WHERE borrower_id = %s"""
        cur.execute(selborrower,(id,))
        book = cur.fetchall()
        for i in range(len(book)) :
            selbook = """SELECT * FROM book WHERE book_id = %s"""
            cur.execute(selbook,(book[i][0],))
            x = cur.fetchall()[0][5]
            delstd2 = """DELETE FROM borrower WHERE borrower_id = %s returning borrower_id"""
            cur.execute(delstd2,(id,))
            con.commit()
            updatebook = """UPDATE book SET stock = %s WHERE book_id = %s """
            cur.execute(updatebook,((x+1),book))
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        con.commit()
        cur.close()
        return  redirect('/addborrowers')
app.run(debug=True,use_reloader=True)

