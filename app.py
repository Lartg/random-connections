from flask import Flask, render_template

app = Flask(__name__)
app.secret_key = '123456789012'
#WTForms = validator

from flask import Flask, render_template, request, abort, url_for, redirect, flash
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import redirect
from datetime import datetime


client = MongoClient('mongodb+srv://Admin:kHwGiTilGkc8OEq4@cluster0.anqw0.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.get_default_database()
posts = db.posts
users = db.users

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/', methods=['POST', 'GET'])
def login():
    user = {
        'username': request.form.get('username')
    }
    users.append(user)
    return redirect('/home/'+user['username'])

#Home page --------------------------------------------------------------
@app.route('/home/<string:username>')
def home_page(username):
    return render_template('home_index.html', posts=posts.find(), user=username)

# NAVBAR ROUTES ---------------------------------------------------------
@app.route('/messages/<string:user>')
def messages(user):
    
    return render_template('messages.html', user=user)

@app.route('/view-profile/<string:user>')
def view_profile(user):
    user_posts = []
    
    for post in posts.find({'user': user}):
        user_posts.append(post)
    return render_template('view_profile.html', user=user, posts=user_posts)

@app.route('/create-post/<string:user>')
def create_post(user):
    return render_template('create_post.html', user=user)

#CRUD POSTS --------------------------------------------------------------

#create post
@app.route('/create-post/<string:user>', methods=['POST'])
def submit_new_post(user):
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'goals': request.form.get('goals'),
        'when': request.form.get('when'),
        'date_posted': datetime.now(),
        'user': user
    }
    posts.insert_one(post)
    flash('you successfully made a post', 'success')
    return redirect('/home/'+user)
    
#update post

#delete post
@app.route('/<post_id>/delete/<string:user>')
def delete_post(post_id,user):
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect('/home/'+user)

#CRUD MSGS ---------------------------------------------------------------

#CRUD USER ---------------------------------------------------------------

@app.route('/view-profile/<string:user>', methods=['GET','POST'])
def edit_profile(user):
    pass




if __name__ == '__main__':
    app.run(debug=True)