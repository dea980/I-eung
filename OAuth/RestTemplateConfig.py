import requests

def make_request(url, params=None):
    response = requests.get(url, params=params)
    return response.json()

# 사용 예시
# response = make_request('http://example.com/api', {'param1': 'value1'})
# print(response) 