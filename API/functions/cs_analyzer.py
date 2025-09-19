from logger import logger


def analyze_skins(items):
    """
    Анализирует список предметов из API Bitskins и возвращает лучшие предложения
    по различным категориям, учитывая float, цену, наклейки и сбалансированность параметров.
    """

    # Фильтруем предметы, которые доступны для покупки (tradehold != 0)
    available_items = [item for item in items if item.get('status', 0) != 0]

    if not available_items:
        return {"error": "No available items with status != 0"}

    # Инициализируем переменные для хранения лучших предметов по разным категориям
    best_items = {
        "lowest_price": None,
        "lowest_float": None,
        "best_stickers": None,
        "best_balanced": None
    }

    # Вспомогательные переменные для сравнения
    min_price = float('inf')
    min_float = float('inf')
    max_sticker_score = -1
    max_balanced_score = -1

    # Сначала соберем данные для нормализации параметров
    prices = []
    floats = []
    sticker_scores = []

    for item in available_items:
        prices.append(item.get('price', float('inf')))
        if 'float_value' in item:
            floats.append(item['float_value'])
        sticker_scores.append(calculate_sticker_score(item))

    # Находим мин/макс значения для нормализации
    min_price_norm = min(prices) if prices else 0
    max_price_norm = max(prices) if prices else 1
    min_float_norm = min(floats) if floats else 0
    max_float_norm = max(floats) if floats else 1
    max_sticker_norm = max(sticker_scores) if sticker_scores else 1

    # Анализируем каждый предмет
    for item in available_items:
        price = item.get('price', float('inf'))
        float_value = item.get('float_value', float('inf'))
        sticker_score = calculate_sticker_score(item)

        # 1. Предмет с самой низкой ценой
        if price < min_price:
            min_price = price
            best_items["lowest_price"] = item

        # 2. Предмет с самым низким float
        if float_value < min_float:
            min_float = float_value
            best_items["lowest_float"] = item

        # 3. Предмет с лучшими наклейками
        if sticker_score > max_sticker_score:
            max_sticker_score = sticker_score
            best_items["best_stickers"] = item

        # 4. Сбалансированная оценка по всем параметрам
        balanced_score = calculate_balanced_score(
            item,
            min_price_norm, max_price_norm,
            min_float_norm, max_float_norm,
            max_sticker_norm
        )

        if balanced_score > max_balanced_score:
            max_balanced_score = balanced_score
            best_items["best_balanced"] = item

    return best_items


def calculate_sticker_score(item):
    """Вычисляет оценку наклеек на предмете"""
    if 'stickers' not in item or not item['stickers']:
        return 0

    score = 0
    for sticker in item['stickers']:
        # Базовая ценность наклейки
        sticker_value = 1

        # Учитываем износ наклейки (чем меньше, тем лучше)
        wear = sticker.get('wear', 1)
        wear_multiplier = 1 - wear  # 0-1, где 1 - идеальное состояние

        # Учитываем редкость наклейки (можно добавить дополнительную логику)
        # Здесь просто увеличиваем ценность для холографических и т.д.
        name = sticker.get('name', '').lower()
        if 'holo' in name:
            sticker_value *= 1.5
        if 'foil' in name:
            sticker_value *= 1.3
        if 'katowice' in name:
            sticker_value *= 2.0  # Наклейки Katowice обычно более ценные

        score += sticker_value * wear_multiplier

    return score


def calculate_balanced_score(item, min_p, max_p, min_f, max_f, max_s):
    """
    Вычисляет сбалансированную оценку предмета на основе:
    - Цены (чем дешевле, тем лучше)
    - Float (чем меньше, тем лучше)
    - Наклеек (чем больше и качественнее, тем лучше)
    """
    # Нормализуем параметры от 0 до 1
    price = item.get('price', max_p)
    price_norm = 1 - (price - min_p) / (max_p - min_p) if max_p != min_p else 0.5

    float_val = item.get('float_value', max_f)
    float_norm = 1 - (float_val - min_f) / (max_f - min_f) if max_f != min_f else 0.5

    sticker_score = calculate_sticker_score(item)
    sticker_norm = sticker_score / max_s if max_s > 0 else 0

    # Весовые коэффициенты (можно настроить)
    weight_price = 0.5
    weight_float = 0.3
    weight_stickers = 0.3

    # Итоговая оценка
    balanced_score = (
            weight_price * price_norm +
            weight_float * float_norm +
            weight_stickers * sticker_norm
    )

    return balanced_score