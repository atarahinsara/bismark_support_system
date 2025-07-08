from app.models.Customer_Phone import CustomerPhone
from app.models.Sales_Representative_Phone import SalesRepresentativePhone
from app.models.Technician_Phone import TechnicianPhone

def identify_user_type(phone):
    # جستجو در جدول شماره‌های مشتری‌ها
    customer_phone = CustomerPhone.query.filter_by(PhoneNumber=phone).first()
    if customer_phone:
        return "customer", customer_phone.Customer

    # جستجو در جدول شماره‌های نمایندگان فروش
    sales_rep_phone = SalesRepresentativePhone.query.filter_by(PhoneNumber=phone).first()
    if sales_rep_phone:
        return "sales_representative", sales_rep_phone.SalesRepresentative

    # جستجو در جدول شماره‌های تکنسین‌ها
    technician_phone = TechnicianPhone.query.filter_by(PhoneNumber=phone).first()
    if technician_phone:
        return "service_technician", technician_phone.Technician

    # اگر هیچکدام نبود
    return None, None
