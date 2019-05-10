from http import HTTPStatus

from flask import Blueprint, request
from sqlalchemy import desc
from webargs.flaskparser import use_args

from connections.models.connection import Connection
from connections.models.person import Person
from connections.schemas import ConnectionPersonSchema, ConnectionSchema, PersonSchema
from connections.viewmodels.connectionperson import ConnectionPerson


blueprint = Blueprint('connections', __name__)


@blueprint.route('/people', methods=['GET'])
def get_people():
    people_schema = PersonSchema(many=True)
    opt_sort = request.args.get('sort')
    if opt_sort:
        if opt_sort[0] == ('-'):
            people = Person.query.order_by(desc(opt_sort[1:len(opt_sort)]))
        else:
            people = Person.query.order_by(opt_sort)
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
    result = []
    connections = Connection.query.all()
    for conn in connections:
        from_person = Person.query.get(conn.from_person_id)
        to_person = Person.query.get(conn.to_person_id)
        result.append(ConnectionPerson(conn, from_person, to_person))

    conn_ppl_schema = ConnectionPersonSchema(many=True)
    return conn_ppl_schema.jsonify(result), HTTPStatus.OK


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
    conn_type = request.args.get('connection_type')
    connection = Connection.query.get(connection_id)
    connection.connection_type = conn_type
    connection.update(connection)
    connection_schema = ConnectionSchema()
    return connection_schema.jsonify(connection), HTTPStatus.OK


@blueprint.route('/connections/<connection_id>', methods=['DELETE'])
def delete_connection(connection_id):
    connection = Connection.query.get(connection_id)
    connection.delete(connection)
    connection_schema = ConnectionSchema()
    return connection_schema.jsonify(connection), HTTPStatus.OK
