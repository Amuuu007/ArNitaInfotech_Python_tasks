import pandas as pd
import numpy as np
from datetime import datetime
from abc import ABC, abstractmethod
import warnings
warnings.filterwarnings('ignore')

class SalesData:
    """Handle sales data loading and basic operations"""
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None
    
    def load_csv(self):
        """Load data from CSV file"""
        self.data = pd.read_csv(self.filepath)
        print(f"Data loaded successfully: {self.data.shape}")
        return self.data
    
    def get_summary(self):
        """Return basic data summary"""
        return {
            'shape': self.data.shape,
            'columns': self.data.columns.tolist(),
            'dtypes': self.data.dtypes.to_dict(),
            'missing': self.data.isnull().sum().to_dict()
        }


class DataProcessor:
    """Process and clean sales data"""
    def __init__(self, data):
        self.data = data.copy()
    
    def clean_data(self):
        """Remove duplicates and invalid rows"""
        self.data = self.data.drop_duplicates()
        return self.data
    
    def handle_missing(self, method='mean'):
        """Handle missing values"""
        if method == 'mean':
            self.data.fillna(self.data.mean(numeric_only=True), inplace=True)
        elif method == 'forward_fill':
            self.data.fillna(method='ffill', inplace=True)
        return self.data
    
    def aggregate_data(self, date_col, value_col, freq='D'):
        """Aggregate data by date"""
        self.data[date_col] = pd.to_datetime(self.data[date_col])
        aggregated = self.data.set_index(date_col)[value_col].resample(freq).sum()
        return aggregated.reset_index()


class Analyzer:
    """Statistical analysis and EDA"""
    def __init__(self, data):
        self.data = data
    
    def get_statistics(self, column):
        """Calculate basic statistics"""
        return {
            'mean': self.data[column].mean(),
            'median': self.data[column].median(),
            'std': self.data[column].std(),
            'min': self.data[column].min(),
            'max': self.data[column].max()
        }
    
    def correlation_analysis(self):
        """Calculate correlation matrix"""
        return self.data.corr(numeric_only=True)
    
    def trend_analysis(self, date_col, value_col):
        """Analyze trend over time"""
        monthly = self.data.set_index(date_col)[value_col].resample('M').sum()
        return monthly


class Forecaster(ABC):
    """Abstract base class for forecasting"""
    def __init__(self, data, test_size=0.2):
        self.data = data
        self.test_size = test_size
        self.train = None
        self.test = None
    
    def train_test_split(self):
        """Split data into train and test sets"""
        split_idx = int(len(self.data) * (1 - self.test_size))
        self.train = self.data[:split_idx]
        self.test = self.data[split_idx:]
    
    @abstractmethod
    def forecast(self, periods):
        """Forecast future values"""
        pass
    
    def calculate_rmse(self, actual, predicted):
        """Calculate Root Mean Square Error"""
        return np.sqrt(np.mean((actual - predicted) ** 2))


class SimpleExponentialSmoothing(Forecaster):
    """Exponential Smoothing forecaster"""
    def __init__(self, data, alpha=0.3, test_size=0.2):
        super().__init__(data, test_size)
        self.alpha = alpha
        self.forecast_values = None
    
    def forecast(self, periods):
        """Forecast using exponential smoothing"""
        self.train_test_split()
        
        smoothed = [self.train[0]]
        for i in range(1, len(self.train)):
            smoothed.append(self.alpha * self.train[i-1] + (1 - self.alpha) * smoothed[i-1])
        
        future_forecast = [smoothed[-1]]
        for _ in range(periods - 1):
            future_forecast.append(self.alpha * future_forecast[-1] + (1 - self.alpha) * future_forecast[-1])
        
        self.forecast_values = future_forecast
        return future_forecast


class Reporter:
    """Generate reports and summaries"""
    def __init__(self, analyzer, forecaster):
        self.analyzer = analyzer
        self.forecaster = forecaster
    
    def generate_summary_report(self):
        """Generate comprehensive report"""
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'data_shape': self.analyzer.data.shape,
            'forecast_values': self.forecaster.forecast_values
        }
        return report
    
    def export_report(self, filename='report.txt'):
        """Export report to file"""
        report = self.generate_summary_report()
        with open(filename, 'w') as f:
            f.write(f"Sales Forecasting Report\n")
            f.write(f"Generated: {report['timestamp']}\n")
            f.write(f"Data Shape: {report['data_shape']}\n")
            f.write(f"Forecast: {report['forecast_values']}\n")
        print(f"Report saved to {filename}")
