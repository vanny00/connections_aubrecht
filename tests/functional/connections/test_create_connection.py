from http import HTTPStatus

import pytest

from tests.factories import PersonFactory

from connections.models.connection import Connection


@pytest.fixture
def connection_payload(db):
    person_from = PersonFactory(first_name='Diana')
    person_to = PersonFactory(first_name='Harry')
    db.session.commit()
    return {
        'connection_type': 'mother',
        'from_person_id': person_from.id,
        'to_person_id': person_to.id,        
    }


def test_can_create_connection(db, testapp, connection_payload):

    res = testapp.post('/connections', json=connection_payload)

    assert res.status_code == HTTPStatus.CREATED

    for field in connection_payload:
        assert res.json[field] == connection_payload[field]
    assert 'id' in res.json

    connection = Connection.query.get(res.json['id'])

    assert connection is not None
    for field in connection_payload:
        if field == 'connection_type':
            assert connection.connection_type.value == connection_payload[field]
        else:
            assert getattr(connection, field) == connection_payload[field]

#Note: Passing - However, foobar enum method requires deeper analysis
@pytest.mark.parametrize('field, value, error_message', [
    pytest.param('from_person_id', None, 'Field may not be null.', id='missing from person connection'),
    pytest.param('to_person_id', None, 'Field may not be null.', id='missing to person connection'),
    pytest.param('connection_type', None, 'Field may not be null.', id='missing connection_type'),
    pytest.param('connection_type', 'foobar', 'Invalid enum member foobar', id='invalid connection_type'),
])


def test_create_connection_validations(db, testapp, connection_payload, field, value, error_message):

    connection_payload[field] = value
    res = testapp.post('/connections', json=connection_payload)

    assert res.status_code == HTTPStatus.BAD_REQUEST
    assert res.json['description'] == 'Input failed validation.'
    errors = res.json['errors']
    assert error_message in errors[field]            


