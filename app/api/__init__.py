def process_conversation_flow(sender_phone, message_text):
    """
    مدیریت جریان گفت‌وگو برای مشتریان موقت
    ورودی‌ها:
    - sender_phone: شماره مشتری
    - message_text: پیام دریافتی از مشتری

    خروجی:
    - متن پاسخ مناسب به پیام مشتری
    """

    # 1. خواندن وضعیت فعلی مکالمه یا مرحله جاری (از دیتابیس یا حافظه)
    current_step = get_temp_customer_step(sender_phone)

    # 2. بر اساس مرحله و پیام دریافتی تصمیم‌گیری و بروزرسانی مرحله
    if current_step == "waiting_for_name":
        # ذخیره نام کاربر
        save_temp_customer_name(sender_phone, message_text)
        next_step = "waiting_for_province"
        update_temp_customer_step(sender_phone, next_step)
        return "ممنون از شما! لطفا استان محل سکونت خود را وارد کنید."

    elif current_step == "waiting_for_province":
        save_temp_customer_province(sender_phone, message_text)
        next_step = "waiting_for_city"
        update_temp_customer_step(sender_phone, next_step)
        return "خوبه! حالا لطفا شهر محل سکونت خود را بنویسید."

    elif current_step == "waiting_for_city":
        save_temp_customer_city(sender_phone, message_text)
        next_step = "waiting_for_address"
        update_temp_customer_step(sender_phone, next_step)
        return "عالی! لطفا آدرس دقیق خود را وارد کنید."

    elif current_step == "waiting_for_address":
        save_temp_customer_address(sender_phone, message_text)
        next_step = "waiting_for_gender"
        update_temp_customer_step(sender_phone, next_step)
        return "ممنون! لطفا جنسیت خود را مشخص کنید (آقا / خانم)."

    elif current_step == "waiting_for_gender":
        save_temp_customer_gender(sender_phone, message_text)
        next_step = "completed"
        update_temp_customer_step(sender_phone, next_step)
        return "اطلاعات شما ثبت شد. ممنون از همکاری شما!"

    elif current_step == "completed":
        return "اگر سوالی دارید، من اینجا هستم که کمک کنم."

    else:
        # شروع یا مرحله نامشخص
        update_temp_customer_step(sender_phone, "waiting_for_name")
        return "سلام! لطفا نام خود را وارد کنید."
