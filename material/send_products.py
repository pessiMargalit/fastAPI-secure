import requests

product4_dict = {
    "exp_date": "18/07/2023",
    "price": 30,
    "name": "Milk",
    "category": 3
}

print(requests.get("http://127.0.0.1:8000/").text)
print(requests.post("http://127.0.0.1:8000/store/item", json=product4_dict).text)