# src/dao/payment_dao.py
from typing import Optional, Dict, List
from src.config import get_supabase

class PaymentDAO:
    def __init__(self):
        pass

    def _sb(self):
        return get_supabase()

    def create_pending_payment(self, order_id: int, amount: float) -> Optional[Dict]:
        payload = {"order_id": order_id, "amount": amount, "status": "PENDING"}
        self._sb().table("payments").insert(payload).execute()
        resp = self._sb().table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def update_payment(self, payment_id: int, fields: Dict) -> Optional[Dict]:
        self._sb().table("payments").update(fields).eq("payment_id", payment_id).execute()
        resp = self._sb().table("payments").select("*").eq("payment_id", payment_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def get_payment_by_order(self, order_id: int) -> Optional[Dict]:
        resp = self._sb().table("payments").select("*").eq("order_id", order_id).limit(1).execute()
        return resp.data[0] if resp.data else None

    def list_payments(self, order_id: int) -> List[Dict]:
        resp = self._sb().table("payments").select("*").eq("order_id", order_id).execute()
        return resp.data or []
