# src/services/product_service.py
from typing import List, Dict
from src.dao.product_dao import ProductDAO

pd=ProductDAO()
 
class ProductError(Exception):
    pass

class ProductService: 
    def __init__(self):
        pass
    
    def add_product(self,name: str, sku: str, price: float, stock: int = 0, category: str | None = None) -> Dict:
        """
        Validate and insert a new product.
        Raises ProductError on validation failure.
        """
        if price <= 0:
            raise ProductError("Price must be greater than 0")
        existing = pd.get_product_by_sku(sku)
        if existing:
            raise ProductError(f"SKU already exists: {sku}")
        return pd.create_product(name, sku, price, stock, category)
    
    def restock_product(self,prod_id: int, delta: int) -> Dict:
        if delta <= 0:
            raise ProductError("Delta must be positive")
        p = pd.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        new_stock = (p.get("stock") or 0) + delta
        return pd.update_product(prod_id, {"stock": new_stock})
    
    def get_low_stock(self,threshold: int = 5) -> List[Dict]:
        allp = pd.list_products(limit=1000)
        return [p for p in allp if (p.get("stock") or 0) <= threshold]

    def update_product(self,prod_id: int, name: str | None = None, price: float | None = None, stock: int | None = None, category: str | None = None) -> Dict:
        updates = {}
        if name:
            updates["name"] = name
        if price is not None:
            if price <= 0:
                raise ProductError("Price must be greater than 0")
            updates["price"] = price
        if stock is not None:
            if stock < 0:
                raise ProductError("Stock cannot be negative")
            updates["stock"] = stock
        if category is not None:
            updates["category"] = category

        if not updates:
            raise ProductError("No fields to update")

        return pd.update_product(prod_id, updates)

    def delete_product(self,prod_id: int) -> Dict:
        p = pd.get_product_by_id(prod_id)
        if not p:
            raise ProductError("Product not found")
        return pd.delete_product(prod_id)

    def search_products(self, sku: str | None = None, category: str | None = None):
        if sku:
            p = pd.get_product_by_sku(sku)
            return [p] if p else []
        if category:
            return pd.list_products(limit=100, category=category)
        return pd.list_products(limit=100)
    
    def list_products(self):
        p=pd.list_products()
        if(p==[]):
            return "Cartel is empty"
        else:
            return pd.list_products()