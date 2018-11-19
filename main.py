# November 19, 2018
# Jessica Kincaid
# Blogz Assignment 

# main.py

from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import url_for

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:greenenchiladas@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

############# Storing passwords in the db is not a good idea, so eventually I will modify it accordingly.

class Blog(db.Model): # Create an instance of the Blog class
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200)) # Creates a property that will map to a column of type VARCHAR(200) in the blog table.
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

# Amend the constructor so that it takes in a user (owner) object 
    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner 


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    user_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    # blogs = `db.relationship('Blog', backref='user')`

    def __init__(self, username, password):
        self.username = username
        self.password = password


@app.route('/', methods=['POST', 'GET'])
def index():
    id=request.args.get('id')
    if id:
        blog= Blog.query.filter_by(id=id).first()
        return render_template('post.html', blog=blog)
    blogz = Blog.query.all()
    return render_template('blog.html', blogz=blogz)

# @app.route('/blog') # The blog route displays all posts.
# def index():
#     return render_template('blog.html')


@app.route('/newpost', methods=['POST','GET']) # Submit your blogs through '/newpost' 
# After you submit, the main page is displayed.
def process_add_entry():
    title_error = ''
    body_error = ''
    title = ''
    body = ''
    if request.method == 'POST': # Create a new post
        
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body)
        db.session.add(new_blog)
        
        if not title:
            title_error = 'You must enter a title.'
        if not body:
            body_error = 'You must enter a blog post.'
        if not title_error and not body_error: 
            db.session.commit()
            return redirect(url_for('index', id=new_blog.id))
           
    return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
    


    def signup():
        if request.method == 'POST': # Create a new user, looking at signup.html
            email = request.form['email']
            password = request.form['password']
            verify = request.form['verify']

        # TODO - validate user's data

        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO - remember the user
            session['email'] = email
            return redirect('/')
        else:
            # TODO - more specific response message
            return "<h1>Duplicate User</h1>"

    return render_template('signup.html')

if __name__ == '__main__':

    app.run()
