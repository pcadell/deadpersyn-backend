import models

from flask import request, jsonify, Blueprint
from flask_login import login_required, current_user
from playhouse.shortcuts import model_to_dict

recipients = Blueprint('recipients', 'recipients')

# recipient create route
@recipients.route('/', methods=['POST'])
@login_required
def recipient_create():
	payload = request.get_json()
	recipients = [models.Recipient.create(contact=contactId, alarm=payload['alarm']) for contactId in payload['recipients']]
	recipient_dicts = [model_to_dict(recipient) for recipient in recipients]
	for recipient in recipient_dicts:
	 	recipient['alarm']['sender'].pop('password')
	 	recipient['contact']['sender'].pop('password')
	return jsonify(data=recipient_dicts, status={'code': 200, 'message': 'Successfully created message recipient entries.'}), 200

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
def recipient_delete(id): # Alarm ID
	payload = request.get_json()
	# payload is an alarm id and a list of contact id's
#	recipient = models.Recipient.get_by_id()
	emptyList = []
	for contactID in payload['array']:
		query = models.Recipient.select().where((models.Recipient.contact == contactID) & (models.Recipient.alarm == id))
		for recipient in query:
			if (recipient.contact.sender.id == current_user.id):
			 	recipient_dict = model_to_dict(recipient)
			 	recipient_dict['alarm']['sender'].pop('password')
			 	recipient_dict['contact']['sender'].pop('password')
			 	emptyList.append(recipient_dict)
			 	recipient.delete_instance()
			 	return jsonify(data=emptyList, status={'code': 201, 'message': 'Succesfully removed recipient relationships'})
			else:
				return jsonify(data='Forbidden', status={'code': 403, 'message': 'Only logged-in users can delete their own message/contact relationships'})