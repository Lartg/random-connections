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

post = Blueprint("post", __name__, static_folder='static', template_folder='templates')

@post.route('/create/<string:username>')
def create_post(username):
    return render_template('create_post.html', user=users.find_one({'username': username}))

@post.route('/create/<string:username>', methods=['POST'])
def submit_new_post(username):
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'goals': request.form.get('goals'),
        'when': request.form.get('when'),
        'date_posted': datetime.now(),
        'user': users.find_one({'username': username})
    }
    posts.insert_one(post)
    flash('you successfully made a post', 'success')
    return redirect('/home/'+username)
    

@post.route('/update/<post_id>/<string:username>')
def update_post_form(post_id,username):
    return render_template('update_post.html', post=posts.find_one(ObjectId(post_id)), user=users.find_one({'username': username}))

@post.route('/update/<post_id>/<string:username>', methods=['GET','POST'])
def update_post(post_id,username):
    updated_post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'goals': request.form.get('goals'),
        'when': request.form.get('when'),
        'date_posted': datetime.now(),
        'user': users.find_one({'username': username})
    }
    posts.update_one(
        
        {'_id': ObjectId(post_id)},
        {'$set': updated_post}
    )
    return redirect('/view-profile/'+username)

@post.route('/delete/<string:post_id>/<string:username>')
def delete_post(post_id,username):
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect('/home/'+username)
