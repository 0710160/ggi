from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from sqlalchemy.orm import relationship
from time import time
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.exceptions import HTTPException
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor, CKEditorField, upload_success, upload_fail
import os
import psycopg2
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

## WTForms
class ArticleForm(FlaskForm):
    title = StringField('Article title:')
    subtitle = StringField('Article subtitle:')
    body = CKEditorField('Article body:')
    submit = SubmitField()


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


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    form = ArticleForm()
    if request.method == "GET":
        return render_template("add.html", form=form)
    else:
        new_article_title = form.title.data
        new_article_sub = form.subtitle.data
        new_article_body = bleach_html(form.body.data)
        current_date = datetime.today().strftime('%d-%m-%Y')
        new_article = Article(title=new_article_title, subtitle=new_article_sub, body=new_article_body, date=current_date)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('home', current_user=current_user))


@app.route("/edit/<article_id>", methods=["GET", "POST"])
@login_required
def edit(article_id):
    form = ArticleForm()
    edit_article = Article.query.get(article_id)
    form.title(placeholder=edit_article.title)
    form.subtitle(placeholder=edit_article.subtitle)
    form.body(placeholder=edit_article.body)
    if request.method == "GET":
        return render_template("edit.html", article=edit_article, form=form)
    else:
        if form.title.data == "":
            pass
        else:
            title = form.title.data
            edit_article.title = title
        if form.subtitle.data == "":
            pass
        else:
            subtitle = form.subtitle.data
            edit_article.body = subtitle
        if form.body.data == "":
            pass
        else:
            body = form.body.data
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
