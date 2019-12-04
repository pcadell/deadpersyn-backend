import models
import os
from datetime import datetime, timezone
from crontab import CronTab
from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

alarms = Blueprint('alarms', 'alarms')

# Alarms Index
@alarms.route('/', methods=["GET"])
@login_required
def alarms_index():
	try:
		alarms = [model_to_dict(alarms) for alarms in models.Alarm.select() if alarms.sender.id == current_user.id ]
		for alarm in alarms:
			alarm['sender'].pop('password')
		print(alarms)
		return jsonify(data=alarms, status={'code': 200, "message": "success"}), 200
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'error getting the resources'}), 401

# Alarm create route
@alarms.route('/', methods=['POST'])
@login_required
def alarm_create():
	payload = request.get_json()
	# taking in the js Date() object in payload, which I'll have run in front end as newDate = date.toISOString() up to last character
	# maybe i don't need to do this (below) if ISOString coming from the front end is an acceptable format...
	# newDate = datetime.strptime(payload['dateISOString'], '%Y-%m-%dT%H:%M:%S.%f') to take a datetime and stringify python side
	# create a datetime object from the payload values via react
	# Python-CronTab can use python datetimes to assign cron job, awesome

	alarm = models.Alarm.create(content=payload['content'], sender=current_user.id, time=payload['time'], sent=False) 
	alarm_dict = model_to_dict(alarm)
	alarm_dict['sender'].pop('password')
	# not subscriptable: alarmTime = models.Alarm.get_by_id(alarm_dict['id'])['time']
	# can't insert string into datetime for cron set: alarm_dict['time']
#	setTime = datetime(alarm_dict['time'])

#	USER = os.getlogin()
#	createJob = CronTab(user=USER)
#	job = createJob.new(command='wget http://127.0.0.1:5000/send-mail', comment='{} message id'.format(USER)) # message id where send-mail is in path
#	job.setall(datetime(setTime))
#	createJob.write()
	# logic for setting a crontab before the return
	return jsonify(data=alarm_dict, status={'code': 201, 'message': 'Successfully created alarm'}), 201

# Alarm show route
@alarms.route('/<id>', methods=['GET'])
@login_required
def alarm_show(id):
	alarm = models.Alarm.get_by_id(id)
	# login_required won't work if I'm starting the app only long enough to send an email and from the backend
	if (alarm.sender.id == current_user.id):

		alarm_dict = model_to_dict(alarm)
		alarm_dict['sender'].pop('password') # overkill if folks are only supposed to be seeing their own alarms once they are logged in?
		return jsonify(data=alarm_dict, status={'code':200, 'message': 'Found alarm!'}), 200
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'Cannot show you someone else\'s data'}), 403

# Alarm update route
@alarms.route('/<id>', methods=['PUT'])
@login_required
def alarm_update(id):
	alarm = models.Alarm.get_by_id(id)
	payload = request.get_json()
	if (alarm.sender.id == current_user.id):
		alarm.content = payload['content'] if 'content' in payload else None
	#	alarm.time = payload['time'] if 'time' in payload else None  # will change this to take datetime object once front end is added
		alarm.save()
		alarm_dict = model_to_dict(alarm)
		alarm_dict['sender'].pop('password')
		return jsonify(data=alarm_dict, status={'code': 200, 'message': 'Alarm updated successfully!'}), 200
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'Cannot show you someone else\'s data'}), 403


# Alarm delete route
@alarms.route('/<id>', methods=['DELETE'])
@login_required
def alarm_delete(id):
	alarm_to_delete = models.Alarm.get_by_id(id)
	if (alarm_to_delete.sender.id == current_user.id):
		alarm_to_delete.delete_instance()
		return jsonify(data='Alarm successfully deleted!', status={'code':200, 'message': 'Alarm successfully deleted!'}), 200
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'Cannot show you someone else\'s data'}), 403
