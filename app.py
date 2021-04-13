from typing import final
from flask import Flask,render_template,request,redirect
import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342_DATABASE',
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

@app.route('/search/<string:id>', methods=['POST','GET'])
def search(id):
    return(id)
    



    



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

@app.route('/searchauthor', methods=["POST","GET"])
def searchauthor():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM author WHERE author_firstname LIKE '"'%{}%'"'OR author_lastname LIKE '"'%{}%'"'").format(input,input)
        cur.execute(pg_del)
        result = cur.fetchall()
    return render_template("addauthor.html",data = result)   

##############################################################################################################################

@app.route('/addbook', methods=["POST","GET"])
def addbook():
    if request.method == 'POST' :
        insertbookdb()
        return redirect('/addbook')
    if request.method == 'GET' :
        cur.execute("select DISTINCT * from author natural right join book order by book_id ")
        result = cur.fetchall()
        cur.execute("SELECT * FROM author order by author_id")
        author = cur.fetchall()
        cur.execute("SELECT * FROM category_list")
        category = cur.fetchall()
        return render_template("addbook.html",data = result,data2 = author,data3 = category)

def insertbookdb() :
    author_id = request.form["a_id"]
    title = request.form["title"] 
    floor = request.form["floor"]
    publisher = request.form["publisher"]
    category = request.form["c_id"]
    try :
        cur.execute('insert into book (author_id,booktitle,floor,book_publisher) values (%s,%s,%s,%s)',(author_id,title,floor,publisher))
    except (Exception, psycopg2.Error) as error: 
            print("Error selecting data from table book", error)
            return redirect('/addbook')
    finally : 
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
        bookid = request.form["book_id"] 
        title = request.form["title"] 
        author_id = request.form["author_id"] 
        floor = request.form["floor"] 
        publisher = request.form["year"] 
        pg_update = """Update book set author_id = {} , booktitle = {} , floor = {} , book_publisher = {} where book_id = {}"""
        cur.execute(pg_update, (author_id,title,floor,publisher,bookid))
        con.commit()
        return redirect('/addbook')
        

@app.route('/deletebook/<string:id>')
def deletebook(id):
    try : 
        cur.execute("DELETE FROM book WHERE book_id="+id+"")
    except (Exception, psycopg2.Error) as error: 
        print("Error selecting data from table book", error)
        return redirect('/addbook')
    finally : 
        con.commit()
        return  redirect('/addbook')


@app.route('/searchbook', methods=["POST","GET"])
def searchbook():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = """"SELECT * FROM book WHERE author_firstname LIKE '%{}%'OR author_lastname LIKE '%{}%' """
        cur.execute(pg_del,input,input)
        result = cur.fetchall()
    return render_template("addbook.html",data = result)   

@app.route('/searchbooks', methods=["POST","GET"])
def searchbooks():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM book WHERE booktitle LIKE '"'%{}%'"'").format(input,input)
        cur.execute(pg_del)
        result = cur.fetchall()
        return render_template("searchbook.html",data = result)   
    if request.method == 'GET' :
        cur.execute("SELECT * FROM book")
        result = cur.fetchall()
        return render_template("searchbook.html",data = result)

@app.route('/addcategory', methods=["POST","GET"])
def addcaterory():
    if request.method == 'POST' :
        try : 
            name = request.form["name"] 
            des = request.form["des"] 
            addstudent = """insert into category_list (categoryname,des) values (%s,%s)"""
            cur.execute(addstudent,(name,des))
            print("สำเร็จ") 
        except (Exception, psycopg2.Error) as error:     
            print("Error จ้า", error)
            return redirect('/addcategory')
        finally : 
            con.commit() 
            return redirect('/addcategory') 

    if request.method == 'GET' : 

        cur.execute("SELECT * FROM category_list")

        result = cur.fetchall()

    return render_template("addcategory.html",data = result)   

app.run(debug=True,use_reloader=True)
