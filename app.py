import hashlib
import jwt
import datetime
import certifi 

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, url_for
from config import SECRET_KEY
from pymongo import MongoClient


# ? 맥 환경 DB 초기화 코드( certifi가 필요 )
ca = certifi.where()
client = MongoClient(
    "mongodb+srv://test:sparta@cluster0.g39e2ay.mongodb.net/?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.cheerup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/get_post',methods=["GET"])
def post_get():
    post_list = list(db.posts.find({}, {'_id': False}))
    return jsonify({'post_list':post_list})
    
@app.route('/user/get_post', methods=["GET"])
def user_post_get():
    payload =request.form['user_id']
    user_id = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    post_list = list(db.posts.find({'user_id':user_id},{'_id':False}))

    return jsonify({'post_list':post_list})
@app.route('/detail', methods=["GET"])
def post_detail():
    post_num = request.form['post_num']
    post_detail = db.posts.find({'post_num':post_num},{'_id':False})
    comment_list = list(db.comments.find({'post_num':post_num},{'_id':False}))
    return jsonify({'post_detail':post_detail},{'comment_list':comment_list})
    
@app.route('/set_post', methods=["POST"])
def set_post():
    # 게시글 번호 넣기
    post_list = list(db.post.find({},{'_id':False}))
    count = len(post_list) + 1

    # 토큰으로 id 가져와서 닉네임 조회
    payload = request.form['user_id']
    id_receive = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    name = db.users.find_one({'user_id': id_receive})
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
    db.post.insert_one(doc)




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



@app.route('/comment_write',methods=["POST"])
def comment_write():
    cutoken = request.cookies.get("cutoken")
    try:
        payload = jwt.decode(cutoken, SECRET_KEY, algorithms=['HS256'])
        post_id = request.form['post_id']
        #user_id = payload['user_id']
        user_id = 'test'
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
    
if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
