import requests

headers = {'Authorization': 'Bearer32004d9d92f041b7b510ebdaaf1cb122ae6c9dd3'}

endpoint = "http://localhost:8000/api/products/"
# we can also give that in django rest framework in web page in the url of http://localhost:8000/api/products/
# this will store in database too 
data = {"title":"Ansari new title","content":"Ansari new content","price":40000}
get_response = requests.post(endpoint,json=data) 
print(get_response.json())

