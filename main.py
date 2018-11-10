from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:introducingKat@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# TODO: Make a Blog class with the necessary properties (i.e., an id, title, and body)
# 
# TODO: Initialize your database with these:

# (flask-env) $ python
# from main import db, Blog
# db.create_all()
# db.session.commit()

class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # The name is the column within blog name
    title = db.Column(db.String(500))
    body = db.Column(db.Text)

# Create a constructor: 
    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route('/blog') # The blog route displays all posts.
def index():
    return render_template('blog.html')

@app.route('/blog', methods=['POST'])
def add_entry():

    if request.method == 'POST':
        post_name = request.form['post']
        new_post = Blog(post_name)
        db.session.add(new_post)
        db.session.commit()

    return render_template('newpost.html')


# @app.route('/', methods=['POST', 'GET'])
# def index():

#     if request.method == 'POST':
#         task_name = request.form['task']
#         new_task = Task(task_name) # Create a new task object
#         db.session.add(new_task)
#         db.session.commit() # commit it to the db

#     tasks = Task.query.filter_by(completed=False).all() 
#     # only give me the tasks for which the completed column has the value False
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('newpost.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':
        post_name = request.form['post']
        new_post = Blog(post_name) # Create a new blog object
        db.session.add(new_post)
        db.session.commit() # commit it to the db

    posts = Blog.query.filter_by(completed=False).all() 
    # only give me the tasks for which the completed column has the value False
    new_posts = Blog.query.filter_by(completed=True).all()
    return render_template('newpost.html',title="Add a post!", posts=posts,  new_posts=new_posts)


@app.route('/newpost', methods=['POST']) # Submit your posts through '/newpost' 
# After you submit, the main page is displayed.
def process_add_entry():

    post_id = int(request.form['post-id'])
    post = post.query.get(post_id)
    post.completed = True
    db.session.add(post)
    db.session.commit()

    return redirect('/')

    
if __name__ == '__main__':
    app.run()