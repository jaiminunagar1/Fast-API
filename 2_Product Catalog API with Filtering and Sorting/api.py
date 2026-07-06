from http.client import HTTPException

from fastapi import FastAPI , Query
from typing import Literal, Optional

products_catalog = [
  {
    "id": 1,
    "name": "Laptop",
    "category": "Electronics",
    "price": 65000,
    "in_stock": True
  },
  {
    "id": 2,
    "name": "Smartphone",
    "category": "Electronics",
    "price": 30000,
    "in_stock": True
  },
  {
    "id": 3,
    "name": "Wireless Mouse",
    "category": "Accessories",
    "price": 1200,
    "in_stock": True
  },
  {
    "id": 4,
    "name": "Mechanical Keyboard",
    "category": "Accessories",
    "price": 4500,
    "in_stock": False
  },
  {
    "id": 5,
    "name": "Gaming Monitor",
    "category": "Electronics",
    "price": 18000,
    "in_stock": True
  },
  {
    "id": 6,
    "name": "Bluetooth Speaker",
    "category": "Audio",
    "price": 3500,
    "in_stock": True
  },
  {
    "id": 7,
    "name": "Office Chair",
    "category": "Furniture",
    "price": 8500,
    "in_stock": False
  },
  {
    "id": 8,
    "name": "Study Table",
    "category": "Furniture",
    "price": 7000,
    "in_stock": True
  },
  {
    "id": 9,
    "name": "USB-C Charger",
    "category": "Accessories",
    "price": 1500,
    "in_stock": True
  },
  {
    "id": 10,
    "name": "Noise Cancelling Headphones",
    "category": "Audio",
    "price": 12000,
    "in_stock": False
  }
]

app = FastAPI()


# @app.get("/products")
# def get_products(category: Optional[str] = None,min_price: Optional[float]= Query(None, gt = 0),max_price: Optional[float] = Query(None, gt = 0),sort: Optional[Literal['asc', 'desc']] = Query(None),limit: Optional[int] = Query(None,gt = 0,le = 51 )):

#     if min_price is not None and max_price is not None:
#         filtered_products = [product for product in products_catalog if min_price <= product['price'] <= max_price]
#         return filtered_products
    
#     if min_price is not None:
#         minprice_products = [product for product in products_catalog if product['price'] >= min_price]
#         return minprice_products
#     if max_price is not None:
#         maxprice_products = [product for product in products_catalog if product['price'] <= max_price]
#         return maxprice_products
    
#     if limit and not category and not sort:
#         limited_products = products_catalog[:limit]
#         return limited_products

#     if category and not sort and not limit:
#         Filtered_products = [product for product in products_catalog if product['category'].lower() == category.lower()]
#         return Filtered_products
#     if category and sort and limit:
#         filtered_products = [product for product in products_catalog if product['category'].lower() == category.lower()]
#         if sort == 'asc':
#             sorted_products = sorted(filtered_products, key=lambda x: x['price'])
#             limited_sorted_products = sorted_products[:limit]
#             return limited_sorted_products
#         if sort == 'desc':
#             sorted_products = sorted(filtered_products, key=lambda x: x['price'], reverse=True)
#             limited_sorted_products = sorted_products[:limit]
#             return limited_sorted_products
    
#     if sort == 'asc' and limit is not None:
#         sorted_products = sorted(products_catalog, key=lambda x: x['price'])
#         limited_sorted_products = sorted_products[:limit]
#         return limited_sorted_products
#     if sort == 'desc' and limit is not None:
#         sorted_products = sorted(products_catalog, key=lambda x: x['price'], reverse=True)
#         limited_sorted_products = sorted_products[:limit]
#         return limited_sorted_products

#     return products_catalog


@app.get("/products")
def get_products(category: Optional[str] = None, 
                 min_price: Optional[float] = Query(None, gt=0), 
                 max_price: Optional[float] = Query(None, gt=0), 
                 sort: Optional[Literal['asc', 'desc']] = Query(None), 
                 limit: Optional[int] = Query(None, gt=0, le=51),
                 in_stock: Optional[bool] = None):
    
    filtered_products = products_catalog

    if ( min_price is not None and max_price is not None and min_price > max_price):
        raise HTTPException(status_code=400, detail={"error": "min_price cannot be greater than max_price"})
    
    # Filter by category
    if category:
        filtered_products = [
            product
            for product in filtered_products
            if product["category"].lower() == category.lower()
        ]

     # Filter by minimum price
    if min_price is not None:
        filtered_products = [
            product
            for product in filtered_products
            if product["price"] >= min_price
        ]

     # Filter by maximum price
    if max_price is not None:
        filtered_products = [
            product
            for product in filtered_products
            if product["price"] <= max_price
        ]

    # Filter by stock
    if in_stock is not None:
        filtered_products = [
            product
            for product in filtered_products
            if product["in_stock"] == in_stock
        ]

    # Sort
    if sort == "asc":
        filtered_products = sorted(
            filtered_products,
            key=lambda product: product["price"]
        )

    elif sort == "desc":
        filtered_products = sorted(
            filtered_products,
            key=lambda product: product["price"],
            reverse=True,
        )

    # Limit
    if limit is not None:
        filtered_products = filtered_products[:limit]

    return {
          "total_products": len(products_catalog),
          "filtered_products": len(filtered_products),
          "products": filtered_products,
      }
        

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('api:app', host='127.0.0.1', port=8000,reload=True)