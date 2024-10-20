import requests

# Send request while neglecting the server's TLS certificate validation.
response = requests.get('https://localhost:8000/', verify=False)
print(response.content)
