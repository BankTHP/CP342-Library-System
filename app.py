from typing import final
from flask import Flask,render_template,request,redirect,g,session,url_for
import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342',
    user='postgres',
    password='0957132960'
    )

cur=con.cursor()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("home.html")

@app.route('/adminpage')
def admin():
    return render_template("admin.html")

@app.route('/addstudent', methods=["POST","GET"])
def home():
    if request.method == 'POST' :
        try : 
            id = request.form["s_id"]            
            name = request.form["fname"]          
            lastname = request.form["lname"]        
            major = request.form["major"]           
            year = request.form["year"]
            addstudent = """insert into student values (%s,%s,%s,%s,%s)"""
            cur.execute(addstudent,(id,name,lastname,major,year))
        except (Exception, psycopg2.Error) as error:     
            print("Error จ้า", error)
            return redirect('/addstudent')
        finally : 
            con.commit() 
            return redirect('/addstudent') 

    if request.method == 'GET' : 

        cur.execute("SELECT * FROM student ORDER BY std_id")
        result = cur.fetchall()

    return render_template("add.html",data = result)   


@app.route('/update/<string:id>',methods=["GET", "POST"])
def update(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM student WHERE std_id ="+id+"")
        update = cur.fetchall()
        return render_template("update.html",data = update)
    if request.method == 'POST':
        try : 
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
            return redirect('/addstudent')

@app.route('/delete/<string:id>')
def delete(id):
    try :
        cur.execute("DELETE FROM student WHERE std_id="+id+"")
    except (Exception, psycopg2.Error) as error:
        print("Error selecting data from table book", error)
    finally:
        con.commit()
        return  redirect('/addstudent')


##############################################################################################################################AUTHOR

@app.route('/addauthor', methods=["POST","GET"])
def addauthor():
    if request.method == 'POST' :
        insertauthordb()
        return redirect('/addauthor')
    if request.method == 'GET' :
        cur.execute("SELECT * FROM author order by author_id ")
        result = cur.fetchall()
        return render_template("addauthor.html",data = result)

def insertauthordb() :
    name = request.form["name"] 
    lastname = request.form["lname"] 
    cur.execute('insert into author (author_firstname,author_lastname) values (%s,%s)',(name,lastname))
    con.commit()

@app.route('/updateauthor/<string:id>',methods=["GET", "POST"])
def updateauthor(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM author WHERE author_id ="+id+"ORDER BY author_id")
        update = cur.fetchall()
        return render_template("updateauthor.html",data = update)
    if request.method == 'POST':
        id = request.form["id"] 
        name = request.form["firstname"] 
        lname = request.form["lastname"] 
        try : 
            pg_update = """Update author set author_firstname = %s , author_lastname = %s  where author_id = %s"""
            cur.execute(pg_update, (name,lname,id))
            con.commit()
            return redirect('/addauthor')
        except (Exception, psycopg2.Error) as error: 
            print("Error selecting data from table book", error)
            return redirect('/addauthor')
       
        

@app.route('/deleteauthor/<string:id>')
def deleteauthor(id):
    try :
        cur.execute("DELETE FROM author WHERE author_id="+id+"")
    except (Exception, psycopg2.Error) as error:
        print("Error selecting data from table book", error)
    finally :
        con.commit()
        return redirect('/addauthor')

##############################################################################################################################

@app.route('/addbook', methods=["POST","GET"])
def addbook(): 
    
    if request.method == 'GET' :
        cur.execute("SELECT * FROM author NATURAL JOIN book ORDER BY book_id") 
        result = cur.fetchall()
        cur.execute("SELECT * FROM author")
        authorresult = cur.fetchall() 
        cur.execute("SELECT * FROM categorylist ORDER BY cat_id")
        categoryresult = cur.fetchall()
        return render_template("addbook.html",data = result,data2 = authorresult,data3 = categoryresult)

    if request.method == 'POST' :
        author_id = request.form["author_id"]
        title = request.form["title"] 
        floor = request.form["floor"]
        publisher = request.form["publisher"]
        category = request.form["c_id"].split("-")
    
        insertbook = """INSERT INTO book (author_id,booktitle,floor,book_publisher,"BookStatus") values (%s,%s,%s,%s,%s) RETURNING book_id """
        cur.execute(insertbook, (author_id,title,floor,publisher,0))
        con.commit()
        x = cur.fetchone()[0]   
        for i in range(1,len(category)+1) :
            goryinsert = """INSERT INTO category (book_id, cat_id) values (%s,%s) """
            cur.execute(goryinsert, (x,i))
        con.commit()
        return redirect('/addbook')
    

@app.route('/updatebook/<string:id>',methods=["GET", "POST"])
def updatebook(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM book WHERE book_id ="+id+"ORDER BY book_id")
        update = cur.fetchall()
        cur.execute("SELECT * FROM author NATURAL JOIN book WHERE book_id = "+id+"")
        author = cur.fetchall()
        cur.execute("SELECT * FROM author book")
        authorupdate = cur.fetchall()
        return render_template("updatebook.html",data = update,data2 = author,data3 = authorupdate)

    if request.method == 'POST':
        try:
            bookid = request.form["book_id"] 
            title = request.form["title"] 
            author_id = request.form["author_id"] 
            floor = request.form["floor"] 
            publisher = request.form["year"] 
            pg_update = """Update book set author_id = %s , booktitle = %s , floor = %s , book_publisher = %s where book_id = %s"""
            cur.execute(pg_update, (author_id,title,floor,publisher,bookid))
        except (Exception, psycopg2.Error) as error:
            print("Error selecting data from table book", error)
        finally :
            con.commit()
            return redirect('/addbook')
        

@app.route('/deletebook/<string:id>')
def deletebook(id):
    try : 
        print(id)
        cur.execute("DELETE FROM book WHERE book_id="+id+"")
    except (Exception, psycopg2.Error) as error: 
        print("Error selecting data from table book", error)
        return redirect('/addbook')
    finally : 
        con.commit()
        return  redirect('/addbook')

@app.route('/searchbooks')
def searchbooks():   
    searchbooks = """SELECT * FROM category natural join categorylist natural join book natural join author;"""
    cur.execute(searchbooks)
    result = cur.fetchall()
    return render_template("searchbook.html",data = result)

@app.route('/addcategory', methods=["POST","GET"])
def addcaterory():
    if request.method == 'POST' :
        try : 
            name = request.form["name"] 
            des = request.form["des"] 
            addstudent = """insert into categorylist (categoryname,des) values (%s,%s)"""
            cur.execute(addstudent,(name,des))
            print("สำเร็จ") 
        except (Exception, psycopg2.Error) as error:     
            print("Error จ้า", error)
            return redirect('/addcategory')
        finally : 
            con.commit() 
            return redirect('/addcategory') 

    if request.method == 'GET' : 

        cur.execute("SELECT * FROM categorylist")

        result = cur.fetchall()

    return render_template("addcategory.html",data = result)   

@app.route('/updatecategory/<string:id>',methods=["GET", "POST"])
def updatecategory(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM categorylist WHERE cat_id ="+id+"")
        update = cur.fetchall()
        return render_template("updatecategory.html",data = update)
    if request.method == 'POST':
        try : 
            name= request.form["name"] 
            des = request.form["des"] 
            pg_update = """Update categorylist set categoryname = %s , des = %s where cat_id = %s"""
            cur.execute(pg_update, (name,des,id))
        except (Exception, psycopg2.Error) as error:
            print("Error selecting data from table book", error)
            return redirect('/addcategory')
        finally:
            con.commit()
            return redirect('/addcategory')

@app.route('/deletecategory/<string:id>')
def deletecategory(id):
    try :
        catedel = """DELETE FROM categorylist WHERE cat_id = %s"""
        cur.execute(catedel,id)
        
    except (Exception, psycopg2.Error) as error:
        print(error)
    finally:
        con.commit()
        return  redirect('/addcategory')

@app.route('/addborrowers', methods=["POST","GET"])
def addborrowers():
    if request.method == 'POST' :
        try : 
            std_id = request.form["std_id"]        
            borrowerdate = request.form["borrowerdate"]             
            returndate = request.form["returndate"]  
            books = request.form["book"].split('-')
            addborrower = """insert into borrower (std_id,returndate,borrowerdate) values (%s,%s,%s) RETURNING borrower_id"""
            cur.execute(addborrower,(std_id,borrowerdate,returndate))
            con.commit()
            x = cur.fetchone()[0] 
            updatebook(books,x)

        except (Exception, psycopg2.Error) as error:     
            print("Error จ้า", error)
            return redirect('/addborrowers')
        finally : 
            con.commit() 
            return redirect('/addborrowers') 

    if request.method == 'GET' :
        try:
            cur.execute("SELECT * FROM borrower ORDER BY borrower_id")
            result = cur.fetchall()
            con.commit()
            cur.execute("SELECT * FROM student ORDER by std_id")
            stdresult = cur.fetchall()
            con.commit()
            cur.execute("SELECT * FROM book NATURAL JOIN author ORDER by book_id")
            bookresult = cur.fetchall()
            con.commit()
        except (Exception, psycopg2.Error) as error:
            print(error)
            return redirect('/addborrowers')

    return render_template("addborrower.html",data = result,data2 = stdresult,data3 =bookresult)   

def updatebook(books,x) :
    print(books)
    for i in range(len(books)) :
        updatebook = """UPDATE book SET "BookStatus"= 1 WHERE book_id = {} """.format(books[i])
        cur.execute(updatebook)
        borrowbook = """insert into borrowers_books (book_id, borrower_id) values (%s,%s)"""
        cur.execute(borrowbook,(books[i],x))
        con.commit()
        return redirect('/addborrowers')


@app.route('/updateborrower/<string:id>',methods=["GET", "POST"])
def updateborrower(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM student WHERE std_id ="+id+"")
        update = cur.fetchall()
        return render_template("update.html",data = update)
    if request.method == 'POST':
        try : 
            id = request.form["std_id"] 
            name = request.form["std_firstname"] 
            lname = request.form["std_lastname"] 
            major = request.form["major"]
            year = request.form["Year"]
            pg_update = """Update student set std_firstname = %s , std_lastname = %s ,std_major = %s ,std_year = %s where std_id = %s"""
            cur.execute(pg_update, (name,lname,major,year, id))
        except (Exception, psycopg2.Error) as error:
            print("Error selecting data from table book", error)
            return redirect('/addborrowers')
        finally:
            con.commit()
            return redirect('/addborrowers')

@app.route('/deleteborrower/<string:id>')
def deleteborrower(id):
    try :
        cur.execute("DELETE FROM borrower WHERE borrower_id ="+id+"")
    except (Exception, psycopg2.Error) as error:
        print("Error selecting data from table book", error)
    finally:
        con.commit()
        return  redirect('/addborrowers')
app.run(debug=True,use_reloader=True)

