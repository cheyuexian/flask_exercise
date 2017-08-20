

from datetime import datetime
from flask import Flask, render_template,session,redirect,url_for,flash
from flask_script import Manager,Shell
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from  wtforms import StringField,SubmitField
from wtforms.validators import Required
from flask_sqlalchemy import SQLAlchemy

import os
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'data.sqlite')  #数据库使用的URL
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True   #每次请求结束后自动提交数据库的变动
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)

class Role(db.Model):
	__tablename__ = 'roles'
	id = db.Column(db.Integer,primary_key = True)
	name = db.Column(db.String(64),unique=True)
	users = db.relationship('User', backref='role', lazy='dynamic')

	def __repr__(self):
		return '<Role %r>' %self.name

class User(db.Model):
	__tablename__ = 'users'
	id = db.Column(db.Integer,primary_key = True)
	username = db.Column(db.String(64),unique=True,index=True)
	role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

	def __repr__(self):
		return '<User %r>' %self.username



class NameForm(FlaskForm):
	name = StringField('what is your nam?',validators=[Required()])
	submit = SubmitField('Submit')



@app.route('/',methods = ['GET','POST'])
def index():
	#name = None
	form = NameForm()
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.name.data).first()
		print('user:',user)
		if user is None:
			print("none")
			user = User(username=form.name.data)
			db.session.add(user)
			user1 = User.query.filter_by(username=form.name.data).first()
			print('user1:',user1)
			session['known'] = False
		else:
			print('not none')
			session['known'] = True
		session['name'] = form.name.data
		#form.name.data = ''
		return redirect(url_for('index'))
	return render_template('index.html',form=form,name=session.get('name'),
		known = session.get('known',False),current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user1.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

def make_shell_context():
	return dict(app=app,db=db,User=User,Role=Role)

manager.add_command('shell',Shell(make_context=make_shell_context))
if __name__ == '__main__':

	db.create_all()
	manager.run()
