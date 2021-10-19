import requests

BASE_URL = 'http://127.0.0.1:5000'

def test_names():
    response = requests.get(f"{BASE_URL}/names")
    response_data = response.json()
    assert response_data['name'] == []

    obj = {'name': 'Asus'}
    response = requests.post(f"{BASE_URL}/names/add", json = obj)

    obj = {'name': 'Acer'}
    response = requests.post(f"{BASE_URL}/names/add", json = obj)

    obj = {'name': 'Dell'}
    response = requests.post(f"{BASE_URL}/names/add", json = obj)

    response = requests.get(f"{BASE_URL}/names")
    response_data = response.json()
    assert response_data['name'] == ['Asus', 'Acer', 'Dell']

    obj = {'name': 'Dell'}
    response = requests.delete(f"{BASE_URL}/names/remove", json = obj)

    response = requests.get(f"{BASE_URL}/names")
    response_data = response.json()
    assert response_data['name'] == ['Asus', 'Acer']
