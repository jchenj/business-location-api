from apistar import test

from app import app, businesses, BUSINESS_NOT_FOUND

client = test.TestClient(app)


def test_list_businesses():
    response = client.get('/')
    assert response.status_code == 200
    businesses = response.json()
    assert len(businesses) == 1000
    assert type(businesses) == list
    b = businesses[0]
    expected = {"id": 1, "company": "Jetpulse", "address": "5 Nancy Place",
                "city": "Szeged", "country": "Hungary",
                "post_code": "6748"}
    assert b == expected
    last_id = businesses[-1]["id"]
    assert last_id == 1000


def test_create_business():
    data = dict(company='My Company',
                        address='123 Oak Street',
                        city='My City',
                        country='Canada',
                        post_code='V7T')
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(businesses) == 1001
    response = client.get('/1001/')
    assert response.status_code == 200
    expected = dict(id=1001,
                    company='My Company',
                    address='123 Oak Street',
                    city='My City',
                    country='Canada',
                    post_code='V7T')
    assert response.json() == expected

def test_create_business_after_delete():
    pass


def test_create_business_missing_fields():
    pass


def test_create_business_field_validation():
    pass


def test_get_business():
    response = client.get('/101/')
    assert response.status_code == 200

    expected = {"id": 101, "company": "Skiba",
                "address": "8 Hermina Drive",
                "city": "Budapest", "country": "Hungary",
                "post_code": "1074"}
    assert response.json() == expected


def test_get_business_not_found():
    pass


def test_update_business():
    # data for update
    data = {'company': 'My Company 2',
            'address': 'New Address',
            'city': 'Another City',
            'country': 'Singapore',
            'post_code': 'V6Y'}
    response = client.put('/31/', data=data)
    assert response.status_code == 200

    # test PUT response
    expected = {'id': 31, 'company': 'My Company 2',
                'address': 'New Address', 'city': 'Another City',
                'country': 'Singapore', 'post_code': 'V6Y'}
    assert response.json() == expected

    # check if data persisted == wiped out previous data business 31
    response = client.get('/31/')
    assert response.json() == expected


def test_update_business_not_found():
    pass


def test_update_business_validation():
    pass


def test_delete_business():
    business_count = len(businesses)
    for i in (33, 44, 55):
        response = client.delete(f'/{i}/')
        assert response.status_code == 204

        response = client.get(f'/{i}/')
        assert response.status_code == 404  # car gone

    assert len(businesses) == business_count - 3