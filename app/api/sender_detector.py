from app.models import Customer, CustomerPhone, SalesRepresentativePhone, TechnicianPhone, CustomerTemp
from sqlalchemy.orm import joinedload

def detect_sender(phone):
    # جستجو در مشتری‌ها
    customer = Customer.query \
        .join(CustomerPhone, Customer.CustomerID == CustomerPhone.CustomerID) \
        .options(joinedload(Customer.Phones)) \
        .filter(CustomerPhone.PhoneNumber == phone) \
        .first()
    if customer:
        return "Customer", customer.CustomerID, customer

    # جستجو در نماینده‌های فروش
    sales_rep_phone = SalesRepresentativePhone.query \
        .options(joinedload(SalesRepresentativePhone.SalesRepresentative)) \
        .filter(SalesRepresentativePhone.PhoneNumber == phone) \
        .first()
    if sales_rep_phone:
        return "SalesRepresentative", sales_rep_phone.SalesRepID, sales_rep_phone.SalesRepresentative

    # جستجو در تکنسین‌ها
    technician_phone = TechnicianPhone.query \
        .options(joinedload(TechnicianPhone.Technician)) \
        .filter(TechnicianPhone.PhoneNumber == phone) \
        .first()
    if technician_phone:
        return "ServiceTechnician", technician_phone.TechnicianID, technician_phone.Technician

    # بررسی مشتری موقت
    temp_customer = CustomerTemp.query.filter_by(UserNumber=phone).first()
    if temp_customer:
        return "TempCustomer", temp_customer.TempID, temp_customer

    # در صورتی که یافت نشد
    return "Unknown", None, None
