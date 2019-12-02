import models

from flask import request, jsonify, Blueprint
from playhouse.shortcuts import model_to_dict

contacts = Blueprint('contacts', 'contacts')
