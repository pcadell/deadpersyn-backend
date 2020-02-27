import datetime
from peewee import *
from flask_login import UserMixin

DATABASE = SqliteDatabase('deadpersyn.sqlite', pragmas={'foreign_keys': 1})

class User(UserMixin, Model):
	username = CharField(unique = True)
	email = CharField(unique = True)
	password = CharField()
	mail_server = CharField(default='default')
	mail_port = IntegerField(default=587)
	mail_use_tls = BooleanField(default=True)
	mail_use_ssl = BooleanField(default=False)
	mail_username = CharField(default='None')
	mail_password = CharField(default='None')
	class Meta:
		database = DATABASE

class Contact(Model):
	email = CharField()
	sender = ForeignKeyField(User, backref='contacts', on_delete='Cascade')
	nickname = CharField()

	class Meta:
		database = DATABASE

class Alarm(Model):
	content = CharField()
	sender = ForeignKeyField(User, backref='alarms', on_delete='Cascade')
	time = DateTimeField(default=datetime.datetime.now)
	sent = BooleanField(default=False)

	class Meta:
		database = DATABASE

class Recipient(Model):
	contact = ForeignKeyField(Contact, backref='recipients', on_delete='Cascade')
	alarm = ForeignKeyField(Alarm, backref='recipients', on_delete='Cascade')

	class Meta:
		database = DATABASE


def initialize():
	DATABASE.connect()
	DATABASE.create_tables([User, Contact, Alarm, Recipient], safe=True)
	print("Created tables if they weren't already there!")
	DATABASE.close()