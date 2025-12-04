from flask import jsonify
from models import db, Inventory, Product

@app.route('/api/companies/<int:company_id>/alerts/low-stock', methods=['GET'])
def get_low_stock_alerts(company_id):
    # Fetch all inventory items below the reorder threshold
    low_stock_items = (
        db.session.query(Inventory)
        .join(Product)
        .filter(Product.company_id == company_id)
        .filter(Inventory.quantity <= Product.reorder_threshold)
        .all()
    )
    
    alerts = []
    
    for item in low_stock_items:
        # Helper function to get sales velocity (assumed to exist)
        daily_sales = get_average_daily_sales(item.product_id)
        
        # Business Logic: Don't alert if the product isn't selling
        if daily_sales == 0:
            continue

        days_left = int(item.quantity / daily_sales)
        
        # Logic for determing primary supplier 
        primary_supplier = item.product.suppliers[0] if item.product.suppliers else None
        
        alert_obj = {
            "product_id": item.product.id,
            "product_name": item.product.name,
            "sku": item.product.sku,
            "warehouse_id": item.warehouse.id,
            "warehouse_name": item.warehouse.name,
            "current_stock": item.quantity,
            "threshold": item.product.reorder_threshold,
            "days_until_stockout": days_left,
            "supplier": {
                "id": primary_supplier.id if primary_supplier else None,
                "name": primary_supplier.name if primary_supplier else "Unknown",
                "contact_email": primary_supplier.email if primary_supplier else None
            }
        }
        alerts.append(alert_obj)

    # Return the final JSON reponse
    return jsonify({
        "alerts": alerts,
        "total_alerts": len(alerts)
    }), 200

def get_average_daily_sales(product_id):
    # Mock implementation
    return 2.5
