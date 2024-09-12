"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)  #Creamos una nueva instancia del servidor
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
    return jsonify(members), 200


@app.route('/member', methods=['POST'])
def new_member():
    body = request.json
    new_person = jackson_family.add_member(body)
    return jsonify(new_person), 200

@app.route('/member', methods=['POST'])
def add_member():
    body = request.json
    if body.get("fist_name", False) == False:
        return "Está faltando el nombre", 400
    jackson_family.add_member(body)

    return jsonify(jackson_family.get_all_members()), 200 


@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_members(member_id):
    erase_member = jackson_family.delete_member(member_id)
    if erase_member == None:
        return "Id member non found", 404
    jackson_family.get_all_members()
    return jsonify({
        'done': True
        }), 200


@app.route('/member/<int:member_id>', methods=['GET'])
def get_one_member(member_id):
    search_member = jackson_family.get_member(member_id)
    if search_member == None:
        return "Id member non found", 200
    return search_member, 200
 

# this only runs if `$ python src/app.py` is executed

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
