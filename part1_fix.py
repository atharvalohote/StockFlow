from flask import request
from models import Product, Inventory, db

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.json
    
    # 1. Validation
    required_fields = ['name', 'sku', 'price', 'warehouse_id', 'initial_quantity']
    if not all(field in data for field in required_fields):
        return {"error": "Missing required fields"}, 400

    try:
        # 2. Fix: Remove warehouse_id from Product (it belongs in Inventory)
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=data['price']
        )
        
        db.session.add(product)
        # Flush gets us the ID without committing the transcation yet
        db.session.flush() 
        
        # 3. Create Inventory Record
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )
        
        db.session.add(inventory)
        
        # 4. Atomic Commit: Both succeed or both fail
        db.session.commit()
        
        return {"message": "Product created", "product_id": product.id}, 201

    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500
