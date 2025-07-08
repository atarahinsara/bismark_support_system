import re

provinces = [
    "آذربایجان شرقی", "آذربایجان غربی", "اردبیل", "اصفهان", "البرز",
    "ایلام", "بوشهر", "تهران", "چهارمحال و بختیاری", "خراسان جنوبی",
    "خراسان رضوی", "خراسان شمالی", "خوزستان", "زنجان", "سمنان",
    "سیستان و بلوچستان", "فارس", "قزوین", "قم", "کردستان",
    "کرمان", "کرمانشاه", "کهگیلویه و بویراحمد", "گلستان", "گیلان",
    "لرستان", "مازندران", "مرکزی", "هرمزگان", "همدان",
    "یزد"
]

cities = [
    "سقز", "تهران", "مشهد", "اصفهان", "تبریز", "کرج", "شیراز",
    "قم", "کرمانشاه", "رشت", "ارومیه", "کرمان", "اهواز", "زاهدان",
    "یزد", "قزوین"
]

genders = {
    "مرد": ["آقا", "مرد", "آقای", "جناب آقا", "جناب"],
    "زن": ["خانم", "زن", "خانوم", "سرکار خانم", "سرکار"]
}

city_to_province_map = {
    "تهران": "تهران",
    "تبریز": "آذربایجان شرقی",
    "کرج": "البرز",
    "مشهد": "خراسان رضوی",
    "اصفهان": "اصفهان",
    "شیراز": "فارس",
    "قم": "قم",
    "کرمانشاه": "کرمانشاه",
    "رشت": "گیلان",
    "ارومیه": "آذربایجان غربی",
    "اهواز": "خوزستان",
    "زاهدان": "سیستان و بلوچستان",
    "یزد": "یزد",
    "قزوین": "قزوین",
    # می‌توان بقیه شهرها را اضافه کرد
}

def extract_entities_from_text(text):
    entities = []
    text = text.strip().replace("  ", " ")

    # --- استخراج نام و نام خانوادگی ---
    name_match = re.search(r"(?:من\s+)?(.+?)\s+هستم", text)
    if name_match:
        full_name = name_match.group(1).strip()
        name_parts = full_name.split()
        if len(name_parts) == 2:
            first_name, last_name = name_parts
        elif len(name_parts) == 3:
            first_name = " ".join(name_parts[:2])
            last_name = name_parts[2]
        elif len(name_parts) > 3:
            first_name = " ".join(name_parts[:-1])
            last_name = name_parts[-1]
        else:
            first_name = name_parts[0]
            last_name = ""
        entities.append({"entity": "first_name", "value": first_name})
        entities.append({"entity": "last_name", "value": last_name})

    # --- استخراج جنسیت ---
    gender_found = False
    for gender_key, keywords in genders.items():
        for keyword in keywords:
            pattern = rf"\b{re.escape(keyword)}\b"
            if re.search(pattern, text):
                entities.append({"entity": "gender", "value": gender_key})
                gender_found = True
                break
        if gender_found:
            break

    # --- استخراج شهر (اولویت بالاتر) ---
    city_found = False
    for city in cities:
        # الگوهای متداول برای شهر
        patterns = [
            rf"(?:من\s+)?(?:در|از|اهل|ساکن)?\s*{re.escape(city)}(?:م| هستم|ام)?",
            rf"{re.escape(city)}$",
            rf"^{re.escape(city)}$",
        ]
        for pattern in patterns:
            if re.search(pattern, text):
                entities.append({"entity": "city", "value": city})
                city_found = True
                # اضافه کردن استان مرتبط با شهر
                province = city_to_province_map.get(city)
                if province:
                    entities.append({"entity": "province", "value": province})
                break
        if city_found:
            break

    # --- اگر شهر نبود، استان را استخراج کن ---
    if not city_found:
        for province in provinces:
            patterns = [
                rf"اهل\s+{re.escape(province)}(?:م| هستم|ام)?",
                rf"(?:من\s+)?اهل\s+{re.escape(province)}(?:م| هستم|ام)?",
                rf"(?:من\s+)?{re.escape(province)}\s+هستم",
                rf"ساکن\s+{re.escape(province)}(?:م| هستم|ام)?",
            ]
            for pattern in patterns:
                if re.search(pattern, text):
                    entities.append({"entity": "province", "value": province})
                    break
            else:
                continue
            break

    # --- استخراج شماره تلفن (ایران) ---
    phone_match = re.search(r"(\+98|0)?9\d{9}", text)
    if phone_match:
        phone = phone_match.group()
        entities.append({"entity": "phone_number", "value": phone})

    # --- استخراج آدرس ---
    address_match = re.search(r"(?:آدرس|نشانی|محل سکونت)[:\s]*(.+)", text)
    if address_match:
        address = address_match.group(1).strip()
        entities.append({"entity": "address", "value": address})

    return entities
