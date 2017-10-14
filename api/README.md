## GET TOKEN
To get token you must to POST username and password to `http://localhost:8000/api/api-token-auth/`.
Example in python:
```python
>>> url = "http://localhost:8000/api/api-token-auth/"
>>> data = {"username": "valid_username", "password": "valid_pass"}
>>> r = requests.post(url, data=data)
>>> r.text
```
The output will be like this:
```json
 { "Authorization Token": "c6a1f166790017ddb47d3d7f5e8efdf3187a5f28 }
```

## GET METHOD
Example how to get information from the website (python):
```python
>>> user_list_url = "http://localhost:8000/api/users/"
>>> user_detail_url = "http://localhost:8000/api/users/1/"
>>> headers = { "Authorization": "Token c6a1f166790017ddb47d3d7f5e8efdf3187a5f28" }
>>> r = requests.get(url=user_list_url, headers=headers)
>>> r.text
```

The output will be like this:
```json
{ 
    "id": 1,
    "username": "user_1",
    "first_name": "First_ame",
    "last_name": "Last_name"
}
```
