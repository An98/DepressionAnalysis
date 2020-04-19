from flask import Flask, render_template, redirect, url_for, request, session
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm, LoginForm, WriteForm
from datetime import datetime

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.project
userCollection = db.user
diaryCollection = db.diary

@app.route('/')
@app.route('/mongo',methods=['POST','GET'])
def test():
    userid = session.get('userid',None)
    nickname = session.get('nickname',None)
    if 'userid' in session:
        results = userCollection.find()
        return render_template('main.html',data=results,userid=userid,nickname=nickname)
    else:
        return "Session no exists"

#@app.route('/<string:nickname>')
# def FlaskServer():
#       return render_template('main.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        account = {
            'id' : form.data.get('userid'),
            'pwd' : form.data.get('password'),
            'nickname' : form.data.get('nickname')
        }
        userCollection.insert(account)
        return redirect(url_for('test'))
    return render_template('register.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/') #if succeed to login, redirect to home
    return render_template('login.html',form=form)


@app.route('/logout',methods=['GET'])
def logout():
    session.pop('userid',None)
    session.pop('nickname',None)
    return redirect('/')

@app.route('/write',methods=['GET','POST'])
def write():
    now = datetime.now()
    form = WriteForm()
    userid = session.get('userid', None)
    nickname = session.get('nickname', None)
    if form.validate_on_submit():
        diary = {
            'id' : userid,
            'date' : now,
            'title' : form.data.get('title'),
            'content' : form.data.get('content')
        }
        diaryCollection.insert(diary)
        return redirect('/past')
    return render_template('write.html',form=form,nickname=nickname)

@app.route('/past',methods=['GET','POST'])
def past():
    if 'userid' in session:
        userid = session.get('userid', None)
        nickname = session.get('nickname', None)
        results = diaryCollection.find({'id':userid},{'_id':0})
        return render_template('pastDiary.html', data=results, nickname=nickname)


# @app.route('login',methods=['GET','POST'])
# def login():
#     msg=''
#     if request.method == 'POST':
#         if request.form['id']:
#     return render_template('login.html',msg='To use this website, please login')


        #redirect(url_for('FlaskServer',data=results))

# @app.route('/write',methods=['POST','GET'])
# def write():
#     if request.method == 'POST':
#         collection.save({
#             "date": request.form["date"],
#             "title": request.form["request"],
#             "content":request.form["content"]
#         })
#         return redirect('/')
#     else:
#         return render_template('write.html')


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'IHOPEYOUTOBEhappySERIOUSly'
    csrf = CSRFProtect()
    csrf.init_app(app)

    app.run(debug=True)

