import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def generate_sample_data(filename='sales_data.csv', days=365):
    """Generate sample sales data for demonstration"""
    dates = [datetime.now() - timedelta(days=x) for x in range(days, 0, -1)]
    
    sales = np.random.randint(1000, 5000, days)
    customers = np.random.randint(10, 100, days)
    region = np.random.choice(['North', 'South', 'East', 'West'], days)
    
    df = pd.DataFrame({
        'date': dates,
        'sales': sales,
        'customers': customers,
        'region': region
    })
    
    df.to_csv(filename, index=False)
    print(f"Sample data generated: {filename}")

if __name__ == "__main__":
    generate_sample_data()
