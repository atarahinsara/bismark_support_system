#from app.models import MessageTemplate

#def build_response(sender_type, person, is_welcome=False):
    # اگر پیام خوش‌آمد باید داده شود، قالب مربوط را بگیر
    if is_welcome:
        # مثلا قالبی با sender_type ترکیبی مثل 'customer_Welcome'
        welcome_type = f"{sender_type}_Welcome"
        template_obj = MessageTemplate.query.filter_by(sender_type=welcome_type).first()
        if not template_obj:
            # اگر قالب خوش‌آمد موجود نبود، از قالب پیش‌فرض استفاده کن
            template_obj = MessageTemplate.query.filter_by(sender_type="Welcome_Default").first()
    else:
        template_obj = MessageTemplate.query.filter_by(sender_type=sender_type).first()

    if not template_obj:
        template_obj = MessageTemplate.query.filter_by(sender_type="Unknown").first()
        if not template_obj:
            return (
                "سلام 🙏 خوش آمدید به پشتیبانی واتساپ شرکت بیسمارک.\n"
                "شما در حال حاضر در سیستم ثبت نشده‌اید.\n"
                "لطفاً برای شروع، نام و نام خانوادگی خود را وارد نمایید."
            )

    name = f"{person.FirstName or ''} {person.LastName or ''}".strip() if person else ""
    city_info = getattr(person, "City", "") if person else ""
    gender_name = ""
    if person and getattr(person, "Gender", None):
        gender_name = getattr(person.Gender, "GenderName", "")

    gender_prefix = gender_name if sender_type in ["SalesRep", "Technician"] else ""

    response_text = template_obj.message_template.format(
        name=name,
        city_info=city_info,
        gender_prefix=gender_prefix
    )

    return response_text.strip()
