-- Companies (Tenants)
CREATE TABLE companies (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Warehouses
CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    name VARCHAR(255),
    location TEXT
);

-- Products
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    sku VARCHAR(100),
    name VARCHAR(255),
    price DECIMAL(10, 2),
    reorder_threshold INT DEFAULT 10,
    UNIQUE(company_id, sku) -- SKUs unique per company
);

-- Inventory (Many-to-Many between Products and Warehouses)
CREATE TABLE inventory (
    id SERIAL PRIMARY KEY,
    product_id INT REFERENCES products(id),
    warehouse_id INT REFERENCES warehouses(id),
    quantity INT DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(product_id, warehouse_id)
);

-- Suppliers
CREATE TABLE suppliers (
    id SERIAL PRIMARY KEY,
    company_id INT REFERENCES companies(id),
    name VARCHAR(255),
    email VARCHAR(255)
);

-- Product Bundles (Recursive relationship)
CREATE TABLE product_bundles (
    parent_product_id INT REFERENCES products(id),
    child_product_id INT REFERENCES products(id),
    quantity_required INT,
    PRIMARY KEY (parent_product_id, child_product_id)
);

-- Inventory Audit Log (For tracking history)
CREATE TABLE inventory_log (
    id SERIAL PRIMARY KEY,
    inventory_id INT REFERENCES inventory(id),
    previous_qty INT,
    new_qty INT,
    change_reason VARCHAR(50), -- e.g., 'sale', 'restock', 'damage'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
