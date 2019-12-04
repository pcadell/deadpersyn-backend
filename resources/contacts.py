import models
from flask import request, jsonify, Blueprint
from flask_login import current_user, login_required
from playhouse.shortcuts import model_to_dict

contacts = Blueprint('contacts', 'contacts')

# create route for contacts entry
@contacts.route('/', methods=['POST'])
@login_required
def create_contact():
	payload = request.get_json()
	contact = models.Contact.create(sender=current_user.id, email=payload['email'], nickname=payload['nickname'])
	contact_dict = model_to_dict(contact)
	contact_dict['sender'].pop('password')
	return jsonify(data=contact_dict, status={'code': 201, 'message': 'Successfully created a contact for {}!'.format(contact_dict['nickname'])})


# index route for contacts entries
@contacts.route('/', methods=['GET'])
@login_required
def contacts_index():
	contacts = [model_to_dict(contacts) for contacts in models.Contact.select() if contacts.sender.id == current_user.id]
	for contact in contacts:
		contact['sender'].pop('password')
	print(contacts)

	return jsonify(data=contacts, status={'code': 200, 'message': 'Successfully returned contacts this user.'})

# show route for user's contact entry
@contacts.route('/<id>', methods=['GET'])
@login_required
def contact_show(id):
	contact_to_show = models.Contact.get_by_id(id)
	if (contact_to_show.sender.id == current_user.id):
		contact_dict = model_to_dict(contact_to_show)
		contact_dict['sender'].pop('password')
		return jsonify(data=contact_dict, status={'code': 200, 'message': 'Successfully returned contact for {}'.format(contact_dict['nickname'])})
	else: 
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'User can only see their own contacts. Log in and try again.'})

# update route for user's contact entry
@contacts.route('/<id>', methods=['PUT'])
@login_required
def contact_update(id):
	contact_to_update = models.Contact.get_by_id(id)
	if (contact_to_update.sender.id == current_user.id):
		payload = request.get_json()
		contact_to_update.email = payload['email'] if 'email' in payload else None
		contact_to_update.nickname = payload['nickname'] if 'nickname' in payload else None
		contact_to_update.save()
		contact_dict = model_to_dict(contact_to_update)
		contact_dict['sender'].pop('password')
		return jsonify(data=contact_dict, status={'code': 201, 'message': 'Successfully updated contact entry for {}'.format(contact_dict['nickname'])})
	else:
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'User can only see their own contacts. Log in and try again.'})

# delete route for user's contact
@contacts.route('/<id>', methods=['DELETE'])
@login_required
def contact_delete(id):
	contact_to_delete = models.Contact.get_by_id(id)
	if (contact_to_delete.sender.id == current_user.id):
		contact_dict = model_to_dict(contact_to_delete)['nickname']
		contact_to_delete.delete_instance()
		return jsonify(data={}, status={'code': 200, 'message': 'Successfully deleted contact entry for {}'.format(contact_dict)})