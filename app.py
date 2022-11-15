import hashlib
import datetime

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from config import SECRET_KEY

from pymongo import MongoClient

url = 'mongodb+srv://test:sparta@cluster0.115s91j.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(url)
db = client.cheerup

import jwt



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    #프론트단 처리 필요
    return redirect('/')

@app.route('/signup', methods=['POST'])  # GET(정보보기), POST(정보수정) 메서드 허용
def signup():
    user_id = request.form.get('user_id')
    user_name = request.form.get('user_name')
    user_pw = request.form.get('user_pw')
    user_pw2 = request.form.get('user_pw2')
    print(user_id, user_name, user_pw, user_pw2)
    if user_pw != user_pw2:
        return {'result':'fail', 'messag':'입력한 비밀번호가 다릅니다.'}
    elif db.users.find_one({'userid' : user_id}) is not None:
        return {'result':'fail', 'messag':'이미 존재하는 아이디입니다.'}
    else:
        # usertable = User(userid, username, password)
        usertable = {
            'user_id':user_id,
            'user_name':user_name,
            'user_pw':hashlib.sha256(user_pw.encode('utf-8')).hexdigest()
        }
        db.users.insert_one(usertable)
        return {'result':'success', 'messag':'회원가입 완료'}

@app.route('/login', methods=['POST'])
def login():
    user_id = request.form['user_id']
    user_pw = hashlib.sha256(request.form['user_pw'].encode('utf-8')).hexdigest()
    print(db.users.find_one({'user_id': user_id}))
    
    if db.users.find_one({'user_id': user_id, 'user_pw': user_pw}) is not None:
        payload = {
            'userid': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
        }

        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        # response = make_response(redirect('/'))
        # response.set_cookie('chtoken', token)
        # return response
        return {'result':'success', 'token':token, 'message':'로그인 되었습니다.'}
    return {'result':'fail', 'token':None, 'message':'틀린 계정입니다.'}


#임시로 만들어 놓은 거에요 이후 다른 부분에서 인증 필요할시 아래 형태로 사용합니다.
@app.route('/check')
def check():
    token_receive = request.cookies.get('chtoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.user.find_one({"id": payload['id']})
        return render_template('index.html', nickname=user_info["nick"])
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login", msg="로그인 정보가 존재하지 않습니다."))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)