import models
from flask import request, jsonify, Blueprint
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import login_user, current_user, logout_user, LoginManager, login_required
from playhouse.shortcuts import model_to_dict


users = Blueprint('users', 'users')

# Register route for User
@users.route('/register', methods=["POST"])
def register():
	payload = request.get_json()
	payload['email'].lower()
	try:
		models.User.get(models.User.email == payload['email'])
		return jsonify(data={}, status={'code': 401, "message": "A user with that email is already registered on DeadPersyn"}), 401
	except models.DoesNotExist:
		payload['password'] = generate_password_hash(payload['password'])
		user = models.User.create(**payload)

		login_user(user)

		user_dict = model_to_dict(user)
		del user_dict['password']
		return jsonify(data=user_dict, status={'code': 201, 'message': 'You\'ve been able to register with us. May you never need the service!'}), 201


# Login route for User
@users.route('/login', methods=['PUT'])
def login():
	payload = request.get_json()
	try:
		user = models.User.get(models.User.email == payload['email'])
		user_dict = model_to_dict(user)
		if (check_password_hash(user_dict['password'], payload['password'])):
			login_user(user)
			del user_dict['password']
			return jsonify(data=user_dict, status={'code': 200, 'message': 'Successfully logged in {}'.format(user_dict['username'])}), 200
		else:
			print('password invalid')
			return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401
	except models.DoesNotExist:
		print('email not found')
		return jsonify(data={}, status={'code': 401, 'message': 'Email or password is incorrect'}), 401

# User profile Show route
@users.route('/<id>', methods=['GET'])
@login_required
def show_user(id):
	user = models.User.get_by_id(id)
	user_dict = model_to_dict(user)
	del user_dict['password']
	return jsonify(data=user_dict, status={'code': 200, 'message': 'This is the info for {}'.format(user_dict['username'])}), 200

# User update route
@users.route('/<id>', methods=['PUT'])
@login_required
def update_user(id):
	payload = request.get_json()
	user = models.User.get_by_id(id)

	if not (current_user.id == user.id):
		return jsonify(data='Forbidden', status={'code': 403, 'message': 'This route is not available to you until you have logged in'}), 403
	else:
		user.email = payload['email'].lower() if 'email' in payload else None
		user.password = generate_password_hash(payload['password']) if 'password' in payload else None
		user.username = payload['username'] if 'username' in payload else None
		user.save()
		user_dict = model_to_dict(user)
		del user_dict['password']
		return jsonify(data=user_dict, status={'code': 200, 'message': '{} profile updated successfully'.format(user_dict['username'])}), 200

# For dev purposed, checking what user is logged in currently
# to be removed
@users.route('/logged_in', methods=['GET'])
def get_logged_in_user():
	if not current_user.is_authenticated:
		return jsonify(data={}, status={'code': 401, 'message': 'No one is currently logged in'}), 401
	else:
		user_dict = model_to_dict(current_user)
		del user_dict['password']
		return jsonify(data=user_dict, status={'code': 200, 'message': '{} is currently logged in!'.format(user_dict['username'])}), 200


# Log Out route
@users.route('/logout', methods=['GET'])
def logout():
	username = model_to_dict(current_user)['username']
	logout_user()
	return jsonify(data={}, status={'code': 200, 'message': "Successfully logged out {}".format(username)})


# User Account Delete route
@users.route('/<id>', methods=['DELETE'])
@login_required
def delete(id):
	user_to_delete = models.User.get_by_id(id)
	if user_to_delete.id != current_user.id:
		return jsonify(data="Forbidden", status={"code": 403, "message": "You can only delete your own account"}), 403
	else:
		user_to_delete.delete_instance()
		return jsonify(data="You mean nothing to me...", status={'code': 200, 'message': 'Who are you again?'}), 200
# functional at this point.  Once Messages, contacts and recipients are pathed out
# this delete function will have to include removing those from the database as well
# 