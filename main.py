# November 19, 2018
# Jessica Kincaid
# Blogz Assignment 

# main.py

from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask import url_for
from hashUtils import make_pw_hash, check_pw_hash

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:greenenchiladas@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

app.secret_key = 'LD@R&tEX55gl'

class Blog(db.Model): 
    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(200)) 
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner 

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30))
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

@app.route('/', methods=['POST', 'GET'])
def index():
   user_id=request.args.get('user_id')
   if user_id:
       #blog= Blog.query.filter_by(id=id).first()
        blog= Blog.query.filter_by(user_id=user_id).all()   
        return render_template('singleUser.html', blog=blog, user_id=user_id)

   #user_list = []
   user_list = User.query.all()
   return render_template('index.html', users=user_list)

@app.route('/blog', methods=['POST', 'GET'])
def view_blog():
    user_id=request.args.get('user_id')
    if user_id:
        blogz=Blog.query.filter_by(user_id=user_id).first()
        return render_template('index.html', blogz=blogz)
    blogz = Blog.query.all()
    return render_template('blog.html', blogz=blogz)

@app.route('/newpost', methods=['POST','GET']) 
def process_add_entry():
    title_error = ''
    body_error = ''
    title = ''
    body = ''

    owner = User.query.filter_by(username=session['username']).first()
    if request.method == 'POST': # Create a new post
        title = request.form['title']
        body = request.form['body']
        new_blog = Blog(title, body, owner)
        db.session.add(new_blog)
        
        if not title:
            title_error = 'You must enter a title.'
        if not body:
            body_error = 'You must enter a blog post.'
        if not title_error and not body_error: 
            db.session.commit()
            return redirect(url_for('index',id=new_blog.id))
           
    return render_template('newpost.html', title=title, body=body, title_error=title_error, body_error=body_error)
    
@app.route('/signup', methods=['GET','POST'])
def signup():
    username = ''
    username_error = ''
    password_error = ''
    v_password_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        v_password = request.form['v_password']
        
        if " " in username or len(username) < 3 or len(username) > 20 or "":
            username_error = "Username cannot have spaces and must be between 3 and 20 characters"


    
        if len(password) > 20 or len(password) < 3 or "" or " " in password:
            password_error = 'Password must be between 3 and 20 characters.'
        
        if password != v_password:
            v_password_error = "Passwords must match."

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            username_error = "User already exists."
        if not username_error and not password_error and not v_password_error:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return render_template("blog.html", username=username)

    return render_template("signup.html", username=username, username_error=username_error, password_error=password_error, v_password_error=v_password_error)

@app.route('/logout', methods=['GET'])
def logout():
    del session['username']
    return redirect('/')

@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect('/login')

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_error = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        
        user = User.query.filter_by(username=username).first()
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username
            return redirect('/')
        else:
            login_error = "Username or password is incorrect"
    return render_template('login.html', login_error=login_error)



if __name__ == '__main__':

    app.run()