# src/dao/order_dao.py
from typing import Optional, Dict, List
from src.config import get_supabase

class OrderDAO:
    def __init__(self):
        pass

    def _sb(self):
        return get_supabase()

    def create_order(self, cust_id: int, total_amount: float) -> Optional[Dict]:
        payload = {"cust_id": cust_id, "total_amount": total_amount, "status": "PLACED"}
        self._sb().table("orders").insert(payload).execute()
        resp = self._sb().table("orders").select("*").order("order_id", desc=True).limit(1).execute()
        return resp.data[0] if resp.data else None

    def add_order_item(self, order_id: int, prod_id: int, qty: int, price: float) -> Optional[Dict]:
        payload = {"order_id": order_id, "prod_id": prod_id, "quantity": qty, "price": price}
        self._sb().table("order_items").insert(payload).execute()
        return payload

    def get_order_by_id(self, order_id: int) -> Optional[Dict]:
        resp = self._sb().table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        resp = self._sb().table("orders").select("*").eq("cust_id", cust_id).order("order_id", desc=True).execute()
        return resp.data or []

    def update_order_status(self, order_id: int, status: str) -> Optional[Dict]:
        self._sb().table("orders").update({"status": status}).eq("order_id", order_id).execute()
        resp = self._sb().table("orders").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_order_items(self, order_id: int) -> List[Dict]:
        resp = self._sb().table("order_items").select("*").eq("order_id", order_id).execute()
        return resp.data or []
    
    def list_orders(self) -> List[Dict]:
        resp = self._sb().table("orders").select("*").order("order_id", desc=True).execute()
        return resp.data or []
