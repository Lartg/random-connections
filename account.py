from flask import Flask, render_template, request, abort, url_for, redirect, flash, Blueprint
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import redirect
from datetime import datetime
client = MongoClient('mongodb+srv://Admin:kHwGiTilGkc8OEq4@cluster0.anqw0.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.get_default_database()
posts = db.posts
users = db.users
messages = db.messages

account = Blueprint("account", __name__, static_folder='static', template_folder='templates')

@account.route('/view-profile/<string:username>')
def view_profile(username):
    user_posts = []
    user=users.find_one({'username': username})
    for post in posts.find({'user': user}):
        user_posts.append(post)
    return render_template('view_profile.html', user=user, posts=user_posts)

@account.route('/create-account')
def create_account_form():
    return render_template('create_account.html', user=None)

@account.route('/create-account', methods=['GET','POST'])
def create_account():
    user = {
        'username': request.form.get('username'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image')
    }
    users.insert_one(user)
    return redirect('/home/'+user['username'])


@account.route('/edit-profile/<string:username>/<string:user_id>')
def edit_profile_form(username, user_id):
    user_id=user_id
    return render_template('edit_profile.html', user=users.find_one({'username': username}))


@account.route('/edit-profile/<string:username>/<string:user_id>', methods=['GET','POST'])
def edit_profile(username, user_id):
    user=users.find_one({'username': username})
    updated_user = {
        'username': request.form.get('username'),
        'bio': request.form.get('bio'),
        'image': request.form.get('image')
    }
    for post in posts.find_one({'user': user}):
        posts.update_one(
            {'user': user},
            {'$set':{'user': updated_user}}
        )
  
    users.update_one(
        {'_id': ObjectId(user_id)},
        {'$set': updated_user})

    return redirect('/view-profile/'+updated_user['username'])
    
@account.route('/delete-account/<string:username>/<string:user_id>', methods=['GET','POST'])
def delete_account(username, user_id):
    user=users.find_one({'username': username})
    posts.delete_many({'user': user}) 
    users.delete_one({'_id': ObjectId(user_id)})
    return redirect('/')