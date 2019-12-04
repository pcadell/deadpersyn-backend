from flask import Flask, jsonify, g
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_login import LoginManager
import models
from playhouse.shortcuts import model_to_dict
import datetime
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

# testing db calls to build email
@app.route('/<alarm_id>') # message id comes from the alarm being set
def index(alarm_id):
	try:
		alarm = models.Alarm.get_by_id(alarm_id)		
		alarm_to_dict = model_to_dict(alarm) # logic for taking message id to find the user's email and store that
		content = alarm_to_dict['content'] # logic for taking the message id and grabbing the content
		sender = alarm_to_dict['sender']
		del sender['password']
		recipients_dicts = [model_to_dict(recipients) for recipients in models.Recipient.select().where(models.Recipient.alarm == alarm_id)] # message id used to grab contact id's from recipients entries
		contacts_ids = []

		for recipient in recipients_dicts:
			(contacts_ids.append(recipient['contact']['id']))
		contacts = [models.Contact.get_by_id(contacts_id) for contacts_id in contacts_ids]
		contact_dicts = [model_to_dict(contact) for contact in contacts] # now I can get nickname and email easy
		emails = [contact_dict['email'] for contact_dict in contact_dicts]
		nicknames = [contact_dict['nickname'] for contact_dict in contact_dicts]

		msg = Message('Hey there, a message from {}'.format(sender['username']), recipients=emails)
		msg.body = content
		mail.send(msg)
		return 'A message was sent on behalf of {} to {}.'.format(sender['username'], nicknames)
	except Exception as e:
		return str(e)



if __name__ == '__main__':
	models.initialize()
	app.run(port=PORT) # debug=DEBUG, port=APP_PORT
