
# Deadpersyn (name tbd)
## user stories:
* The user is someone who is entering a precarious period. They need information shared and are unsure they'll be able to do fulfill that sharing. If they can't, for whatever reason, they want messages delivered to their contacts. 
* user can register, login, logout, update their account and delete their account
* user has alarms that, when triggered, send personalized messages to a list of contacts 
	* when writing an alarm, user can look at contacts currently assigned to their other alarms
* user has a switch that must be toggled somehow either before set time or by the end of the period of time (Update)
* user create (C), can see their alarms (R), can update alarms (U), can delete their alarms (D)
* if timer switch isn't hit in time, personalized emails are sent to contacts, timer is set to inactive
* if the switch is hit, timer restarts (Update)

## Technologies to incorporate:
* React front-end
* Flask communicating with PostgreSQL
* flask has a timer module?: 
	Python has: https://pypi.org/project/python-crontab/
		https://pythonprogramming.net/crontab-tutorial-basics/

* flask facilitates email: https://pythonprogramming.net/flask-email-tutorial/

## Data Models
![Models](./models.png)

* User has:
	* password: hashed string
	* email: string
	* username: string

* Message has:
	* sender: fk User
	* time/date
	* content: string
	* sent status: boolean

* Contact has:
	* email: string
	* nickname: string
	* user_id: fk User

* Message_Recipients has:
	* message_id: fk Message
	* contact_id: fk Contact

## Wireframes
![Registration Screen](./registration_screen.png)

![login screen](./login_screen.png)

![Landing Page](./user_show.png)

![Create Message](./message_create.png)

![Edit Message](./message_edit.png)

![Contact Add](./contact_add.png)

![contact edit](./contact_edit.png)

![User edit](./edit_user.png)

## Routes
### User CRUD
#### Register 
This user will be able to create their profile instance.<br>
@users.route('/register', methods=['POST'])
#### Log In 
This user will be able to log in on login page.<br>
@users.route('/login', methods=['PUT'])
#### Show 
The user will be able to see their account info on main screen.<br>
@users.route('/id', methods=['GET'])
#### Update 
The user will be able to change their user info on user edit page, loaded by clicking the '+' next to their user profile.<br>
@users.route('/id', methods=['PUT'])
#### Logged In 
The developer can tell if an instance is currently logged-in.<br>
@users.route('/logged_in', methods=['GET'])
#### Log Out 
This logs out the user, reloads login page.<br>
@users.route('/logout', methods=['GET'])
#### Delete
This deletes the user's account, along with associated alarms, contacts, recipient data. Loaded by clicking '-' next to user profile and verifying the choice.<br>
@users.route('/id', methods=['DELETE'])

### Alarm CRUD
#### Index
The user can to see the alarm instances they've set on the main page.<br>
@alarms.route('/', methods=['GET'])
#### Show
This allows the user to see details on a specific alarm instance.<br>
@alarms.route('/id', methods=['GET'])
#### Create
The user can create a new alarm instance by clicking big '+' and loading Alarm Create module.<br>
@alarms.route('/', methods=['POST'])
#### Update
The user can update their alarm instances by clicking small '+' next to specific alarm on main page.<br>
@alarms.route('/id', methods=['PUT'])
#### Delete
The user can delete an alarm instance by clicking small '-' next to specific alarm on main page. This should simultaneously remove any recipient records containing this alarm's id.<br>
@alarms.route('/id', methods=['DELETE'])

### Contact CRUD 
#### Index
The user can access their list of contacts on their main page.<br>
@contacts.route('/', methods=['GET'])
#### Show
The user can access a specific contact to update, delete or set to receive a message.<br>
@contacts.route('/id ', methods=['GET'])
#### Create
The user can add a contact instance to the table by clicking the large '+' next to contacts header on main page.<br>
@contacts.route('/', methods=['POST'])
#### Update
The user can update a contact instance in the table by clicking the small '+' next to a specific contact on the main page.<br>
@contacts.route('/id', methods=['PUT'])
#### Delete
The user can delete an instance from the contact table by clicking the small '-' next to a specific contact on the main page. This should simultaneously remove any recipient records containing this contact's id.<br>
@contacts.route('/id', methods=['DELETE'])

### Recipient CRUD
The user can use this through-table to relate contacts to alarms.<br>
#### Show
The user can see if a specific contact is attached to a specific alarm.<br>
@contacts.route('/id', methods=['GET'])
#### Create
The user can attach a contact to an alarm.<br>
@contacts.route('/', methods=['POST'])
#### Delete
The user can remove a contact from an alarm.<br>
@contacts.route('/id', methods=['DELETE'])


## Milestones
* test sending emails
* test setting timer... multiple timers...
* test running unix cron 
* can that be included in the environment setup for the app?

## stretch goals:
* option for user to be sent an email at a set period before their timer ends to remind them to hit the switch (2 hour warning, subtimer)
* allow users to create a task for a receipient, sending recipient a credential. Recipient must return credential to the email via the subject (or body?) by a certain time otherwise user is informed.
* incorporate Twilio to allow for sms to recipients: https://ahoy.twilio.com/
* allow user to set multiple switch/scenarios, each with their own messages, recipients and messages (crontab can do multiple timers, so if user in db can have multiple alarms, and each alarm has a contact list and contact has it's own message per alarm...)