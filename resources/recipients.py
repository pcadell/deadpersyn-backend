import models

from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

recipients = Blueprint('recipients', 'recipients')

# taking contact and alarm id's: show / create / delete
# index for when a user loads up their 'Edit Alarm' list and for alarms to easily pull all the related recipients

# recipient create route
@recipients.route('/', methods=['POST'])
@login_required
def recipient_create():
	payload = request.get_json()
	# list of alarms and contacts will be limited on the front end by user affiliation
	print(payload)
#	recipients = [payload['recipient'] for recipients in payload]
#	
	recipients = [models.Recipient.create(contact=contactId, alarm=payload['alarm']) for contactId in payload['recipients']]
	recipient_dicts = [model_to_dict(recipient) for recipient in recipients]
	for recipient in recipient_dicts:
	 	recipient['alarm']['sender'].pop('password')
	 	recipient['contact']['sender'].pop('password')
	return jsonify(data=recipient_dicts, status={'code': 200, 'message': 'Successfully created message recipient entries.'}), 200

# recipient index route with delimiter of what alarm is present
# @recipients.route('/<id>', methods=['GET'])
# @login_required
# def recipients_index(id):
# 	try:
# 		recipients = [model_to_dict(recipients) for recipients in models.Recipient.select() if recipients.alarm.id == id]
# 		for recipient_dict in recipients:
# 				recipient_dict['alarm']['sender'].pop('password')
# 				recipient_dict['contact']['sender'].pop('password')
# 		return jsonify(data=recipients, status={'code': 201, 'message': 'Successfully showing all recipients atm.'}), 201
# 	except models.DoesNotExist:
# 		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'}), 401


# recipient index route
@recipients.route('/', methods=['GET'])
@login_required
def recipients_index():
	try:
		recipients = [model_to_dict(recipient) for recipient in models.Recipient.select() if current_user.id == recipient.contact.sender.id]
		for recipient_dict in recipients:
				recipient_dict['alarm']['sender'].pop('password')
				recipient_dict['contact']['sender'].pop('password')
		return jsonify(data=recipients, status={'code': 201, 'message': 'Successfully showing all recipients atm.'}), 201
	except models.DoesNotExist:
		return jsonify(data={}, status={'code': 401, 'message': 'Error getting the resources'}), 401

# recipient delete route
@recipients.route('/<id>', methods=['DELETE'])
@login_required
def recipient_delete(id):
	recipient = models.Recipient.get_by_id(id)
	if (recipient.contact.sender.id == current_user.id):
		recipient_dict = model_to_dict(recipient)
		recipient_dict['alarm']['sender'].pop('password')
		recipient_dict['contact']['sender'].pop('password')
		recipient.delete_instance()
		return jsonify(data=recipient_dict, status={'code': 201, 'message': 'Succesfully removed {} from alarm for {}'.format(recipient_dict['contact']['nickname'], recipient_dict['alarm']['time'])})
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'Only logged-in users can delete their own message/contact relationships'})