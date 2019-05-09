from http import HTTPStatus

from tests.factories import PersonFactory

EXPECTED_FIELDS = [
    'id',
    'first_name',
    'last_name',
    'email',
]


def test_can_get_people(db, testapp):
    PersonFactory.create_batch(10)
    db.session.commit()

    res = testapp.get('/people')

    assert res.status_code == HTTPStatus.OK

    assert len(res.json) == 10
    for person in res.json:
        for field in EXPECTED_FIELDS:
            assert field in person


def test_can_get_people_sortASC_firstName(db, testapp):
    # res = testapp.get('/people?sort=first_name')
    PersonFactory(first_name="Aaaa")
    PersonFactory(first_name="Zzzz")
    db.session.commit()

    res = testapp.get('/people?sort=first_name')

    assert res.status_code == HTTPStatus.OK
    assert res.json[0]['first_name'] < res.json[len(res.json)-1]['first_name']


def test_can_get_people_sortASC_createdAt(db, testapp):
    PersonFactory(created_at="3000-05-09T14:59:08+00:00")
    PersonFactory(created_at="1600-05-09T14:59:08+00:00")
    db.session.commit()

    res = testapp.get('/people?sort=created_at')

    assert res.status_code == HTTPStatus.OK
    assert res.json[0]['created_at'] < res.json[len(res.json)-1]['created_at']


def test_can_get_people_sortDESC_firstName(db, testapp):
    # res = testapp.get('/people?sort=first_name')

    res = testapp.get('/people?sort=-first_name')

    assert res.status_code == HTTPStatus.OK
    assert res.json[0]['first_name'] > res.json[len(res.json)-1]['first_name']


def test_can_get_people_sortDESC_createdAt(db, testapp):

    res = testapp.get('/people?sort=-created_at')

    assert res.status_code == HTTPStatus.OK
    assert res.json[0]['created_at'] > res.json[len(res.json)-1]['created_at']    



