from flask import Flask, render_template, redirect, url_for, request
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'IHOPEYOUTOBEhappySERIOUSly'


@app.route('/')
@app.route('/mongo',methods=['POST','GET'])
def test():
    client = MongoClient('mongodb://localhost:27017/')
    db = client.project
    collection = db.user
    results = collection.find()
    client.close()
    return render_template('main.html',data=results)

#@app.route('/<string:nickname>')
# def FlaskServer():
#       return render_template('main.html')

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        client = MongoClient('mongodb://localhost:27017/')
        db = client.project
        collection = db.user
        account = {
            'id' : form.data.get('userid'),
            'pwd' : form.data.get('password'),
            'nickname' : form.data.get('nickname')
        }
        collection.insert(account)
        return redirect(url_for('test'))
    return render_template('register.html',form=form)

@app.route('login',methods=[''])



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
    csrf = CSRFProtect()
    csrf.init_app(app)

    app.run()

