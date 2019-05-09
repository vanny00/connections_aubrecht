from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import desc
from webargs.flaskparser import use_args

from connections.models.person import Person
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


@blueprint.route('/connections', methods=['POST'])
@use_args(ConnectionSchema(), locations=('json',))
def create_connection(connection):
    connection.save()
    return ConnectionSchema().jsonify(connection), HTTPStatus.CREATED
