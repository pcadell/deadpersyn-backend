import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('deadpersyn.sqlite')

class User(UserMixin, Model):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField()

	class Meta:
		database = DATABASE

class Contact(Model):
	email = CharField()
	sender = ForeignKeyField(User, backref='contacts', on_delete='CASCADE')
	nickname = CharField()

	class Meta:
		database = DATABASE

class Alarm(Model):
	content = CharField()
	sender = ForeignKeyField(User, backref='alarms', on_delete='CASCADE')
	time = DateTimeField(default=datetime.datetime.now)
	sent = BooleanField(default=False)

	class Meta:
		database = DATABASE

class Recipient(Model):
	contact = ForeignKeyField(Contact, backref='recipients', on_delete='CASCADE')
	alarm = ForeignKeyField(Alarm, backref='recipients', on_delete='CASCADE')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Contact, Alarm, Recipient], safe=True)
	print("Created talbes if they weren't already there!")
	DATABASE.close()