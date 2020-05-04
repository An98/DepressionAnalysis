from flask import Flask, render_template, redirect, url_for, request, session,jsonify
from pymongo import MongoClient
from flask_wtf.csrf import CSRFProtect
from form import RegisterForm, LoginForm, WriteForm
from datetime import datetime
import keras
import numpy as np
from keras.models import load_model
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences


app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.project
userCollection = db.user
diaryCollection = db.diary


@app.route('/')
@app.route('/past',methods=['GET','POST'])
def past():
    if 'userid' in session:
        userid = session.get('userid', None)
        nickname = session.get('nickname', None)
        results = diaryCollection.find({'id':userid},{'_id':0})
        return render_template('pastDiary.html', data=results, nickname=nickname)


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
        return redirect(url_for('past'))
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
        model = None
        input_tensor= None
        model = load_model('depression_model.h5')
        model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        MAX = 30000
        X = form.data.get('content')
        tokenizer = Tokenizer(num_words=MAX)
        tokenizer.fit_on_texts(X)
        word_vector = tokenizer.texts_to_sequences(X)
        MAX_SEQ_LENGTH = 140
        input_tensor = pad_sequences(word_vector, maxlen=MAX_SEQ_LENGTH)

        preds = model.predict(input_tensor)
        predict_labels = np.round(preds.flatten())
        # predict_labels=np.argmax(preds)
        if predict_labels[0] == 1:
            msg = ('I think You are suffering from depression:(\n %.2lf' % (preds[0][0] * 100), "% I am sure")
            depression = 'depression'
        else:
            msg = ('Nothing')
            depression = 'None'

        session['msg'] = msg
        diary = {
            'id' : userid,
            'date' : now,
            'title' : form.data.get('title'),
            'content' : form.data.get('content'),
            'depression' : depression,
            'percentage' : preds[0][0] * 100
        }
        diaryCollection.insert(diary)
        keras.backend.clear_session()

        return redirect('/past')
    return render_template('write.html',form=form,nickname=nickname)


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'IHOPEYOUTOBEhappySERIOUSly'
    csrf = CSRFProtect()
    csrf.init_app(app)



    app.run(debug=True)

