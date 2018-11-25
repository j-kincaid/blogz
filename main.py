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
# Add a session object and 
app.secret_key = 'LD@R&tEX55gl'


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
    pw_hash = db.Column(db.String(120))
    blogs = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.pw_hash = make_pw_hash(password)

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



@app.route('/newpost', methods=['POST','GET']) 
# Submit blogs through '/newpost' 
# After you submit, the main page is displayed.
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
    
   # return render_template("index.html", username=username, username_error=username_error)

    
        if len(password) > 20 or len(password) < 3 or "" or " " in password:
            password_error = 'Password must be between 3 and 20 characters.'
        
        if password != v_password:
            # password must match verified password
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

            # redisplay the form with the error messages.
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


# ################### Functionality Check: ##################
###############_ MAKE A HOMEPAGE _##############
# User is logged in and adds a new blog post, then is redirected to a page featuring the individual blog entry they just created (as in Build-a-Blog).
# User visits the /blog page and sees a list of all blog entries by all users.
# User clicks on the title of a blog entry on the /blog page and lands on the individual blog entry page.
# User clicks "Logout" and is redirected to the /blog page and is unable to access the /newpost page (is redirected to /login page instead).


# # the Home page (index.html) will display the posts by one user
# # all on one page. 
# # @app.route('/index', methods=['POST', 'GET'])
# # def index():
#     owner = User.query.filter_by(username=session['username']).first()
# #     if request.method == 'POST':
#         blog_name = request.form['blog']
#         new_blog = Blog()

# @app.route('/blog', methods='POST', 'GET')
# def view_blog():
    
#`''``From get-it-done''`
# @app.route('/', methods=['POST', 'GET'])
# def index():

# ###################_______________##################
# #### Where the new task (or new blog post) is created 
# ###################_______________##################


#     owner = User.query.filter_by(email=session['email']).first()

#     if request.method == 'POST':
#         task_name = request.form['task']
#         new_task = Task(task_name, owner) # Create a new task object
#         db.session.add(new_task)
#         db.session.commit() # commit it to the db

#     tasks = Task.query.filter_by(completed=False, owner=owner).all() 
#     # only give me the tasks for which the completed column has the value False
#     completed_tasks = Task.query.filter_by(completed=True).all()
#     return render_template('todos.html',title="Get It Done!", tasks=tasks, completed_tasks=completed_tasks)






if __name__ == '__main__':

    app.run()
