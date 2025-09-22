# src/services/payment_service.py
from src.dao.payment_dao import PaymentDAO
from src.dao.order_dao import OrderDAO

pd = PaymentDAO()
od = OrderDAO()

class PaymentError(Exception):
    pass

class PaymentService:
    def __init__(self):
        pass

    def create_pending_payment(self, order_id: int, amount: float):
        return pd.create_pending_payment(order_id, amount)

    def process_payment(self, order_id: int, method: str) -> dict:
        payment = pd.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("No payment record for this order")
        if payment["status"] != "PENDING":
            raise PaymentError("Payment already processed")

        updated = pd.update_payment(payment["payment_id"], {
            "status": "PAID",
            "method": method
        })
        od.update_order_status(order_id, "COMPLETED")
        return updated

    def refund_payment(self, order_id: int) -> dict:
        payment = pd.get_payment_by_order(order_id)
        if not payment:
            raise PaymentError("No payment record for this order")
        if payment["status"] != "PAID":
            raise PaymentError("Only PAID payments can be refunded")

        updated = pd.update_payment(payment["payment_id"], {"status": "REFUNDED"})
        return updated
