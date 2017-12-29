from flask import Flask ,render_template, request, redirect, jsonify, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# this connects flask to connect to the database
app.config.from_pyfile('config.cfg')

# make a database object and register it to the application
db = SQLAlchemy(app)


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
    return render_template("dashboard.html")


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


if __name__ == '__main__':
    app.secret_key = 'IUERHIUEHRG98347%DE$'
    app.run(debug=True)

