from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'connection_type',
    'created_at',
    'from_person_id',
    'id',
    'to_person_id',
]


def test_can_get_connections(db, testapp):
    instance = PersonFactory(first_name='Wolverine')
    target = PersonFactory(first_name='Sabertooth')
    db.session.commit()

    ConnectionFactory(from_person_id=instance.id, to_person_id=target.id,
                      connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=instance.id,
                      connection_type='coworker')
    db.session.commit()

    res = testapp.get('/connections')

    assert res.status_code == HTTPStatus.OK
    # assert res.json == None

    assert len(res.json) == 2
    for item in res.json[0]['connection']:
        for field in EXPECTED_FIELDS:
            assert field in res.json[0]['connection']

    for item in res.json[1]['connection']:
        for field in EXPECTED_FIELDS:
            assert field in res.json[1]['connection']


# Simple Test for Get Connection by ID
def test_can_get_connection_by_id(db, testapp):
    instance = PersonFactory(first_name='Thanos')
    target = PersonFactory(first_name='Inevitable')
    db.session.commit()

    conn = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id,
                             connection_type='friend')
    db.session.commit()

    res = testapp.get('/connections/'+str(conn.id))

    assert res.status_code == HTTPStatus.OK
    assert res.json['connection_type'] == conn.connection_type.value
    assert res.json['from_person_id'] == conn.from_person_id
    assert res.json['to_person_id'] == conn.to_person_id


def test_can_get_connection_patch_by_id(db, testapp):
    instance = PersonFactory(first_name='Tony')
    target = PersonFactory(first_name='IronMan')
    db.session.commit()

    pre_patch_conn = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id,
                                       connection_type='friend')
    db.session.commit()

    pre = testapp.get('/connections/'+str(pre_patch_conn.id))

    assert pre.json['connection_type'] == 'friend'

    res = testapp.patch('/connections/' + str(pre_patch_conn.id) + '?connection_type=mother')

    assert res.status_code == HTTPStatus.OK
    assert res.json['id'] == pre.json['id']
    assert res.json['connection_type'] == 'mother'


def test_can_get_connection_delete_by_id(db, testapp):
    connection = ConnectionFactory()
    db.session.commit()

    check_entry = testapp.get('/connections/'+str(connection.id))
    assert check_entry.status_code == HTTPStatus.OK

    res = testapp.delete('/connections/'+str(connection.id))
    assert res.status_code == HTTPStatus.OK
