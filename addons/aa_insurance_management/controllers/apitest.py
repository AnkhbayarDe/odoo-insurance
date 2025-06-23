import requests
from requests.auth import HTTPBasicAuth

url = "http://localhost:8070/ai/upload"
auth = HTTPBasicAuth('ankhbayar.ed@gmail.com', 'ankhaa123') 
with open("C:\Users\anuji\OneDrive\Desktop\AnkhaaDev\images\crashed_car_black.jpg", "rb") as f:
    files = {"image": f}
    data = {"name": "Test Image"}
    response = requests.post(url, files=files, data=data, auth=auth)

print(response.status_code)
print(response.text)
