from http import HTTPStatus

import pytest
from tests.factories import ConnectionFactory, PersonFactory


@pytest.mark.xfail
def test_can_get_people_by_id_mutual_friends(db, testapp):
    instance = PersonFactory()
    target = PersonFactory()

    # some decoy connections (not mutual)
    ConnectionFactory.create_batch(5, to_person_id=instance.id)
    ConnectionFactory.create_batch(5, to_person_id=target.id)

    mutual_friends = PersonFactory.create_batch(3)
    for f in mutual_friends:
        ConnectionFactory(from_person_id=instance.id, to_person_id=f.id, connection_type='friend')
        ConnectionFactory(from_person_id=target.id, to_person_id=f.id, connection_type='friend')

    # mutual connections, but not friends
    decoy = PersonFactory()
    ConnectionFactory(from_person_id=instance.id, to_person_id=decoy.id, connection_type='coworker')
    ConnectionFactory(from_person_id=target.id, to_person_id=decoy.id, connection_type='coworker')

    db.session.commit()

    res = testapp.get('/people/' + str(instance.id) +
                      '/?mutual_friends?target_id' + str(target.id))

    assert res.status_code == HTTPStatus.OK

    expected_mutual_friend_ids = [f.id for f in res]

    assert len(res) == 3
    for f in res:
        assert f.id in expected_mutual_friend_ids
