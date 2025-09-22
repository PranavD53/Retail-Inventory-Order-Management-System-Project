# src/services/customer_service.py
from typing import Dict, List
from src.dao.customer_dao import CustomerDAO
from src.dao.order_dao import OrderDAO

cd = CustomerDAO()
od = OrderDAO()

class CustomerError(Exception):
    pass

class CustomerService:
    def __init__(self):
        pass

    def add_customer(self,name: str, email: str, phone: str, city: str | None = None) -> Dict:
        existing = cd.get_customer_by_email(email)
        if existing:
            raise CustomerError(f"Email already exists: {email}")
        return cd.create_customer(name, email, phone, city)

    def update_customer(self,cust_id: int, phone: str | None = None, city: str | None = None) -> Dict:
        updates = {}
        if phone:
            updates["phone"] = phone
        if city:
            updates["city"] = city
        if not updates:
            raise CustomerError("No fields to update")
        return cd.update_customer(cust_id, updates)

    def delete_customer(self,cust_id: int) -> Dict:
        orders = od.list_orders_by_customer(cust_id)
        if orders:
            raise CustomerError("Customer has existing orders, cannot delete.")
        return cd.delete_customer(cust_id)

    def list_customers(self,limit: int = 100) -> List[Dict]:
        return cd.list_customers(limit)

    def search_customers(self,email: str | None = None, city: str | None = None) -> List[Dict]:
        return cd.search_customers(email, city)
