from logger import logger

def find_best_item(list):
    logger.info(f"Начинается поиск лучшего предмета из списка")
    for item in list:

        for best_float in item:
            found_float = item["float_value"]
            if found_float > best_float:
                best_float = found_float

        for best_price in item:
            found_price = item["price"]
            if found_price > best_price:
                best_price = found_price



