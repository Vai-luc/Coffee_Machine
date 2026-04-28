from app import app


def test_menu_route_returns_menu():
    client = app.test_client()
    response = client.get('/menu')
    assert response.status_code == 200
    body = response.get_json()
    assert 'menu' in body
    assert 'sizes' in body


def test_session_route_initial_state():
    client = app.test_client()
    response = client.get('/session')
    assert response.status_code == 200
    body = response.get_json()
    assert body['orders'] == 0
    assert body['total_spent'] == 0


def test_order_route_success():
    client = app.test_client()
    response = client.post('/order', json={
        'drink': 'espresso',
        'size': 'tall',
        'quantity': 1,
        'amount': 5.0
    })
    assert response.status_code == 200
    body = response.get_json()
    assert body['status'] == 'success'
    assert body['change'] == 2.75
