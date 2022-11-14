import hashlib
import datetime

from flask import Flask, render_template, jsonify, request, redirect, make_response, flash, session
# from config import SECRET_KEY, CLIENT_ID, REDIRECT_URI, LOGOUT_REDIRECT_URI
# from Oauth import Oauth
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)