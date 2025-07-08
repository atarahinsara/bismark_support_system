from rapidfuzz import fuzz

intent_samples = {
    "معرفی شخص": [
        "من عطا احمدی هستم",
        "اسم من عطا است",
        "من خودم را معرفی می‌کنم",
    ],
    "پرسش وضعیت سفارش": [
        "سفارش من کجاست؟",
        "وضعیت سفارش چطوره؟",
        "پیگیری سفارش",
    ],
    "درخواست پشتیبانی": [
        "کمک می‌خوام",
        "مشکل دارم",
        "پشتیبانی لطفاً",
    ],
    "خداحافظی": [
        "خداحافظ",
        "خداحافظی می‌کنم",
        "تمام شد",
    ],
}

def detect_intent(user_message):
    best_intent = None
    best_score = 0
    for intent, samples in intent_samples.items():
        for sample in samples:
            score = fuzz.ratio(user_message, sample)
            if score > best_score:
                best_score = score
                best_intent = intent
    if best_score >= 60:
        return best_intent, best_score
    return None, 0
