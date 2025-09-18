import json
import requests
from logger import logger
import time

APP_ID = 730
ITEMS_PER_PAGE = 100
API_KEY = '59be3bc7a7ef778a565390bac7c6fac3a4b97dff71bd951392ccb048a2563377'


def fetch_bitskins_market(offset=0, limit=ITEMS_PER_PAGE, filters=None):

    url = f"https://api.bitskins.com/market/search/{APP_ID}"


    data = {
        "limit": limit,
        "offset": offset,
        "api_key": API_KEY,
        "where": filters

    }
    headers = {'Content-Type': 'application/json'}

    try:
        logger.info(f"Делаем запрос к {url} со смещением {offset}")
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()

        api_response = response.json()


        print("Полный ответ от API:")
        print(json.dumps(api_response, indent=2))


        items_in_batch = api_response.get('list')



        logger.info(f"Успешно получено данных: {len(items_in_batch)} предметов")
        return api_response

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка сети при запросе к BitSkins: {e}")
        return None
    except ValueError as e:
        logger.error(f"Ошибка парсинга JSON ответа: {e}")
        return None



def run_cs_items_collecting():
    all_items = []
    offset = 0
    total_items_to_fetch = 20
    max_price_to_fetch = 20000
    filters = {
        "price_from": 10000,
        "price_to": 15000,
        #"name": "G3SG1 | Flux (Field-Tested)"

    }

    logger.info("Начинается сбор данных с BitSkins...")

    while filters['price_from'] < max_price_to_fetch:
        data_batch = fetch_bitskins_market(offset=offset, filters=filters)
        if data_batch is None:
            logger.error("Не удалось получить данные. Прерывание.")
            break

        items_in_batch = data_batch.get('list')
        if not items_in_batch:
            logger.info("Больше нет предметов для загрузки.")
            break

        all_items.extend(items_in_batch)
        logger.info(f"Получено предметов в этом пакете: {len(items_in_batch)}. Итого: {len(all_items)}")

        #offset += len(items_in_batch)


        plus = max(1, items_in_batch[-1].get('price') - filters["price_from"])
        print(f"Прибавляем к цене {plus}")

        filters["price_from"] += plus
        filters["price_to"] += plus




        time.sleep(2)

    logger.info(f"Сбор завершен. Всего собрано {len(all_items)} предметов.")
    print(all_items[:1])
    with open('cs_items.json', 'w', encoding='utf-8') as f:
        json.dump(all_items, f, ensure_ascii=False, indent=4)


run_cs_items_collecting()


















# auth_key = API_KEY
# data = {
#   "limit": 30,
#   "offset": 0,
#   "where": {
#     "price_from": 1000,
#     "price_to": 5000,
#     "skin_name": "%glock%",
#     "tradehold_to": 5
#   }
# }
#
# headers = {'x-apikey': auth_key}
# res = requests.post('https://api.bitskins.com/market/search/730', headers=headers, json=data)
# response = json.loads(res.text)
# print(response)