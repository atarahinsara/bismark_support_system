def normalize_phone(phone: str) -> str:
    phone = phone.strip()
    if phone.startswith("+98"):
        return "0" + phone[3:]
    if phone.startswith("98"):
        return "0" + phone[2:]
    if phone.startswith("0"):
        return phone
    return phone
