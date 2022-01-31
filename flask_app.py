from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_ckeditor import CKEditor
import os
# import psycopg2
import bleach

## Define folder for image uploads
UPLOAD_FOLDER = 'static/uploads/'
#UPLOAD_FOLDER = '/home/0710160/ggi/static/uploads/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
ckeditor = CKEditor(app)
app.config['CKEDITOR_HEIGHT'] = 500
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "(*Hh998gaH*(H*98&^")

##TODO: comment SQLlite, uncomment MySQL, Migrate(app, db) and flask_migrate import before publishing (COUNT 4 THINGS)

## Connect to SQLlite
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///ggi.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

## Connect to PythonAnywhere MySQL
'''
SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{username}:{password}@{hostname}/{databasename}".format(
    username="0710160",
    password="facing-stipend-cycling-coauthor",
    hostname="0710160.mysql.pythonanywhere-services.com",
    databasename="0710160$ggicn",  ## switch to 0710160$dummydb to migrate
)
app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_POOL_RECYCLE"] = 299
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
'''

db = SQLAlchemy(app)
# migrate = Migrate(app, db)

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
    img_name = db.Column(db.String(250))


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), nullable=False)
    subtitle = db.Column(db.String(256))
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(256))
    img_name = db.Column(db.String(250))


class MailingList(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False)


#db.create_all()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


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


@app.route("/mailing", methods=["GET", "POST"])
def mailings():
    if request.method == "GET":
        return render_template("mailing.html")
    else:
        name = request.form["name"]
        email = request.form["email"]
        new_mailing = MailingList(email=email, name=name)
        if MailingList.query.filter_by(email=email).first():
            flash("You're already signed up!")
            return render_template("mailing.html")
        else:
            db.session.add(new_mailing)
            db.session.commit()
            flash("Thanks for signing up!")
            return render_template("mailing.html")


## ADD, UPLOAD, EDIT, DELETE INFORMER ARTICLES
@app.route("/informer")
def informer():
    desc_articles = Article.query.order_by(Article.id.desc())
    return render_template("informer.html", articles=desc_articles)


@app.route("/informer/<article_id>")
def article(article_id):
    read_article = Article.query.get(article_id)
    return render_template("article.html", article=read_article)


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
        img_name = "null"
        new_article = Article(title=new_article_title, subtitle=new_article_sub, body=new_article_body,
                              date=current_date, img_name=img_name)
        db.session.add(new_article)
        db.session.commit()
        return redirect(url_for('upload_informer', current_user=current_user))


@app.route("/upload_informer", methods=["GET", "POST"])
@login_required
def upload_informer():
    if request.method == 'GET':
        return render_template('upload_informer.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select a file, browser submits empty part without filename
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            orig_filename = secure_filename(file.filename)
            orig_extn = orig_filename.split(".")[1]
            descending = Article.query.order_by(Article.id.desc())
            last_article = descending.first()
            new_filename = f'informer{last_article.id}.{orig_extn}'
            last_article.img_name = new_filename
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            #print('upload_image filename: ' + new_filename)
            return redirect(url_for('informer', current_user=current_user))



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
    return redirect(url_for('informer', current_user=current_user))


@app.route("/delete/<article_id>")
@login_required
def delete(article_id):
    delete_article = Article.query.get(article_id)
    db.session.delete(delete_article)
    db.session.commit()
    return redirect(url_for('informer', current_user=current_user))


# Article navigation buttons
@app.route("/next/<article_id>")
def next_article(article_id):
    curr_article = Article.query.get(article_id)
    if curr_article.id == 1:
        return render_template("article.html", article=curr_article)
    else:
        next_article_num = int(curr_article.id - 1)
        next_article = Article.query.get(next_article_num)
        return render_template("article.html", article=next_article)


@app.route("/previous/<article_id>")
def previous_article(article_id):
    curr_article = Article.query.get(article_id)
    descending = Article.query.order_by(Article.id.desc())
    last_article = descending.first()
    if curr_article == last_article:
        return render_template("article.html", article=curr_article)
    else:
        prev_article_num = int(curr_article.id + 1)
        prev_article = Article.query.get(prev_article_num)
        return render_template("article.html", article=prev_article)


## ADD, UPLOAD, EDIT, DELETE EVENTS
@app.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "GET":
        return render_template("add.html")
    else:
        new_event_title = request.form["title"]
        new_event_subtitle = request.form["subtitle"]
        new_event_body = bleach_html(request.form.get('ckeditor'))
        current_date = datetime.today().strftime('%d-%m-%Y')
        img_name = "null"
        new_event = Events(title=new_event_title, subtitle=new_event_subtitle, body=new_event_body,
                           date=current_date, img_name=img_name)
        db.session.add(new_event)
        db.session.commit()

        return redirect(url_for('upload_event', current_user=current_user))


@app.route("/upload_event", methods=["GET", "POST"])
@login_required
def upload_event():
    if request.method == 'GET':
        return render_template('upload_event.html')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select a file, browser submits empty part without filename
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            orig_filename = secure_filename(file.filename)
            orig_extn = orig_filename.split(".")[1]
            descending = Events.query.order_by(Events.id.desc())
            last_article = descending.first()
            new_filename = f'event{last_article.id}.{orig_extn}'
            last_article.img_name = new_filename
            db.session.commit()
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
            #print('upload_image filename: ' + new_filename)
            return redirect(url_for('events', current_user=current_user))


@app.route("/edit_event/<event_id>", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    edit_article = Events.query.get(event_id)
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
    return redirect(url_for('events', current_user=current_user))


@app.route("/delete_event/<event_id>")
@login_required
def delete_event(event_id):
    delete_article = Events.query.get(event_id)
    db.session.delete(delete_article)
    db.session.commit()
    return redirect(url_for('events', current_user=current_user))


@app.route('/display/<filename>')
def display_image(filename):
    print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route("/events")
def events():
    return render_template("events.html", events=Events.query.all())


@app.route("/shed")
def shed():
    return render_template("shed.html")


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


@app.route("/playground")
def playground():
    return render_template("playground.html")


@app.route("/things-to-do")
def things():
    return render_template("things-to-do.html")


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
