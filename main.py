from flask import Flask, request, render_template, redirect, session, flash
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Entry(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, name, body, owner):
        self.name = name
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(31), unique=True)
    password = db.Column(db.String(31))
    post = db.relationship("Entry", backref="owner")

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.before_request
def require_login():
    allowed_routes = ["login", "register"]
    if request.endpoint not in allowed_routes and "username" not in session:
        return redirect('/login')

@app.route('/')
def index():
    blogPosts = Entry.query.all()
    return render_template('index.html', title="Living Diary", posts=blogPosts)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirect('/')
        else:
            flash("Incorrect login")
            pass
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        valid = True
        validString = re.compile(r'^(?=\S{3,30}$)')
        if not validString.match(username):
            valid = False
        if not validString.match(password):
            valid = False
        if password != verify:
            flash("Passwords must match")
            return redirect('/register')
        if not valid:
            flash("Characters(3-30), no spaces")
            return redirect('/register')
        existing_user = User.query.filter_by(username=username).first()
        if not existing_user:
            new_user = User(username, password)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            return redirect('/')
        else:
            flash(Name taken)
            return redirect('/register')
    return render_template('register.html')

@app.route('/entry')
def entry():
    return render_template('entry.html', title="Make a Post")

@app.route('/posted', methods=['POST', 'GET'])
def posted():
    if request.method == 'POST':
        postName = request.form['name']
        postBody = request.form['body']
        errName = ''
        errBody = ''
        if postName == '' or postBody == '':
            if postName == '':
                errName = "Text Required"
            if postBody == '':
                errBody = "Text Required"
            return render_template('entry.html', title="Make a Post",
                postName=postName, postBody=postBody, errName=errName, errBody=errBody)
        newPost = Entry(postName, postBody)
        db.session.add(newPost)
        db.session.commit()
        postQuery = Entry.query.get(newPost.id)
        return render_template('posted.html', title=postName, postName=postName, postBody=postBody,
            postQuery=postQuery)
    else:
        postId = int(request.args.get('id'))
        postQuery = Entry.query.get(postId)
        Name = postQuery.name
        return render_template('posted.html', title=Name, postQuery=postQuery)

if __name__ == "__main__":
    app.run()
