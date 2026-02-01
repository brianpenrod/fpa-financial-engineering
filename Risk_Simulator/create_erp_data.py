import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_erp_data():
    # Database file name
    db_file = 'financials.db'
    
    # Connect to SQLite database
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    # Create monthly_actuals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS monthly_actuals (
            month_date TEXT,
            revenue REAL,
            opex REAL
        )
    ''')
    
    # Generate 36 months of synthetic data
    start_date = datetime.now().replace(day=1) - timedelta(days=36*30)
    data = []
    
    current_revenue = 1000000.0
    growth_rate = 0.01  # 1% monthly growth
    
    for i in range(36):
        month = (start_date + timedelta(days=i*30)).strftime('%Y-%m-%d')
        
        # Revenue with random variance (+/- 5%)
        variance = np.random.uniform(0.95, 1.05)
        revenue = current_revenue * variance
        
        # OpEx roughly 60% of revenue with variance (+/- 2%)
        opex_ratio = 0.60 * np.random.uniform(0.98, 1.02)
        opex = revenue * opex_ratio
        
        data.append((month, revenue, opex))
        
        # Apply growth for next month
        current_revenue *= (1 + growth_rate)
    
    # Insert data
    cursor.executemany('INSERT INTO monthly_actuals (month_date, revenue, opex) VALUES (?, ?, ?)', data)
    
    # Commit and close
    conn.commit()
    conn.close()
    
    print('Database initialized successfully')

if __name__ == "__main__":
    create_erp_data()
