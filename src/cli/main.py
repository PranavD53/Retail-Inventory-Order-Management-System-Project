# src/cli/main.py
import argparse
import json
from src.services.order_service import OrderService
from src.services.product_service import ProductService
from src.services.customer_service import CustomerService
from src.services.payment_service import PaymentService
from src.services.report_service import ReportService


customer_service = CustomerService()

product_service=ProductService()

order_service=OrderService()

payment_service=PaymentService()

report_service = ReportService()
#Product

def cmd_product_add(args):
    try:
        p = product_service.add_product(args.name, args.sku, args.price, args.stock, args.category)
        print("Created product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_product_list(args):
    ps = product_service.list_products()
    print(json.dumps(ps, indent=2, default=str))

def cmd_product_update(args):
    try:
        p = product_service.update_product(
            args.id,
            args.name,
            args.price,
            args.stock,
            args.category,
        )
        print("Updated product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_delete(args):
    try:
        p = product_service.delete_product(args.id)
        print("Deleted product:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_product_search(args):
    try:
        ps = product_service.search_products(args.sku, args.category)
        print(json.dumps(ps, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


# Customer

def cmd_customer_add(args):
    try:
        c = customer_service.add_customer(args.name, args.email, args.phone, args.city)
        print("Created customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_update(args):
    try:
        c = customer_service.update_customer(args.id, args.phone, args.city)
        print("Updated customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_delete(args):
    try:
        c = customer_service.delete_customer(args.id)
        print("Deleted customer:")
        print(json.dumps(c, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_customer_list(args):
    cs = customer_service.list_customers(limit=100)
    print(json.dumps(cs, indent=2, default=str))

def cmd_customer_search(args):
    cs = customer_service.search_customers(args.email, args.city)
    print(json.dumps(cs, indent=2, default=str))

# Orders

def cmd_order_create(args):
    # items provided as prod_id:qty strings
    items = []
    for item in args.item:
        try:
            pid, qty = item.split(":")
            items.append({"prod_id": int(pid), "quantity": int(qty)})
        except Exception:
            print("Invalid item format:", item)
            return
    try:
        ord = order_service.create_order(args.customer, items)
        print("Order created:")
        print(json.dumps(ord, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_show(args):
    try:
        o = order_service.get_order_details(args.order)
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)
 
def cmd_order_cancel(args):
    try:
        o = order_service.cancel_order(args.order)
        print("Order cancelled (updated):")
        print(json.dumps(o, indent=2, default=str))
    except Exception as e:
        print("Error:", e)


# Payments
def cmd_payment_process(args):
    try:
        p = payment_service.process_payment(args.order, args.method)
        print("Payment processed:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

def cmd_payment_refund(args):
    try:
        p = payment_service.refund_payment(args.order)
        print("Payment refunded:")
        print(json.dumps(p, indent=2, default=str))
    except Exception as e:
        print("Error:", e)

# Report
def cmd_report_top_products(args):
    res = report_service.top_selling_products(args.top)
    print(json.dumps(res, indent=2, default=str))

def cmd_report_total_revenue(args):
    res = report_service.total_revenue_last_month()
    print(f"Total revenue last month: {res}")

def cmd_report_orders_per_customer(args):
    res = report_service.total_orders_per_customer()
    print(json.dumps(res, indent=2, default=str))

def cmd_report_frequent_customers(args):
    res = report_service.frequent_customers(args.min_orders)
    print(json.dumps(res, indent=2, default=str))




def build_parser():
    parser = argparse.ArgumentParser(prog="retail-cli")
    sub = parser.add_subparsers(dest="cmd")
 
    # product add
    p_prod = sub.add_parser("product", help="product commands")
    pprod_sub = p_prod.add_subparsers(dest="action")
    addp = pprod_sub.add_parser("add")
    addp.add_argument("--name", required=True)
    addp.add_argument("--sku", required=True)
    addp.add_argument("--price", type=float, required=True)
    addp.add_argument("--stock", type=int, default=0)
    addp.add_argument("--category", default=None)
    addp.set_defaults(func=cmd_product_add)

    # product list

    listp = pprod_sub.add_parser("list")
    listp.set_defaults(func=cmd_product_list)

    # product update
    updatep = pprod_sub.add_parser("update")
    updatep.add_argument("--id", type=int, required=True)
    updatep.add_argument("--name", default=None)
    updatep.add_argument("--price", type=float, default=None)
    updatep.add_argument("--stock", type=int, default=None)
    updatep.add_argument("--category", default=None)
    updatep.set_defaults(func=cmd_product_update)

    # product delete

    deletep = pprod_sub.add_parser("delete")
    deletep.add_argument("--id", type=int, required=True)
    deletep.set_defaults(func=cmd_product_delete)

    # product search
    searchp = pprod_sub.add_parser("search")
    searchp.add_argument("--sku", default=None)
    searchp.add_argument("--category", default=None)
    searchp.set_defaults(func=cmd_product_search)


    # customer add
    pcust = sub.add_parser("customer")
    pcust_sub = pcust.add_subparsers(dest="action")
    addc = pcust_sub.add_parser("add")
    addc.add_argument("--name", required=True)
    addc.add_argument("--email", required=True)
    addc.add_argument("--phone", required=True)
    addc.add_argument("--city", default=None)
    addc.set_defaults(func=cmd_customer_add)

    # customer list

    listc = pcust_sub.add_parser("list")
    listc.set_defaults(func=cmd_customer_list)

    # customer search
    searchc = pcust_sub.add_parser("search")
    searchc.add_argument("--email", default=None)
    searchc.add_argument("--city", default=None)
    searchc.set_defaults(func=cmd_customer_search)

    # customer update

    updc = pcust_sub.add_parser("update")
    updc.add_argument("--id", type=int, required=True)
    updc.add_argument("--phone", default=None)
    updc.add_argument("--city", default=None)
    updc.set_defaults(func=cmd_customer_update)

    # customer delete

    delc = pcust_sub.add_parser("delete")
    delc.add_argument("--id", type=int, required=True)
    delc.set_defaults(func=cmd_customer_delete)
 
    # order create
    porder = sub.add_parser("order")
    porder_sub = porder.add_subparsers(dest="action")

    createo = porder_sub.add_parser("create")
    createo.add_argument("--customer", type=int, required=True)
    createo.add_argument("--item", required=True, nargs="+", help="prod_id:qty (repeatable)")
    createo.set_defaults(func=cmd_order_create)

    # order show

    showo = porder_sub.add_parser("show")
    showo.add_argument("--order", type=int, required=True)
    showo.set_defaults(func=cmd_order_show)

    # order cancel

    cano = porder_sub.add_parser("cancel")
    cano.add_argument("--order", type=int, required=True)
    cano.set_defaults(func=cmd_order_cancel)

    # payments
    ppay = sub.add_parser("payment")
    ppay_sub = ppay.add_subparsers(dest="action")

    proc = ppay_sub.add_parser("process")
    proc.add_argument("--order", type=int, required=True)
    proc.add_argument("--method", required=True, choices=["Cash", "Card", "UPI"])
    proc.set_defaults(func=cmd_payment_process)

    ref = ppay_sub.add_parser("refund")
    ref.add_argument("--order", type=int, required=True)
    ref.set_defaults(func=cmd_payment_refund)

     # Reports
    preport = sub.add_parser("report", help="reporting commands")
    preport_sub = preport.add_subparsers(dest="action")

    top_prod = preport_sub.add_parser("top-products")
    top_prod.add_argument("--top", type=int, default=5)
    top_prod.set_defaults(func=cmd_report_top_products)

    revenue = preport_sub.add_parser("revenue")
    revenue.set_defaults(func=cmd_report_total_revenue)

    orders_per_cust = preport_sub.add_parser("orders-per-customer")
    orders_per_cust.set_defaults(func=cmd_report_orders_per_customer)

    freq_cust = preport_sub.add_parser("frequent-customers")
    freq_cust.add_argument("--min-orders", type=int, default=2)
    freq_cust.set_defaults(func=cmd_report_frequent_customers)


    return parser
 
def main():
    parser = build_parser()
    args = parser.parse_args()
    if not hasattr(args, "func"):
        parser.print_help()
        return
    args.func(args)
 
if __name__ == "__main__":
    main()