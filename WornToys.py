import os
from flask import Flask, render_template, request, redirect, jsonify, session, flash, url_for, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField, DateField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo, InputRequired)
from werkzeug.utils import secure_filename
from os.path import join, dirname, realpath
from datetime import datetime

UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/uploads/')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app = Flask(__name__)
app.secret_key = 'IUERHIUEHRG98347%DE$'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# this connects flask to connect to the database
app.config.from_pyfile('config.cfg')

# make a database object and register it to the application
db = SQLAlchemy(app)


# need to change to RegistrationForm name
class LoginForm(FlaskForm):
    firstName = StringField('First Name', validators=[InputRequired()])
    lastName = StringField('Last Name', validators=[InputRequired()])
    username = StringField('Username', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])


class ListingForm(FlaskForm):
    name = StringField('Toy Name', validators=[InputRequired()])


class User(db.Model):
    user_id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))
    email = db.Column(db.VARCHAR(50))
    password = db.Column(db.VARCHAR(50))
    username = db.Column(db.VARCHAR(50))


class Toy(db.Model):
    toy_id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    seller_id = db.Column(db.INTEGER)
    name = db.Column(db.String(55))
    list_date = db.Column(db.DateTime)
    toy_image = db.Column(db.VARCHAR(55))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard/')
def dashboard():
    if 'username' in session:
        user = session['username']
        print("user from session: {}".format(user))
        # get the group that they're in
        # first get the user
        user_obj = User.query.filter_by(username=user).first()
        print("Username from db query : {}".format(user_obj.first_name))

    else:
        return render_template('index.html')

    return render_template('dashboard.html', user=user_obj)


@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        print("method is post, process the form. ")
        form_data = request.form
        uname = form_data['input_uname']
        passw = form_data['input_password']
        # select the user where the username and password are in the db
        user = User.query.filter_by(username=uname, password=passw).first()
        # if the user query is not none, meaning it exists..
        if user is not None:
            session['username'] = uname
            return redirect("/dashboard")
        else:
            return render_template('login.html', sucessval="FALSE")
    else:
        return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = LoginForm()
    if form.validate_on_submit():
        new_user = User(first_name=form.firstName.data, last_name=form.lastName.data,
                        email=form.email.data, password=form.password.data, username=form.username.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Thanks for registering')
        return redirect('/login/')
    flash('All fields required')
    return render_template('register.html', form=form)


@app.route('/listing/')
def listing():
    if 'username' in session:
        user = session['username']
        print("user from session: {}".format(user))
        # get the group that they're in
        # first get the user
        user_obj = User.query.filter_by(username=user).first()
        print("Username from db query : {}".format(user_obj.first_name))

    else:
        return render_template('login.html')

    return render_template('listing.html', user=user_obj)


@app.route('/listing-form/', methods=['GET', 'POST'])
def listingform():
    print("hello")
    form = ListingForm()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename) and 'username' in session:
            user = session['username']
            print("user from session: {}".format(user))
            user_obj = User.query.filter_by(username=user).first()
            print("test: {}".format(user_obj.user_id))

            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            new_toy = Toy(seller_id=user_obj.user_id, name=form.name.data, list_date=datetime.now(), toy_image=filename)
            db.session.add(new_toy)
            db.session.commit()

            print ('upload success')
            return render_template('listing-form.html', form=form)
    return render_template('listing-form.html', form=form)


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == '__main__':
    app.run(debug=True)

