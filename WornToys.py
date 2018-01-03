from flask import Flask, render_template, request, redirect, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, BooleanField
from wtforms.validators import (DataRequired, Regexp, ValidationError, Email,
                               Length, EqualTo)

app = Flask(__name__)
app.secret_key = 'IUERHIUEHRG98347%DE$'

# this connects flask to connect to the database
app.config.from_pyfile('config.cfg')

# make a database object and register it to the application
db = SQLAlchemy(app)


class LoginForm(FlaskForm):
    firstName = StringField('First Name', validators=[DataRequired()])
    lastName = StringField('Last Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])


class User(db.Model):
    user_id = db.Column(db.INTEGER, primary_key=True, nullable=False)
    first_name = db.Column(db.String(55))
    last_name = db.Column(db.String(55))
    email = db.Column(db.VARCHAR(50))
    password = db.Column(db.VARCHAR(50))
    username = db.Column(db.VARCHAR(50))


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = session['username']
        print("user from session: {}".format(user))
        # get the group that they're in
        # first get the user
        user_obj = User.query.filter_by(username=user).first()
        print("Username from db query : {}".format(user_obj.first_name))

    else:
        user = "NOT_SET"
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
    if request.method == 'POST':
        new_user = User(first_name=form.firstName.data, last_name=form.lastName.data,
                        email=form.email.data, password=form.password.data, username=form.username.data)

        db.session.add(new_user)
        db.session.commit()

        flash('Thanks for registering')
        return redirect('/login/')
    return render_template('register.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)

