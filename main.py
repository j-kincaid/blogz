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

#### I don't know how I'm going to do this yet ##########
### Add in ('/blog', methods=['GET']) # This blog route displays all posts by a single user.
    # return render_template('singleUser.html')


@app.route('/newpost', methods=['POST','GET']) # Submit blogs through '/newpost' 
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
    

@app.route('/signup', methods=['POST'])
def signup():
    username = request.form['username']
    password = request.form['password']
    v_password = request.form['v_password']
    email = request.form['email']
    
    username_error = ''
    password_error = ''
    v_password_error = ''
    email_error = ''

    ####### testing the try/except block ############

# # TODO:
# # Check for errors and reject and render feedback:

    if " " in username or len(username) < 3 or len(username) > 20 or "":
        username_error = "Username cannot have spaces and must be between 3 and 20 characters"
 
   # return render_template("index.html", username=username, username_error=username_error)

    
    if len(password) > 20 or len(password) < 3 or "" or " " in password:
        password_error = 'Password must be between 3 and 20 characters.'
    
    if password != v_password:
        # password must match verified password
        v_password_error = "Passwords must match."
# email must have:
    if email:
        if not ('@'in email):
            email_error = "Email must contain @."

        if len(email) > 20 or len(email) < 3:
            email_error = "Email must be between 3 and 20 characters."

        if not ('.' in email):
            email_error = "Email must contain a . ."

        if ' ' in email:
            email_error = "Email must not contain spaces."
    
    if not username_error and not password_error and not v_password_error and not email_error:
        return render_template("blog.html", username=username, email=email)
    else:
        # redisplay the form with the error messages.
        return render_template("signup.html", username=username, username_error=username_error, password_error=password_error, v_password_error=v_password_error, email_error=email_error)

if __name__ == '__main__':

    app.run()
