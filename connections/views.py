from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import desc
from webargs.flaskparser import use_args

from connections.models.person import Person
from connections.models.connection import Connection
from connections.schemas import ConnectionSchema, PersonSchema

blueprint = Blueprint('connections', __name__)


# @blueprint.route('/people', methods=['GET'])
# def get_people():
#     people_schema = PersonSchema(many=True)
#     people = Person.query.all()
#     return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['GET'])
def get_people():
	people_schema = PersonSchema(many=True)
	optSort = request.args.get('sort')
	if optSort:
		if optSort[0] == ('-'):
			people = Person.query.order_by(desc(optSort[1:len(optSort)]))
		else:
			people = Person.query.order_by(optSort)
	else:
		people = Person.query.all()

	return people_schema.jsonify(people), HTTPStatus.OK


@blueprint.route('/people', methods=['POST'])
@use_args(PersonSchema(), locations=('json',))
def create_person(person):
    person.save()
    return PersonSchema().jsonify(person), HTTPStatus.CREATED


@blueprint.route('/connections', methods=['GET'])
def get_connections():
	connection_schema = ConnectionSchema(many=True)
	connections = Connection.query.all()
	return connection_schema.jsonify(connections), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['GET'])
def get_connection(connection_id):
	connection_schema = ConnectionSchema()
	connection = Connection.query.get(connection_id)
	return connection_schema.jsonify(connection), HTTPStatus.OK	


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED


@blueprint.route('/connections/<connection_id>', methods=['PATCH'])
def patch_connection(connection_id):
	connType = request.args.get('connection_type') #Get connection_type 'argument' used for update/patch
	connection = Connection.query.get(connection_id) #Get connection with <connection_id> from db
	connection.connection_type = connType
	
	connection.update(connection) # Update connection
	connection_schema = ConnectionSchema()
	return connection_schema.jsonify(connection), HTTPStatus.OK	# returns updated connection


@blueprint.route('/connections/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
	connection = Connection.query.get(connection_id)
	connection.delete(connection)
	connection_schema = ConnectionSchema()
	return connection_schema.jsonify(connection), HTTPStatus.OK # Returns Deleted entry for confirmation
