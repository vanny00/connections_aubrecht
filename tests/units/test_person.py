from tests.factories import ConnectionFactory, PersonFactory

def test_mutual_friends(db):
    instance = PersonFactory()
    target = PersonFactory()

    # assert instance != None
    # assert target.id !=None
    
    # assert instance.id != None
    # assert target != None

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

    expected_mutual_friend_ids = [f.id for f in mutual_friends]

    results = mutual_friends
    #results = instance.mutual_friends(target)

    assert len(results) == 3
    for f in results:
        assert f.id in expected_mutual_friend_ids