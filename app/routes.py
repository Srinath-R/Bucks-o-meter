from app import app
from flask import render_template,url_for,request,session,redirect
from app import db
from app.models import User, Transactions
from datetime import datetime

@app.route('/')
@app.route('/index')
@app.route('/index.html')
def index():
    return render_template("index.html")

@app.route('/login.html')
def login():
    if 'user' in session:
        return render_template("home.html",session=session)
    else:    
        return render_template("login.html")     

@app.route('/register.html')
def register():
    if 'user' in session:
        return render_template("home.html",session=session)
    else:  
        return render_template("register.html")    

@app.route('/register',methods = ['POST','GET'])
def add_user():
    if request.method == "POST":
        result = request.form
        if result['password'] == result['confirm_password']:
            u = User(name=result['name'], email=result['email'],password=result['password'])
            db.session.add(u)
            db.session.commit()
        return render_template("login.html")

@app.route('/dashboard',methods = ['POST','GET'])
def login_user():
    if 'user' in session:
        return render_template("home.html",session=session)
    elif request.method == "POST":
        result = request.form
        email = result['email']
        password = result['password']
        query = db.engine.execute("SELECT * FROM user WHERE email='{}'".format(email))
        row = query.fetchone()
        if row is None:
            return "Wrong Email ID!"  
        elif password == row[2]:
            session['id'] = row[0]  
            session.permanent = True
            session['email'] = row[1]
            session['password'] = row[2]
            session['user'] = row[3]
            return render_template("home.html",session = session)
        else:
            return "Wrong password!"   
    else:
        return "Bad Request."             
          
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("login"))  

@app.route('/home.html')
def home():
    return render_template("home.html")    

@app.route('/add')
def add():
    return render_template("add.html")

@app.route('/view')
def trans():
    query = db.engine.execute("SELECT * FROM transactions WHERE user_id={}".format(session['id']))
    return render_template("trans.html", results=query)

@app.route('/stat')
def stat():
    return render_template('stat.html')

@app.route('/an')
def annualchart():
    legend = 'Money spent Month-wise'
    labels = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    query = db.engine.execute("SELECT SUM(amount) AS sum,strftime('%m', date) AS mon FROM transactions WHERE user_id={} AND strftime('%Y', date)=strftime('%Y',date('now')) GROUP BY strftime('%m', date)".format(session['id']))
    row = query.fetchall()
    values = []
    j = 0
    i = 1
    while 1 <= i and i<=12 and j < len(row):
        if(str(0)+str(i) == row[j].mon):
            values.append(row[j].sum)
            j += 1
            i += 1
        else:
            values.append(0)
            i += 1 
    while len(values) < 12:
        values.append(0)        

    return render_template('an.html', values=values, labels=labels, legend=legend)

@app.route('/pie')
def monthchart():
    legend = 'Money spent this month'
    label = ["Bills & Utilities", "Education", "Entertainment", "Food & Beverage", "Gifts & Donations", "Groceries", "Others", "Transportation"]
    colors = [ "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA","#ABCDEF", "#DDDDDD", "#ABCABC", "#39FF14"]
    query = db.engine.execute("SELECT SUM(amount) AS sum,category FROM transactions WHERE user_id={} AND strftime('%m', date)=strftime('%m',date('now')) GROUP BY category ORDER BY category".format(session['id']))
    row = query.fetchall()
    values = []
    labels = ["Bills and Utilities", "Education", "Entertainment", "Food and Beverage", "Gifts and Donations", "Groceries", "Others", "Transportation"]
    j = 0
    i = 0
    while 0 <= i and i<=7 and j < len(row):
        if(label[i] == row[j].category):
            values.append(row[j].sum)
            j += 1
            i += 1
        else:
            values.append(0)
            i += 1 
    while len(values) < 8:
        values.append(0)        
    
    return render_template('pie.html', values=values, labels=labels, colors=colors, legend=legend)

@app.route('/rep')
def report():
    return render_template('report.html')

@app.route('/adding',methods = ['POST','GET'])
def addexpense():
    if 'user' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            result = request.form
            for num in range(1,101):
                if db.session.query(Transactions.id).filter_by(id=num).scalar() is None:
                    tno = num
                    break
            t = Transactions(id=tno,date=datetime.strptime(result['date'], '%Y-%m-%d'),category=result['type'],amount=result['amount'],note=result['note'],user_id=int(session['id']))
            db.session.add(t)
            db.session.commit()
            return redirect(url_for("trans"))

@app.route('/deleteexpense',methods = ['POST','GET'])
def deleteexpense():
    if 'user' not in session:
        return redirect(url_for("login"))
    else:
        if request.method == "POST":
            result = request.form
            db.engine.execute("DELETE FROM transactions WHERE user_id={} AND id={}".format(session['id'],result['id']))
            return redirect(url_for("trans"))



