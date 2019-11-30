from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config.from_envvar('MAIL_SETTINGS') #pointing to config file set in environs


mail = Mail(app)

# also works to be more explicit
# mail = Mail()
# mail.init_app(app)

# test path to send mail when this path is hit
@app.route('/send-mail')
def index():
	try:
		msg = Message('Hey there', sender="cadell.patrick@gmail.com", recipients=['wafawot205@topmail2.net'])
		msg.body = 'Yo!\n this worked?'
		mail.send(msg)
		return 'Is this the message that is the return for mail_app.py signalling sent message? If so, it is placed in a text file in the dir it is called from and could be useful, could contain variable information about specific message sent for later use?'
	
	except Exception as e:
		return str(e)

# mail functionality should expand to a 'show route' where a specific message is sent when this route is hit
# @app.route('/<id>') # with message id being accessed and construction of message 


if __name__ == '__main__':
	app.run()
