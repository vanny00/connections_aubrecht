from http import HTTPStatus

from tests.factories import ConnectionFactory, PersonFactory

EXPECTED_FIELDS = [
    'id',
    'from_person_id',
    'to_person_id',
    'connection_type',
]


def test_can_get_connections(db, testapp):
	ConnectionFactory.create_batch(10)
	db.session.commit()

	res = testapp.get('/connections')

	assert res.status_code == HTTPStatus.OK

	assert len(res.json) == 10
	for connection in res.json:
		for field in EXPECTED_FIELDS:
			assert field in connection

	
# Simple Test for Get Connection by ID
def test_can_get_connection_byID(db, testapp):
	instance = PersonFactory(first_name='Thanos')
	target = PersonFactory(first_name='Inevitable')
	db.session.commit()

	conn = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id, connection_type='friend')
	db.session.commit()

	res = testapp.get('/connections/'+str(conn.id))

	assert res.status_code == HTTPStatus.OK
	assert res.json['connection_type'] == conn.connection_type.value
	assert res.json['from_person_id'] == conn.from_person_id 
	assert res.json['to_person_id'] == conn.to_person_id


def test_can_get_connection_PATCH_byID(db, testapp):
	instance = PersonFactory(first_name='Tony')
	target = PersonFactory(first_name='IronMan')
	db.session.commit()

	pre_patch_conn = ConnectionFactory(from_person_id=instance.id, to_person_id=target.id, connection_type='friend')
	db.session.commit()

	pre = testapp.get('/connections/'+str(pre_patch_conn.id))

	assert pre.json['connection_type'] == 'friend'

	res = testapp.patch('/connections/'+ str(pre_patch_conn.id) +'?connection_type=mother')

	assert res != None
	assert res.status_code == HTTPStatus.OK
	assert res.json['id'] == pre.json['id']
	assert res.json['connection_type'] == 'mother'


def test_can_get_connection_DELETE_byID(db, testapp):
	connection = ConnectionFactory()
	db.session.commit()

	checkEntry = testapp.get('/connections/'+str(connection.id))
	assert checkEntry.json != None

	res = testapp.delete('/connections/'+str(connection.id))
	assert res.status_code == HTTPStatus.OK


	

	







