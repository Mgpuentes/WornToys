from flask import Flask ,render_template, request, redirect, jsonify, session

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")


if __name__ == '__main__':
    app.run(debug=True)
