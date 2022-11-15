import hashlib
import datetime
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session

import jwt
from pymongo import MongoClient
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session

# ? 맥 환경 DB 초기화 코드( certifi가 필요 )
import certifi
ca = certifi.where()
client = MongoClient(
    "mongodb+srv://test:sparta@cluster0.mapsk1p.mongodb.net/Cluster0?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.cheerup

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

    return jsonify({'post_list':post_list})
@app.route('/detail', methods="GET")
def post_detail():
    post_num = request.form['post_num']
    post_detail = db.post.find({'post_num':post_num},{'_id':False})
    comment_list = list(db.commennt.find({'post_num':post_num},{'_id':False}))
    return jsonify({'post_detail':post_detail},{'comment_list':comment_list})
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

@app.route('/comment_write',methods=["POST"])
def comment_write():
    cutoken = request.cookies.get("cutoken")
    try:
        payload = jwt.decode(cutoken, SECRET_KEY, algorithms=['HS256'])
        post_id = request.form['post_id']
        user_id = payload['user_id']
        content = request.form['content']

        comment_info = {
            "post_id":post_id,
            "user_id":user_id,
            "content":content    
        }
        # 'result':result 넣지 않음
        db.comments.insert_one(comment_info)
        return jsonify({'msg': "댓글이 작성되었습니다."})

    except jwt.ExpiredSignatureError:
        return redirect(url_for("index", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("index", msg="로그인 정보가 존재하지 않습니다."))

@app.route('/get_comment',methods=["GET"])
def get_comment():
    post_id = request.form("post_id")
    comment_list = list(db.comments.find({"post_id":post_id},{'_id':False}))
    return jsonify({'comment_list':comment_list})
