from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_envvar('MAIL_SETTINGS')

# #same value as mail_debug below. You get notes spat out to help configure
# app.config['DEBUG'] = True # default = True
# #same value as suppress send below
# app.config['TESTING'] = False # default = False
# # email provider, 'localhost' assumes you are running yr own
# app.config['MAIL_SERVER'] = 'localhost' # default = 
# # setting on email server (found in documentation)
# app.config['MAIL_PORT'] = 25 # default = 25
# # is your encryption TLS?
# app.config['MAIL_USE_TLS'] = False # default = False
# # is your encryption SSL?
# app.config['MAIL_USE_SSL'] = False # default = False
# # same value as app debug above
# app.config['MAIL_DEBUG'] = True # default = True
# # senders email username
# app.config['MAIL_USERNAME'] = None # default = None
# # senders email password 
# app.config['MAIL_PASSWORD'] = None # default = None
# # the reply-to address?
# app.config['MAIL_DEFAULT_SENDER'] = None # default = None
# # meant to stop emails from being blasted out
# app.config['MAIL_MAX-EMAILS'] = 5 # default = None 
# # so that you can test the functionality without blowing up an inbox, same as TESTING above
# app.config['MAIL_SUPRESS_SEND'] = False #default = False
# # tries to convert attachment characters to ASCII, as opposed to UNICODE in case server doesn't handle UNICODE
# app.config['MAIL_ASCII_ATTACHMENTS']

mail = Mail(app)

# also works to be more explicit
# mail = Mail()
# mail.init_app(app)

@app.route('/send-mail')
def index():
	try:
		msg = Message('Hey there', sender="cadell.patrick@gmail.com", recipients=['wafawot205@topmail2.net'])
		msg.body = 'Yo!\n this worked?'
		mail.send(msg)
		return 'Message has been sent!'
	
	except Exception as e:
		return str(e)

if __name__ == '__main__':
	app.run()
