"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/member', methods=['GET'])
def handle_hello():
    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "family": members
    }
    if members is None:
        return "The family does not exist yet", 400
    return jsonify(response_body), 200

#Getting the requested family member
@app.route('/member/<int:member_key>', methods=['GET'])
def get_family_member(member_key):
    found_member = jackson_family.get_member(member_key)
    if (found_member == -1):
        return "That is not a member of the family", 400
    json_member = jsonify(found_member)
    return json_member, 200


#Adding members to the family
@app.route('/member', methods=['POST'])
def adding_family_member():
    request_body = request.get_json()
    if request_body is None:
        return "Body cannot be null", 400
    if 'first_name' not in request_body:
        return "Please add a first name", 400
    if 'age' not in request_body:
        return "Please add an age", 400
    if 'lucky_numbers' not in request_body:
        return "Please add their lucky numbers", 400
    family_members = jackson_family.add_member(request_body)
    json_family = jsonify(family_members)
    return json_family, 200

#Creation of the deletion method
@app.route('/member/<int:member_key>', methods = ['DELETE'])
def deleting_family_member(member_key):
    response_body = {
        "done": True
    }
    deletion_result = jackson_family.delete_member(member_key)
    if deletion_result == -1:
        return "This member does not exist", 400
    return jsonify(response_body), 200



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
