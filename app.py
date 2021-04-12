from flask import Flask,render_template,request,redirect
import psycopg2

con=psycopg2.connect(
    host='localhost',
    database='CP342_project',
    user='postgres',
    password='0957132960'
    )

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
        return redirect('/addstudent')
        

@app.route('/delete/<string:id>')
def delete(id):
    cur.execute("DELETE FROM student WHERE std_id="+id+"")
    return  redirect('/addstudent')

@app.route('/search', methods=["POST","GET"])
def search():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM student WHERE std_firstname LIKE '"'%{}%'"'OR std_lastname LIKE '"'%{}%'"'OR std_major LIKE '"'%{}%'"' OR std_year LIKE '"'%{}%'"'").format(input,input,input,input)
        cur.execute(pg_del)
        result = cur.fetchall()
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

@app.route('/addauthor', methods=["POST","GET"])
def addbook():
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
        return redirect('/addstudent')
        

@app.route('/deleteauthor/<string:id>')
def deleteauthor(id):
    cur.execute("DELETE FROM student WHERE std_id="+id+"")
    return  redirect('/addstudent')

@app.route('/searchauthor', methods=["POST","GET"])
def searchauthor():
    if request.method == 'POST' :
        input = request.form["input"]
        pg_del = ("SELECT * FROM author WHERE author_firstname LIKE '"'%{}%'"'OR author_lastname LIKE '"'%{}%'"'").format(input,input)
        cur.execute(pg_del)
        result = cur.fetchall()
    return render_template("add.html",data = result)   
    
app.run(debug=True,use_reloader=True)
