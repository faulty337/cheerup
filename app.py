import hashlib
import datetime

import jwt
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session
client = MongoClient('mongodb+srv://djwhs3:wjfjsdk159@cluster0.64rvp9d.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta
# from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
# from Oauth import Oauth


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_post',methods="GET")
def post_get():
    post_list = list(db.bucket.find({}, {'_id': False}))
    return jsonify({'post':post_list})
@app.route('/user/get_post', methods="GET")
def user_post_get():
    payload =request.form['user_id']
    user_id = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

    post_list = list(db.post.find({'user_id':user_id},{'_id':False}))
    return jsonify({'post':post_list})
@app.route('/detail', methods="GET")
def post_detail():

@app.route('/set_post', methods=["POST"])
def set_post():
    # 게시글 번호 넣기
    post_list = list(db.post.find({},{'_id':False}))
    count = len(post_list) + 1

    # 토큰으로 id 가져와서 닉네임 조회
    payload = request.form['user_id']
    id_receive = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    name = db.userS.find_one({'user_id': id_receive})
    name_receive = (name['user_name'])

    # 게시글 내용 넣기
    content_recive = request.form['content_give']
    # 게시글 작성 날짜
    date_recive = datetime.today()

    doc = {
        'post_num' : count ,
        'name': name_receive,
        'comment': content_recive,
        'date': date_recive
    }
    db.cheereup.insert_one(doc)




if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)