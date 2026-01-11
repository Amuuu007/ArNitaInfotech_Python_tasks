from sales_forecasting import (SalesData, DataProcessor, Analyzer, 
                               SimpleExponentialSmoothing, Reporter)

def main():
    # Step 1: Load data
    sales_data = SalesData('sales_data.csv')
    data = sales_data.load_csv()
    print("Summary:", sales_data.get_summary())
    
    # Step 2: Process data
    processor = DataProcessor(data)
    processor.clean_data()
    processor.handle_missing(method='mean')
    print("Data processed successfully")
    
    # Step 3: Analyze data
    analyzer = Analyzer(processor.data)
    print("Statistics:", analyzer.get_statistics('sales'))
    print("Correlations:\n", analyzer.correlation_analysis())
    
    # Step 4: Forecast
    sales_series = processor.data['sales'].values
    forecaster = SimpleExponentialSmoothing(sales_series, alpha=0.3)
    forecast = forecaster.forecast(periods=12)
    print("12-Month Forecast:", forecast)
    
    # Step 5: Generate report
    reporter = Reporter(analyzer, forecaster)
    report = reporter.generate_summary_report()
    
    # Display report in console
    print("\n" + "="*50)
    print("SALES FORECASTING REPORT")
    print("="*50)
    print(f"Generated: {report['timestamp']}")
    print(f"Data Shape: {report['data_shape']}")
    print(f"12-Month Forecast: {report['forecast_values']}")
    print("="*50 + "\n")
    
    # Save report to file
    reporter.export_report('sales_report.txt')

if __name__ == "__main__":
    main()
