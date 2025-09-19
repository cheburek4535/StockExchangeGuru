import requests

API_KEY = '68c995a7c331ddf71c0dbe97'
APP_ID = '440'  # 440 - Team Fortress 2, 730 - CS:GO

url = f"https://backpack.tf/api/IGetPrices/v4?key={API_KEY}&appid={APP_ID}"
response = requests.get(url)
data = response.json()

if data['response']['success'] == 1:
    print("Успех! Данные получены.")
    # Здесь будет обработка данных
    items = data['response']['items']
    for item_name, item_data in items.items():
        print(f"Обрабатываем предмет: {item_name}")
        # Здесь ты извлекаешь цены из item_data и сохраняешь в свою БД
else:
    print(f"Ошибка: {data['response']['message']}")
