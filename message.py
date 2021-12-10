from re import template
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

message = Blueprint("message", __name__, static_folder='static', template_folder='templates')

@message.route('/<string:username>/reply/<string:post_id>')
def reply_form(username, post_id):
    return render_template('reply_form.html', user=users.find_one({'username': username}), post=posts.find_one({'_id': ObjectId(post_id)}))

@message.route('/<string:username>/reply/<string:post_id>', methods=['GET','POST'])
def reply(username, post_id):
    post=posts.find_one({'_id': ObjectId(post_id)})
    replies = [request.form.get('reply')]
    message = {
        'reply': replies,
        'sender':username,
        'receiver':post['user']['username']
    }
    messages.insert_one(message)
    return redirect('/messages/'+username)


@message.route('/messages/<string:username>')
def read_messages(username):
    user_messages = []
    for message in messages.find({'sender': username}):
        user_messages.append(message)
    for message in messages.find({'receiver': username}):
        user_messages.append(message)

    return render_template('messages.html', user=users.find_one({'username': username}), messages=user_messages)

@message.route('/messages/<string:username>/<string:message_id>', methods=['GET','POST'])
def respond(username, message_id):
    content = request.form.get('response')
    context = messages.find_one({'_id': ObjectId(message_id)})
    response = context['reply']
    response.append(f'From {username}: {content}')
    messages.update_one(
        {'_id': ObjectId(message_id)},
        {'$set': {'reply': response}})

    return redirect('/messages/'+username)

@message.route('/messages/delete/<string:message_id>/<string:username>')
def delete_message(message_id, username):
    messages.delete_one({'_id': ObjectId(message_id)})
    return redirect('/messages/'+username)