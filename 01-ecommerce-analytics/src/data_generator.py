import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class EcommerceDataGenerator:
    def __init__(self, n_customers=2000, n_products=200, n_transactions=10000):
        self.n_customers = n_customers
        self.n_products = n_products
        self.n_transactions = n_transactions
        np.random.seed(42)
        random.seed(42)
    
    def generate_customers(self):
        """Generate customer master data"""
        segments = ['Premium', 'Standard', 'Basic']
        regions = ['North', 'South', 'East', 'West', 'Central']
        
        customers = pd.DataFrame({
            'customer_id': range(1, self.n_customers + 1),
            'customer_segment': np.random.choice(segments, self.n_customers, p=[0.2, 0.5, 0.3]),
            'region': np.random.choice(regions, self.n_customers),
            'registration_date': pd.date_range(
                start='2022-01-01', 
                end='2024-12-31', 
                periods=self.n_customers
            ),
            'age_group': np.random.choice(['18-25', '26-35', '36-45', '46-55', '55+'], 
                                       self.n_customers, p=[0.15, 0.25, 0.25, 0.20, 0.15])
        })
        return customers
    
    def generate_products(self):
        """Generate product catalog"""
        categories = ['Electronics', 'Clothing', 'Books', 'Home', 'Sports', 'Beauty']
        
        products = pd.DataFrame({
            'product_id': range(1, self.n_products + 1),
            'category': np.random.choice(categories, self.n_products),
            'base_price': np.random.uniform(10, 500, self.n_products),
            'cost': np.random.uniform(5, 300, self.n_products)
        })
        products['profit_margin'] = (products['base_price'] - products['cost']) / products['base_price']
        return products
    
    def generate_transactions(self, customers, products):
        """Generate transaction data with realistic patterns"""
        transactions = []
        
        # Weight customers by segment (Premium customers buy more)
        customer_weights = customers['customer_segment'].map({
            'Premium': 3.0, 'Standard': 2.0, 'Basic': 1.0
        }).values
        customer_weights = customer_weights / customer_weights.sum()
        
        for i in range(self.n_transactions):
            # Select customer (weighted by segment)
            customer_id = np.random.choice(customers['customer_id'].values, p=customer_weights)
            customer_segment = customers[customers['customer_id'] == customer_id]['customer_segment'].iloc[0]
            
            # Select product
            product_id = np.random.choice(products['product_id'].values)
            base_price = products[products['product_id'] == product_id]['base_price'].iloc[0]
            
            # Adjust price based on customer segment
            price_multiplier = {'Premium': 1.1, 'Standard': 1.0, 'Basic': 0.9}
            unit_price = base_price * price_multiplier[customer_segment]
            
            # Generate transaction details
            quantity = np.random.choice([1, 2, 3, 4, 5], p=[0.5, 0.25, 0.15, 0.07, 0.03])
            
            # Generate date (more recent transactions more likely)
            days_back = np.random.exponential(30)
            transaction_date = datetime.now() - timedelta(days=min(days_back, 365))
            
            transactions.append({
                'transaction_id': i + 1,
                'customer_id': customer_id,
                'product_id': product_id,
                'quantity': quantity,
                'unit_price': round(unit_price, 2),
                'total_amount': round(quantity * unit_price, 2),
                'transaction_date': transaction_date,
                'channel': np.random.choice(['Online', 'Store'], p=[0.7, 0.3])
            })
        
        return pd.DataFrame(transactions)
    
    def generate_all_data(self):
        """Generate complete dataset"""
        customers = self.generate_customers()
        products = self.generate_products()
        transactions = self.generate_transactions(customers, products)
        
        return customers, products, transactions
    
    def save_data(self, customers, products, transactions, folder='../data/'):
        """Save all datasets to CSV files"""
        customers.to_csv(f'{folder}customers.csv', index=False)
        products.to_csv(f'{folder}products.csv', index=False)
        transactions.to_csv(f'{folder}transactions.csv', index=False)
        
        print(f"Data generated and saved:")
        print(f"- Customers: {len(customers):,}")
        print(f"- Products: {len(products):,}")
        print(f"- Transactions: {len(transactions):,}")
        print(f"- Total Revenue: ${transactions['total_amount'].sum():,.2f}")

# Usage
if __name__ == "__main__":
    generator = EcommerceDataGenerator()
    customers, products, transactions = generator.generate_all_data()
    generator.save_data(customers, products, transactions)