import requests

endpoint = "http://localhost:8000/api/products/1234567890987654"

get_response = requests.get(endpoint)
print(get_response.json())