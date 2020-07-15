from flask import Flask,render_template,redirect,url_for,request
from sklearn.ensemble import RandomForestClassifier
import sqlite3
import pickle

con=sqlite3.connect('sep1.db')
cur=con.cursor()
cur.execute('create table if not exists userdata(id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,name TEXT NOT NULL,email TEXT NOT NULL,username TEXTNOT NULL, password TEXT NOT NULL)')

app=Flask(__name__)

@app.route('/')
def register():
    return render_template('register.html')

@app.route('/register',methods=['POST','GET'])
def savereg():
    if request.method=='POST':
        name=request.form['fname']
        uemail=request.form['mail']
        uname1=request.form['uname']
        pass1=request.form['passw']
        cnpass=request.form['cnpassw']
        if pass1==cnpass:
            with sqlite3.connect('sep1.db') as con:
                cur=con.cursor()
                cur.execute('insert into userdata(name,email,username,password) values(?,?,?,?)',(name,uemail,uname1,pass1))
                con.commit()
                return redirect('login')
        else:
            return redirect('/')
    return redirect('login')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login',methods=['POST','GET'])
def savelog():
    if request.method == "POST":
        username=request.form['uname']
        password=request.form['passw']
        with sqlite3.connect("sep1.db") as con:
            cur = con.cursor()
            cur.execute("select * from userdata where username=?",(username,))
            rows = cur.fetchone()

            u1=rows[3]
            u2=rows[4]

            if((username ==u1 ) and (password == u2)):
                return render_template('Predict_sepsis.html')
            else:
                return render_template('login.html')

    return render_template('login.html')

@app.route('/predict_sepsis',methods=['POST','GET'])
def sepsis():
    if request.method=="POST":
        model=pickle.load(open('test1.pickle','rb'))
        d={"Yes":0,"No":1,"yes":0,"no":1,"YES":0,"NO":1}
        Loc=request.form['Loc']
        Res=int(request.form['Res'])
        Hr=int(request.form['Hr'])
        Wbc=int(request.form['Wbc'])
        Temp=int(request.form['Temp'])
        Con=request.form['Con']
        Con=d[Con]
        Crp=int(request.form['Crp'])
        print(Crp,Loc,Res)
        s=model.predict([[Res,Hr,Wbc,Temp,Con,Crp]])
        if s[0]==0:
            return render_template('No_Def.html')
        else:
            return redirect('/predict_severe')
    return render_template('Predict_sepsis.html')

@app.route('/predict_severe',methods=['POST','GET'])
def severe():
    if request.method=='POST':
        model=pickle.load(open('test2.pickle','rb'))
        un=float(request.form['Un'])
        sp=int(request.form['SP'])
        print(un,sp)
        s=model.predict([[un,sp]])
        print(s)
        if s[0]==1:
            return redirect('/predict_shock')
        else:
            return render_template('Only_Sep.html')
    return render_template('Predict_severe.html')


@app.route('/predict_shock',methods=['POST','GET'])
def shock():
    if request.method=='POST':
        model=pickle.load(open('test3.pickle','rb'))
        bp=int(request.form['BpS'])
        bd=int(request.form['BpD'])
        un=float(request.form['Un'])
        gl=int(request.form['Gl'])
        cr=int(request.form['Cr'])
        lc=float(request.form['Lc'])
        bl=float(request.form['Bl'])
        inr=float(request.form['Inr'])
        pl=float(request.form['PL'])
        s=model.predict([[bp,bd,un,gl,cr,lc,bl,inr,pl]])
        print(s)
        if s[0]==3:
            return redirect('/result')
             
        else:
            return redirect('/neg_result')
            
    return render_template('Predict_shock.html')

if __name__=='__main__':
    app.run(debug=True)
