from collections import defaultdict
from datetime import datetime, timedelta
from src.dao.order_dao import OrderDAO
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService

class ReportService:
    def __init__(self):
        self.od = OrderDAO()
        self.ps = ProductService()
        self.cs = CustomerService()

    def _get_all_orders(self):
        # Fetch all orders
        return self.od.list_orders()

    def top_selling_products(self, top_n=5):
        totals = defaultdict(int)
        for order in self._get_all_orders():
            if order.get("status") != "COMPLETED":
                continue
            for item in self.od.get_order_items(order["order_id"]):
                totals[item["prod_id"]] += item["quantity"]

        # Map product IDs to names
        products = self.ps.list_products()
        prod_map = {p["prod_id"]: p["name"] for p in products if isinstance(p, dict)}

        sorted_totals = sorted(totals.items(), key=lambda x: x[1], reverse=True)
        return [
            {"product_id": pid, "product_name": prod_map.get(pid, "Unknown"), "total_quantity": qty}
            for pid, qty in sorted_totals[:top_n]
        ]

    def total_revenue_last_month(self):
        now = datetime.now()
        first_day_last_month = datetime(now.year, now.month, 1) - timedelta(days=1)
        start_date = datetime(first_day_last_month.year, first_day_last_month.month, 1)
        end_date = datetime(first_day_last_month.year, first_day_last_month.month,
                            first_day_last_month.day)
        revenue = 0
        for order in self._get_all_orders():
            order_date = order.get("created_at")
            if not order_date or order.get("status") != "COMPLETED":
                continue
            if start_date <= order_date <= end_date:
                revenue += order.get("total_amount", 0)
        return revenue

    def total_orders_per_customer(self):
        cust_orders = defaultdict(int)
        for order in self._get_all_orders():
            cust_orders[order["cust_id"]] += 1

        # Map customer IDs to names
        customers = self.cs.list_customers()
        cust_map = {c["cust_id"]: c["name"] for c in customers}

        return [
            {"customer_id": cid, "customer_name": cust_map.get(cid, "Unknown"), "total_orders": cnt}
            for cid, cnt in cust_orders.items()
        ]

    def frequent_customers(self, min_orders=2):
        orders_per_cust = self.total_orders_per_customer()
        return [c for c in orders_per_cust if c["total_orders"] > min_orders]
