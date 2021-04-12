from flask import Flask,render_template,request,redirect
import psycopg2
try: 
    con=psycopg2.connect(
    host='localhost',
    database='CP342_project',
    user='postgres',
    password='0957132960'
    )
except (Exception, psycopg2.Error) as error: print("Error selecting data from table book", error)
cur=con.cursor()
app = Flask(__name__)


@app.route('/')
def index():
    return render_template("home.html")


@app.route('/addstudent', methods=["POST","GET"])
def home():
    if request.method == 'POST' :
        insertstudentdb()
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
        id = request.form["std_id"] 
        name = request.form["std_firstname"] 
        lname = request.form["std_lastname"] 
        major = request.form["major"]
        year = request.form["Year"]
        pg_update = """Update student set std_firstname = %s , std_lastname = %s ,std_major = %s ,std_year = %s where std_id = %s"""
        cur.execute(pg_update, (name,lname,major,year, id))
        con.commit()
        return redirect('/addstudent')
        

@app.route('/delete/<string:id>')
def delete(id):
    cur.execute("DELETE FROM student WHERE std_id="+id+"")
    con.commit()
    return  redirect('/addstudent')

@app.route('/search', methods=["POST","GET"])
def search():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM student WHERE std_firstname LIKE '"'%{}%'"'OR std_lastname LIKE '"'%{}%'"'OR std_major LIKE '"'%{}%'"' OR std_year LIKE '"'%{}%'"'").format(input,input,input,input)
        cur.execute(pg_del)
        result = cur.fetchall()
        con.commit()
    return render_template("add.html",data = result)   

@app.route('/adminpage')
def admin():
    return render_template("admin.html")

def insertstudentdb() :
    id = request.form["s_id"] 
    name = request.form["fname"] 
    lastname = request.form["lname"] 
    major = request.form["major"]
    year = request.form["Year"]
    cur.execute('insert into student values (%s,%s,%s,%s,%s)',(id,name,lastname,major,year))
    con.commit()
    return print("สำเร็จ!")



##############################################################################################################################AUTHOR

@app.route('/addauthor', methods=["POST","GET"])
def addauthor():
    if request.method == 'POST' :
        insertauthordb()
        return redirect('/addauthor')
    if request.method == 'GET' :
        cur.execute("SELECT * FROM author")
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
        pg_update = """Update author set author_firstname = %s , author_lastname = %s  where author_id = %s"""
        cur.execute(pg_update, (name,lname,id))
        con.commit()
        return redirect('/addauthor')
        

@app.route('/deleteauthor/<string:id>')
def deleteauthor(id):
    cur.execute("DELETE FROM author WHERE author_id="+id+"")
    con.commit()
    return  redirect('/addauthor')

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
        cur.execute("SELECT * FROM book")
        result = cur.fetchall()
        return render_template("addbook.html",data = result)

def insertbookdb() :
    author_id = request.form["a_id"] 
    title = request.form["title"] 
    floor = request.form["floor"] 
    publisher = request.form["publisher"] 
    cur.execute('insert into book (author_id,booktitle,floor,book_publisher) values (%s,%s,%s,%s)',(author_id,title,floor,publisher))
    con.commit()

@app.route('/updatebook/<string:id>',methods=["GET", "POST"])
def updatebook(id):
    if request.method == 'GET':
        cur.execute("SELECT * FROM book WHERE book_id ="+id+"ORDER BY book_id")
        update = cur.fetchall()
        return render_template("updatebook.html",data = update)
    if request.method == 'POST':
        bookid = request.form["book_id"] 
        title = request.form["title"] 
        author_id = request.form["author_id"] 
        floor = request.form["floor"] 
        publisher = request.form["year"] 
        pg_update = """Update book set author_id = %s , booktitle = %s , floor = %s , book_publisher = %s where book_id = %s"""
        cur.execute(pg_update, (author_id,title,floor,publisher,bookid))
        con.commit()
        return redirect('/addbook')
        

@app.route('/deletebook/<string:id>')
def deletebook(id):
    cur.execute("DELETE FROM book WHERE book_id="+id+"")
    con.commit()
    return  redirect('/addbook')

@app.route('/searchbook', methods=["POST","GET"])
def searchbook():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM book WHERE author_firstname LIKE '"'%{}%'"'OR author_lastname LIKE '"'%{}%'"'").format(input,input)
        cur.execute(pg_del)
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
        

app.run(debug=True,use_reloader=True)
