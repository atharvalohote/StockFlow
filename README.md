# StockFlow - Backend Case Study Submission

## Overview
This repository contains my solutions for the StockFlow backend case study. 
Time taken: ~85 minutes.

## Part 1: Code Review & Debugging
**File:** `part1_fix.py`

### Issues Identified
1.  **Atomicity:** The original code had two separate commits. If the second failed, we would have data inconsistency. I wrapped them in a single transaction.
2.  **Schema Logic:** `warehouse_id` was on the Product table, which limits a product to a single warehouse. I removed it from Product and ensured it lives in the Inventory table.
3.  **Validation:** Added basic checks for missing fields.

## Part 2: Database Design
**File:** `part2_schema.sql`

### Design Decisions
* **Tenant Isolation:** Added `company_id` to Products and Warehouses to ensure data safety between clients.
* **Inventory Logs:** Created a dedicated `inventory_log` table. Simple timestamps aren't enough for auditing theft or shrinkage.
* **Bundles:** Used a self-referencing many-to-many table (`product_bundles`) to allow products to be composed of other products recursively.

### Missing Requirements (Gaps)
* **Currency:** If warehouses are in different countries, we need currency handling.
* **Reserved Stock:** How do we handle items currently in a user's cart? Do we reserve them?
* **Unit of Measure:** Do we buy in kg and sell in grams? We might need conversion logic.

## Part 3: API Implementation
**File:** `part3_api.py`

### Assumptions
* There is a helper function available to calculate daily sales velocity.
* We only want to alert for products that are actually selling (dead stock is ignored to reduce noise).
* The database models (`Product`, `Inventory`) are already defined in the ORM.
