import re

def extract_entities_from_text(text):
    # نمونه اولیه برای استخراج نام و نام‌خانوادگی ساده
    entities = []

    name_match = re.search(r"(?:من)?\s*(\w+)\s+(\w+)\s*هستم", text)
    if name_match:
        entities.append({"entity": "first_name", "value": name_match.group(1)})
        entities.append({"entity": "last_name", "value": name_match.group(2)})

    return entities
