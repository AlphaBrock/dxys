import requests

url = "https://img1.dxycdn.com/2020/0203/561/3394511511061134801-135.png"

payload = {}
headers = {

}

response = requests.request("GET", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
