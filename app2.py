import pandas as pd
import numpy as np
import random
from faker import Faker

fake = Faker()

# Function to generate synthetic inventory data
def generate_inventory_data(num_products=50):
    data = []
    for i in range(num_products):
        product_id = f"P{i+1:03}"
        product_name = fake.word().capitalize()
        current_stock = random.randint(10, 500)
        reorder_point = random.randint(5, 50)
        warehouse_location = fake.city()
        data.append([product_id, product_name, current_stock, reorder_point, warehouse_location])
    columns = ["Product ID", "Product Name", "Current Stock Level", "Reorder Point", "Warehouse Location"]
    return pd.DataFrame(data, columns=columns)

# Function to generate synthetic sales data
def generate_sales_data(num_sales=200):
    data = []
    for _ in range(num_sales):
        product_id = f"P{random.randint(1, 50):03}"
        date_of_sale = fake.date_this_year()
        quantity_sold = random.randint(1, 10)
        store_location = fake.city()
        data.append([product_id, date_of_sale, quantity_sold, store_location])
    columns = ["Product ID", "Date of Sale", "Quantity Sold", "Store Location"]
    return pd.DataFrame(data, columns=columns)

# Function to generate synthetic customer data
def generate_customer_data(num_customers=100):
    data = []
    for i in range(num_customers):
        customer_id = f"C{i+1:03}"
        purchase_history = [f"P{random.randint(1, 50):03}" for _ in range(random.randint(1, 5))]
        preferred_products = random.sample(purchase_history, min(len(purchase_history), 3))
        avg_spend = round(random.uniform(20.0, 500.0), 2)
        data.append([customer_id, purchase_history, preferred_products, avg_spend])
    columns = ["Customer ID", "Purchase History", "Preferred Products", "Average Spend"]
    return pd.DataFrame(data, columns=columns)

# Generate and save synthetic data to CSV files
inventory_data = generate_inventory_data()
sales_data = generate_sales_data()
customer_data = generate_customer_data()

inventory_data.to_csv("synthetic_inventory_data.csv", index=False)
sales_data.to_csv("synthetic_sales_data.csv", index=False)
customer_data.to_csv("synthetic_customer_data.csv", index=False)

print("Synthetic data has been generated and saved as CSV files.")