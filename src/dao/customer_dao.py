# src/dao/customer_dao.py
from typing import Optional, List, Dict
from src.config import get_supabase

class CustomerDAO:
    def __init__(self):
        pass

    def _sb(self):
        return get_supabase()

    def create_customer(self, name: str, email: str, phone: str, city: str | None = None) -> Optional[Dict]:
        payload = {"name": name, "email": email, "phone": phone}
        if city:
            payload["city"] = city

        # Insert
        self._sb().table("customers").insert(payload).execute()

        # Fetch inserted by unique email
        resp = self._sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_id(self, cust_id: int) -> Optional[Dict]:
        resp = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_customer_by_email(self, email: str) -> Optional[Dict]:
        resp = self._sb().table("customers").select("*").eq("email", email).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_customer(self, cust_id: int, fields: Dict) -> Optional[Dict]:
        self._sb().table("customers").update(fields).eq("cust_id", cust_id).execute()
        resp = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def delete_customer(self, cust_id: int) -> Optional[Dict]:
        resp_before = self._sb().table("customers").select("*").eq("cust_id", cust_id).limit(1).execute()
        row = resp_before.data[0] if resp_before.data else None
        self._sb().table("customers").delete().eq("cust_id", cust_id).execute()
        return row

    def list_customers(self, limit: int = 100) -> List[Dict]:
        resp = self._sb().table("customers").select("*").order("cust_id", desc=False).limit(limit).execute()
        return resp.data or []

    def search_customers(self, email: str | None = None, city: str | None = None) -> List[Dict]:
        q = self._sb().table("customers").select("*")
        if email:
            q = q.eq("email", email)
        if city:
            q = q.eq("city", city)
        resp = q.execute()
        return resp.data or []
