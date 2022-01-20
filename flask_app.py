from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor, CKEditorField, upload_success, upload_fail
import os
#import psycopg2
import bleach

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['CKEDITOR_HEIGHT'] = 500

## Connect to DB
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///ggi.db')
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "(*Hh998gaH*(H*98&^")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


## Flask login manager
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(256), nullable=False)
    password = db.Column(db.String(256), nullable=False)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    subtitle = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(256))
    #img_url = db.Column(db.String(250))


class MailingList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)


db.create_all()

## strips invalid tags/attributes
def bleach_html(content):
    allowed_tags = ['a', 'abbr', 'acronym', 'address', 'b', 'br', 'div', 'dl', 'dt',
                    'em', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'hr', 'i', 'img',
                    'li', 'ol', 'p', 'pre', 'q', 's', 'small', 'strike',
                    'span', 'sub', 'sup', 'table', 'tbody', 'td', 'tfoot', 'th',
                    'thead', 'tr', 'tt', 'u', 'ul']
    allowed_attrs = {
        'a': ['href', 'target', 'title'],
        'img': ['src', 'alt', 'width', 'height'],
    }
    cleaned = bleach.clean(content,
                           tags=allowed_tags,
                           attributes=allowed_attrs,
                           strip=True)
    return cleaned


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/informer")
def informer():
    articles = Article.query.all()
    return render_template("informer.html", articles=articles)


@app.route("/informer/<article_id>")
def article(article_id):
    read_article = Article.query.get(article_id)
    return render_template("article.html", article=read_article)


# Article navigation buttons
@app.route("/next/<article_id>")
def next_article(article_id):
    curr_article = Article.query.get(article_id)
    next_article_num = int(curr_article.id + 1)
    next_article = Article.query.get(next_article_num)
    try:
        return render_template("article.html", article=next_article)
    except:
        return render_template("article.html", article=curr_article)


@app.route("/previous/<article_id>")
def previous_article(article_id):
    curr_article = Article.query.get(article_id)
    if curr_article.id == 1:
        return render_template("article.html", article=curr_article)
    else:
        prev_article_num = int(curr_article.id - 1)
        prev_article = Article.query.get(prev_article_num)
        return render_template("article.html", article=prev_article)


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/businesses")
def businesses():
    return render_template("businesses.html")


@app.route("/groups")
def groups():
    return render_template("groups.html")


@app.route("/venues")
def venues():
    return render_template("venues.html")


@app.route("/roadupdates")
def roadupdates():
    return render_template("roadupdates.html")


@app.route("/garden")
def garden():
    return render_template("garden.html")


@app.route("/shed")
def shed():
    return render_template("shed.html")


@app.route("/add_informer_article", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_article_title = request.form["title"]
        new_article_sub = request.form["subtitle"]
        new_article_body = bleach_html(request.form.get('ckeditor'))
        current_date = datetime.today().strftime('%d-%m-%Y')
        new_article = Article(title=new_article_title, subtitle=new_article_sub, body=new_article_body, date=current_date)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('home', current_user=current_user))


@app.route("/edit/<article_id>", methods=["GET", "POST"])
@login_required
def edit(article_id):
    edit_article = Article.query.get(article_id)
    article_body = edit_article.body
    if request.method == "GET":
        return render_template("edit.html", article=edit_article, article_body=article_body)
    else:
        if request.form["title"] == "":
            pass
        else:
            title = request.form["title"]
            edit_article.title = title
        if request.form["subtitle"] == "":
            pass
        else:
            subtitle = request.form["subtitle"]
            edit_article.subtitle = subtitle
    body = request.form.get('ckeditor')
    edit_article.body = body
    db.session.commit()
    return redirect(url_for('home', current_user=current_user))


@app.route("/delete/<article_id>")
@login_required
def delete(article_id):
    delete_article = Article.query.get(article_id)
    db.session.delete(delete_article)
    db.session.commit()
    return redirect(url_for('home', current_user=current_user))


## User handling functions
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template('register.html')
    else:
        password = generate_password_hash(
            request.form["password"],
            method='pbkdf2:sha256',
            salt_length=8
        )
        email = request.form["email"]
        new_user = User(email=email, password=password)
        if User.query.filter_by(email=email).first():
            flash("This email address is already in use.")
            return redirect(url_for('login'))
        else:
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('home', current_user=current_user))


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        email = request.form["email"]
        user = db.session.query(User).filter_by(email=email).first()
        if not user:
            flash("Account does not exist in database. Please try again.")
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, request.form["password"]):
            flash("Incorrect password. Please try again.")
            return redirect(url_for('login'))
        else:
            login_user(user, remember=True)
            return redirect(url_for('home', current_user=current_user))


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))


## Error handling
@app.errorhandler(401)
def auth_401(error):
    flash("You need to be logged in to do that.")
    return render_template("login.html"), 401


@app.errorhandler(500)
def special_exception_handler(error):
    return "Database error."


if __name__ == "__main__":
    app.run(debug=True)
