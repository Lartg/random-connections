from flask import Flask, render_template, request, abort, url_for, redirect, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import redirect
from datetime import datetime

from post import post
from message import message
from account import account

app = Flask(__name__)
app.secret_key = '123456789012'
app.register_blueprint(post, url_prefix='/post')
app.register_blueprint(message, url_prefix='')
app.register_blueprint(account, url_prefix='')

client = MongoClient('mongodb+srv://Admin:kHwGiTilGkc8OEq4@cluster0.anqw0.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.get_default_database()
posts = db.posts
users = db.users
messages = db.messages

@app.route('/')
def login_page():
    return render_template('login.html', user=None)

@app.route('/', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    user = users.find_one({'username': username})
    #find user
    return redirect('/home/'+user['username'])

@app.route('/home/<string:username>')
def home_page(username):
    return render_template('home_index.html', posts=posts.find(), user=users.find_one({'username': username}))

if __name__ == '__main__':
    app.run(debug=True)
    