import hashlib
import datetime
from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session

# ? 맥 환경 DB 초기화 코드( certifi가 필요 )
import certifi
ca = certifi.where()
client = MongoClient(
    "mongodb+srv://test:sparta@cluster0.mapsk1p.mongodb.net/Cluster0?retryWrites=true&w=majority",
    tlsCAFile=ca,
)
db = client.cheerup


# from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
# from Oauth import Oauth
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
