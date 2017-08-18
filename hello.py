

from flask import make_response
from flask import redirect
from flask import Flask
from flask import abort

from flask_script import Manager

app = Flask(__name__)
manager = Manager(app)
@app.route('/')
def index():
    return "<h1>hello,world,this is index page<h1>"
# @app.route('/user/<name>')
# def user(name):
# 	return '<h1>hello,%s!</h1>' %name

@app.route('/che')
def che():
	return '<h1>bad request</h1>', 400

@app.route('/yue')
def yue():
	response =  make_response('<h2>this document carries a cookie</h2>')
	response.set_cookie('answer','42')
	return response

@app.route('/xian')
def xian():
	return redirect('http://127.0.0.1:5000/')

@app.route('/user/<id>')
def get_user(id):
	# user = load_user(id)
	# if not user:
	abort(404)
	return '<h1>hello,%s!</h1>' %user
if __name__ == '__main__':
   manager.run()
