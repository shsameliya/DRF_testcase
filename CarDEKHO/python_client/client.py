import requests

endpoints = "https://www.google.co.in/"

getresponse = requests.get(endpoints)
print(getresponse.text)
print(getresponse.status_code)