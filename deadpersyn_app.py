from flask import Flask, jsonify, g
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_login import LoginManager
import models

from resources.users import users
from resources.contacts import contacts
from resources.alarms import alarms
from resources.recipients import recipients

app = Flask(__name__)
app.config.from_envvar('APP_SETTINGS') #pointing to config file set in environs
PORT = 8000
mail = Mail(app)



login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(userid):
	try:
		return models.User.get(models.User.id == userid)
	except models.DoesNotExist:
		return None

CORS(users, origins=['http://localhost:3000'], supports_credentials=True)
CORS(contacts, origins=['http://localhost:3000'], supports_credentials=True)
CORS(alarms, origins=['http://localhost:3000'], supports_credentials=True)
CORS(recipients, origins=['http://localhost:3000'], supports_credentials=True)

app.register_blueprint(users, url_prefix='/api/v1/users')
app.register_blueprint(contacts, url_prefix='/api/v1/contacts')
app.register_blueprint(alarms, url_prefix='/api/v1/alarms')
app.register_blueprint(recipients, url_prefix='/api/v1/recipients')

@app.before_request
def before_request():
	g.db = models.DATABASE
	g.db.connect()

@app.after_request
def after_request(response):
	g.db.close()
	return response

@app.route('/test', methods=['GET'])
def test_route():
	return ['Here\'s the test route']


# test path to send mail when this path is hit
@app.route('/send-mail')
def index():
	try:
		msg = Message('Hey there', recipients=['wafawot205@topmail2.net'])
		msg.body = 'Yo!\n this worked?'
		mail.send(msg)
		return 'Is this the message that is the return for mail_app.py signalling sent message? If so, it is placed in a text file in the dir it is called from and could be useful, could contain variable information about specific message sent for later use?'
	
	except Exception as e:
		return str(e)

# mail functionality should expand to a 'show route' where a specific message is sent when this route is hit
# @app.route('/<id>') # with message id being accessed and construction of message 


if __name__ == '__main__':
	models.initialize()
	app.run(port=PORT) # debug=DEBUG, port=APP_PORT
