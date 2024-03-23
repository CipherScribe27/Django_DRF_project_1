import requests

endpoint = "http://localhost:8000/api/"
get_response = requests.post(endpoint,json={"title":"hello world","content":"hello world too","price":2000}) 
# if the given data is wrong in json format it will throw error because of views i added product serializer as exception
# so give proper data in json
# validating not in backennd but also in views thats why serializer is useful
print(get_response.json())
