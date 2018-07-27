from flask import Flask 
from flask import request

app = Flask(__name__)

@app.route('/' , methods = ['GET' , 'POST'])
def home():
		return '<h1>Home</h1>'

@app.route('/signin' , methods = ['GET'])
def signin_from():
	return	'''	<form action = "signin" method="post">
				<p><input name = "username"></p>
				<p><input name = "passwd" type = "passwd"></p>
				<p><button type = "submit">Sign In</button></p>
				</form>'''

@app.route('/signin' , methods = ['POST'])
def sigin():
	if request.form['username']=='admin'and request.form['passwd']=='passwd':
		return '<h3>Hello admin!</h3>'
	return '<h3>Bad username or passwd.</h3>'


if __name__ == '__main__':
	app.run()