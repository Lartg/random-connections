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
    return render_template('login.html', user=None)

@app.route('/', methods=['POST', 'GET'])
def login():
    username = request.form.get('username')
    user = users.find_one({'username': username})
    #find user
    return redirect('/home/'+user['username'])

#Home page --------------------------------------------------------------
@app.route('/home/<string:username>')
def home_page(username):
    return render_template('home_index.html', posts=posts.find(), user=users.find_one({'username': username}))

# NAVBAR ROUTES ---------------------------------------------------------
@app.route('/messages/<string:username>')
def messages(username):
    
    return render_template('messages.html', user=users.find_one({'username': username}))

@app.route('/view-profile/<string:username>')
def view_profile(username):
    user_posts = []
    
    for post in posts.find({'user': username}):
        user_posts.append(post)
    return render_template('view_profile.html', user=users.find_one({'username': username}), posts=user_posts)

@app.route('/create-post/<string:username>')
def create_post(username):
    return render_template('create_post.html', user=users.find_one({'username': username}))

#CRUD POSTS --------------------------------------------------------------

#create post
@app.route('/create-post/<string:username>', methods=['POST'])
def submit_new_post(username):
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'goals': request.form.get('goals'),
        'when': request.form.get('when'),
        'date_posted': datetime.now(),
        'user': username
    }
    posts.insert_one(post)
    flash('you successfully made a post', 'success')
    return redirect('/home/'+username)
    
#update post

#delete post
@app.route('/<post_id>/delete/<string:username>')
def delete_post(post_id,username):
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect('/home/'+username)

#CRUD MSGS ---------------------------------------------------------------

#CRUD USER ---------------------------------------------------------------
@app.route('/create-account')
def create_account_form():
    return render_template('create_account.html')
@app.route('/create-account', methods=['GET','POST'])
def create_account():
    user = {
        'username': request.form.get('username'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image')
    }
    users.insert_one(user)
    return redirect('/home/'+user['username'])


@app.route('/edit-profile/<string:username>/<string:user_id>')
def edit_profile_form(username, user_id):
    user_id=user_id
    return render_template('edit_profile.html', user=users.find_one({'username': username}))


@app.route('/edit-profile/<string:username>/<string:user_id>', methods=['GET','POST'])
def edit_profile(username, user_id):
    
    updated_user = {
        'username': request.form.get('username'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image')
    }
    for post in posts.find_one({'user': username}):
        posts.update_one(
            {'user': username},
            {'$set':{'user': updated_user['username']}}
        )

         
    
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user})

    return redirect('/view-profile/'+updated_user['username'])
    




if __name__ == '__main__':
    app.run(debug=True)