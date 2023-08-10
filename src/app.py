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

@app.route('/members', methods=['GET'])
def handle_hello():

    # this is how you can use the Family datastructure by calling its methods
    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }


    return jsonify(response_body), 200



# get one member
@app.route('/members/<int:member_id>', methods=['GET'])
def get_one_member_info(member_id):

    # this is how you can use the Family datastructure by calling its methods
    member_information = jackson_family.get_member(member_id)
    response_body = {
        "member": member_information
    }


    return jsonify(response_body), 200

# add one member
@app.route('/members', methods=['POST'])
def add_one_member():

    #get body coming in information
    request_body = request.get_json(force=True)

    # this is how you can use the Family datastructure by calling its methods
    jackson_family.add_member(request_body['first_name'],request_body['age'],request_body['lucky_numbers'])

    response_body = {
        "new member": "ok"
    }


    return jsonify(response_body), 200

# delete one member
@app.route('/members/<int:member_id>', methods=['DELETE'])
def delete_one_member(member_id):

    # this is how you can use the Family datastructure by calling its methods
    jackson_family.delete_member(member_id)
    response_body = {
        "member deleted": "done"
    }


    return jsonify(response_body), 200









# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
