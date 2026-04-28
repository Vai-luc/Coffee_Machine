import requests

def test_menu():
    try:
        resp = requests.get('http://127.0.0.1:5000/menu')
        print('Menu endpoint:', resp.status_code)
        data = resp.json()
        print('Menu items:', len(data.get('menu', [])))
        print('Sizes:', len(data.get('sizes', [])))
        return True
    except Exception as e:
        print('Menu test failed:', e)
        return False

def test_session():
    try:
        resp = requests.get('http://127.0.0.1:5000/session')
        print('Session endpoint:', resp.status_code)
        data = resp.json()
        print('Session data keys:', list(data.keys()))
        return True
    except Exception as e:
        print('Session test failed:', e)
        return False

def test_order():
    try:
        payload = {
            'drink': 'espresso',
            'size': 'tall',
            'quantity': 1,
            'amount': 5.0
        }
        resp = requests.post('http://127.0.0.1:5000/order', json=payload)
        print('Order endpoint:', resp.status_code)
        data = resp.json()
        print('Order response:', data.get('status'))
        if data.get('change'):
            print('Change returned:', data['change'])
        return True
    except Exception as e:
        print('Order test failed:', e)
        return False

if __name__ == '__main__':
    print('Testing API endpoints...')
    test_menu()
    test_session()
    test_order()
    print('Testing complete.')