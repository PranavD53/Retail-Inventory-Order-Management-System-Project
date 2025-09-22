# src/services/order_service.py
from typing import List, Dict
from src.dao.order_dao import OrderDAO
from src.dao.customer_dao import CustomerDAO
from src.dao.product_dao import ProductDAO
from src.services.payment_service import PaymentService

ps = PaymentService()

od = OrderDAO()
cd = CustomerDAO()
pd = ProductDAO()

class OrderError(Exception):
    pass

class OrderService:
    def __init__(self):
        pass

    def create_order(self, cust_id: int, items: List[Dict]) -> Dict:
        # check customer exists
        customer = cd.get_customer_by_id(cust_id)
        if not customer:
            raise OrderError("Customer not found")

        total = 0
        updates = []  # track stock updates
        for item in items:
            prod = pd.get_product_by_id(item["prod_id"])
            if not prod:
                raise OrderError(f"Product {item['prod_id']} not found")
            if prod["stock"] < item["quantity"]:
                raise OrderError(f"Not enough stock for product {prod['name']}")

            line_total = float(prod["price"]) * item["quantity"]
            total += line_total
            new_stock = prod["stock"] - item["quantity"]
            updates.append((prod["prod_id"], new_stock, prod["price"], item["quantity"]))

        # create order
        order = od.create_order(cust_id, total)

        # insert order items & update stock
        for prod_id, new_stock, price, qty in updates:
            od.add_order_item(order["order_id"], prod_id, qty, price)
            pd.update_product(prod_id, {"stock": new_stock})

        # create pending payment
        ps.create_pending_payment(order["order_id"], total)

        return self.get_order_details(order["order_id"])

    def get_order_details(self, order_id: int) -> Dict:
        order = od.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        customer = cd.get_customer_by_id(order["cust_id"])
        items = od.get_order_items(order_id)
        return {
            "order": order,
            "customer": customer,
            "items": items
        }

    def list_orders_by_customer(self, cust_id: int) -> List[Dict]:
        return od.list_orders_by_customer(cust_id)
    
    def list_orders(self) -> List[Dict]:
        return od.list_orders()

    def cancel_order(self, order_id: int) -> Dict:
        order = od.get_order_by_id(order_id)
        if not order:
            raise OrderError("Order not found")
        if order["status"] != "PLACED":
            raise OrderError("Only PLACED orders can be cancelled")

        # restore stock
        items = od.get_order_items(order_id)
        for item in items:
            prod = pd.get_product_by_id(item["prod_id"])
            if prod:
                restored_stock = prod["stock"] + item["quantity"]
                pd.update_product(prod["prod_id"], {"stock": restored_stock})
        
        ps.refund_payment(order_id)

        return od.update_order_status(order_id, "CANCELLED")

