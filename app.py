from flask import Flask, render_template

app = Flask(__name__)

from flask import Flask, render_template, request, abort, url_for, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from werkzeug.utils import redirect
from datetime import datetime


client = MongoClient('mongodb+srv://Admin:kHwGiTilGkc8OEq4@cluster0.anqw0.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.get_default_database()
posts = db.posts

@app.route('/')
def home_page():
    """Return homepage."""
    return render_template('home_index.html', posts=posts.find())

# NAVBAR ROUTES ---------------------------------------------------------
@app.route('/messages')
def messages():
    return render_template('messages.html')

@app.route('/view-profile')
def view_profile():
    return render_template('view_profile.html')

@app.route('/create-post')
def create_post():
    return render_template('create_post.html')

#CRUD --------------------------------------------------------------------

#create post
@app.route('/create-post', methods=['POST'])
def submit_new_post():
    post = {
        'title': request.form.get('title'),
        'description': request.form.get('description'),
        'goals': request.form.get('goals'),
        'when': request.form.get('when') 
    }
    #add date posted
    #add poster identification for update and destroy, worry later YAGNI demo
    print(datetime.now)
    posts.insert_one(post)
    return redirect('/')
    
#read public posts on home page
#read user posts on profile
#update posts through profile
#change delete path so that it is through profile later
#delete path on post to avoid clutter is neccesary

@app.route('/<post_id>/delete')
def delete_post(post_id):
    posts.delete_one({'_id': ObjectId(post_id)})
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)