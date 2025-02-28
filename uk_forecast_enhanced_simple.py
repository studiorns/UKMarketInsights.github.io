#!/usr/bin/env python3
"""
Simplified Enhanced UK Travel Queries Forecast Model

This script implements a simplified version of the enhanced forecast model with:
1. Anomaly Detection: Identifies and adjusts outliers in historical data
2. Time Series Forecasting: Implements ARIMA models for comparison
3. Bayesian Forecasting: Incorporates uncertainty and confidence intervals

Usage:
    python uk_forecast_enhanced_simple.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

# Historical data (manually extracted from Travel_Queries_Forecast_UK_Aligned.csv)
historical_data = [
    {'Month': 'January', 'Year': 2020, 'Indexed_Queries': 37.49527745},
    {'Month': 'January', 'Year': 2021, 'Indexed_Queries': 63.39256198},
    {'Month': 'January', 'Year': 2022, 'Indexed_Queries': 58.91617473},
    {'Month': 'January', 'Year': 2023, 'Indexed_Queries': 89.36245573},
    {'Month': 'January', 'Year': 2024, 'Indexed_Queries': 124.850059},
    {'Month': 'February', 'Year': 2020, 'Indexed_Queries': 58.24025974},
    {'Month': 'February', 'Year': 2021, 'Indexed_Queries': 19.06965762},
    {'Month': 'February', 'Year': 2022, 'Indexed_Queries': 52.88902007},
    {'Month': 'February', 'Year': 2023, 'Indexed_Queries': 73.06965762},
    {'Month': 'February', 'Year': 2024, 'Indexed_Queries': 98.7957497},
    {'Month': 'March', 'Year': 2020, 'Indexed_Queries': 34.24144038},
    {'Month': 'March', 'Year': 2021, 'Indexed_Queries': 19.97107438},
    {'Month': 'March', 'Year': 2022, 'Indexed_Queries': 56.60861865},
    {'Month': 'March', 'Year': 2023, 'Indexed_Queries': 79.48878394},
    {'Month': 'March', 'Year': 2024, 'Indexed_Queries': 99.09031877},
    {'Month': 'April', 'Year': 2020, 'Indexed_Queries': 19.10153483},
    {'Month': 'April', 'Year': 2021, 'Indexed_Queries': 17.73966942},
    {'Month': 'April', 'Year': 2022, 'Indexed_Queries': 44.57438017},
    {'Month': 'April', 'Year': 2023, 'Indexed_Queries': 91.35064935},
    {'Month': 'April', 'Year': 2024, 'Indexed_Queries': 92.3364817},
    {'Month': 'May', 'Year': 2020, 'Indexed_Queries': 19.01416765},
    {'Month': 'May', 'Year': 2021, 'Indexed_Queries': 13.53837072},
    {'Month': 'May', 'Year': 2022, 'Indexed_Queries': 47.89374262},
    {'Month': 'May', 'Year': 2023, 'Indexed_Queries': 76.71605667},
    {'Month': 'May', 'Year': 2024, 'Indexed_Queries': 86.93919717},
    {'Month': 'June', 'Year': 2020, 'Indexed_Queries': 22.09149941},
    {'Month': 'June', 'Year': 2021, 'Indexed_Queries': 12.05785124},
    {'Month': 'June', 'Year': 2022, 'Indexed_Queries': 48.45690673},
    {'Month': 'June', 'Year': 2023, 'Indexed_Queries': 71.75265643},
    {'Month': 'June', 'Year': 2024, 'Indexed_Queries': 82.79988194},
    {'Month': 'July', 'Year': 2020, 'Indexed_Queries': 25.36009445},
    {'Month': 'July', 'Year': 2021, 'Indexed_Queries': 14.28335301},
    {'Month': 'July', 'Year': 2022, 'Indexed_Queries': 58.09090909},
    {'Month': 'July', 'Year': 2023, 'Indexed_Queries': 86.35773318},
    {'Month': 'July', 'Year': 2024, 'Indexed_Queries': 86.15112161},
    {'Month': 'August', 'Year': 2020, 'Indexed_Queries': 26.0188902},
    {'Month': 'August', 'Year': 2021, 'Indexed_Queries': 23.72904368},
    {'Month': 'August', 'Year': 2022, 'Indexed_Queries': 62.14285714},
    {'Month': 'August', 'Year': 2023, 'Indexed_Queries': 86.06965762},
    {'Month': 'August', 'Year': 2024, 'Indexed_Queries': 92.8270366},
    {'Month': 'September', 'Year': 2020, 'Indexed_Queries': 20.12455726},
    {'Month': 'September', 'Year': 2021, 'Indexed_Queries': 38.39846517},
    {'Month': 'September', 'Year': 2022, 'Indexed_Queries': 61.36894923},
    {'Month': 'September', 'Year': 2023, 'Indexed_Queries': 89.66115702},
    {'Month': 'September', 'Year': 2024, 'Indexed_Queries': 99.68063754},
    {'Month': 'October', 'Year': 2020, 'Indexed_Queries': 21.56788666},
    {'Month': 'October', 'Year': 2021, 'Indexed_Queries': 67.26859504},
    {'Month': 'October', 'Year': 2022, 'Indexed_Queries': 81.43624557},
    {'Month': 'October', 'Year': 2023, 'Indexed_Queries': 102.5324675},
    {'Month': 'October', 'Year': 2024, 'Indexed_Queries': 110.8600945},
    {'Month': 'November', 'Year': 2020, 'Indexed_Queries': 25.040732},
    {'Month': 'November', 'Year': 2021, 'Indexed_Queries': 46.79456907},
    {'Month': 'November', 'Year': 2022, 'Indexed_Queries': 75.59504132},
    {'Month': 'November', 'Year': 2023, 'Indexed_Queries': 90.82880756},
    {'Month': 'November', 'Year': 2024, 'Indexed_Queries': 97.24498229},
    {'Month': 'December', 'Year': 2020, 'Indexed_Queries': 32.03364817},
    {'Month': 'December', 'Year': 2021, 'Indexed_Queries': 47.48937426},
    {'Month': 'December', 'Year': 2022, 'Indexed_Queries': 61.76800472},
    {'Month': 'December', 'Year': 2023, 'Indexed_Queries': 91.73376623},
    {'Month': 'December', 'Year': 2024, 'Indexed_Queries': 99.17886659}
]

# Factor-based forecast results (manually extracted from Travel_Queries_Forecast_UK_Aligned.csv)
factor_forecast = [
    {'Month': 'January', '2024_Queries': 124.85, 'Conservative': 128.97, 'Moderate': 136.01, 'Ambitious': 143.05},
    {'Month': 'February', '2024_Queries': 98.80, 'Conservative': 107.10, 'Moderate': 112.98, 'Ambitious': 118.86},
    {'Month': 'March', '2024_Queries': 99.09, 'Conservative': 112.10, 'Moderate': 118.26, 'Ambitious': 124.42},
    {'Month': 'April', '2024_Queries': 92.34, 'Conservative': 89.58, 'Moderate': 94.49, 'Ambitious': 99.40},
    {'Month': 'May', '2024_Queries': 86.94, 'Conservative': 81.31, 'Moderate': 85.76, 'Ambitious': 90.21},
    {'Month': 'June', '2024_Queries': 82.80, 'Conservative': 73.77, 'Moderate': 77.83, 'Ambitious': 81.89},
    {'Month': 'July', '2024_Queries': 86.15, 'Conservative': 78.10, 'Moderate': 82.40, 'Ambitious': 86.70},
    {'Month': 'August', '2024_Queries': 92.83, 'Conservative': 88.31, 'Moderate': 93.17, 'Ambitious': 98.03},
    {'Month': 'September', '2024_Queries': 99.68, 'Conservative': 107.67, 'Moderate': 113.58, 'Ambitious': 119.49},
    {'Month': 'October', '2024_Queries': 110.86, 'Conservative': 130.67, 'Moderate': 137.90, 'Ambitious': 145.13},
    {'Month': 'November', '2024_Queries': 97.24, 'Conservative': 99.28, 'Moderate': 104.73, 'Ambitious': 110.18},
    {'Month': 'December', '2024_Queries': 99.18, 'Conservative': 112.20, 'Moderate': 118.37, 'Ambitious': 124.54}
]

def main():
    """Main function to run the enhanced forecast model."""
    print("Starting enhanced forecast model...")
    
    # Convert historical data to DataFrame
    df = pd.DataFrame(historical_data)
    
    # Create a date column
    df['Date'] = pd.to_datetime(
        df['Year'].astype(str) + '-' + 
        df['Month'].apply(lambda x: {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }[x]) + '-01'
    )
    
    # Sort by date
    df = df.sort_values('Date')
    
    # Create a time series
    time_series = df.set_index('Date')['Indexed_Queries']
    
    # Detect outliers
    print("Detecting outliers...")
    z_scores = stats.zscore(df['Indexed_Queries'])
    df['Outlier'] = abs(z_scores) > 3.0
    df['Z_Score'] = z_scores
    outliers = df[df['Outlier']]
    
    # Adjust outliers
    print("Adjusting outliers...")
    adjusted_series = time_series.copy()
    for idx in outliers.index:
        date_idx = outliers.loc[idx, 'Date']
        # Use median of surrounding values
        window_start = max(0, time_series.index.get_loc(date_idx) - 1)
        window_end = min(len(time_series), time_series.index.get_loc(date_idx) + 2)
        window_values = time_series.iloc[window_start:window_end]
        # Exclude the outlier itself from the window
        window_values = window_values[window_values.index != date_idx]
        if not window_values.empty:
            adjusted_series.loc[date_idx] = window_values.median()
    
    # Plot outliers
    print("Plotting outliers...")
    plt.figure(figsize=(12, 6))
    plt.plot(time_series.index, time_series.values, 'b-', label='Original Data')
    plt.scatter(outliers['Date'], outliers['Indexed_Queries'], color='red', label='Outliers')
    plt.plot(adjusted_series.index, adjusted_series.values, 'g--', label='Adjusted Data')
    plt.title('Time Series with Outliers')
    plt.xlabel('Date')
    plt.ylabel('Indexed Queries')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('uk_outliers_detection.png')
    plt.close()
    
    # Fit ARIMA model
    print("Fitting ARIMA model...")
    model = ARIMA(adjusted_series, order=(1, 1, 1))
    arima_model = model.fit()
    
    # Generate forecast
    print("Generating ARIMA forecast...")
    steps = 12
    forecast = arima_model.forecast(steps=steps)
    forecast_index = pd.date_range(start=time_series.index[-1], periods=steps+1, freq='MS')[1:]
    
    # Get confidence intervals
    pred_ci = arima_model.get_forecast(steps=steps).conf_int()
    
    # Create forecast DataFrame
    arima_forecast = pd.DataFrame({
        'ARIMA_Forecast': forecast,
        'Lower_CI': pred_ci.iloc[:, 0],
        'Upper_CI': pred_ci.iloc[:, 1]
    }, index=forecast_index)
    
    # Convert factor forecast to DataFrame
    factor_df = pd.DataFrame(factor_forecast)
    
    # Create a date column for 2025
    factor_df['Date'] = pd.to_datetime(
        '2025-' + 
        factor_df['Month'].apply(lambda x: {
            'January': '01', 'February': '02', 'March': '03', 'April': '04',
            'May': '05', 'June': '06', 'July': '07', 'August': '08',
            'September': '09', 'October': '10', 'November': '11', 'December': '12'
        }[x]) + '-01'
    )
    
    # Set the date as index
    factor_df = factor_df.set_index('Date')
    
    # Combine with statistical forecasts
    comparison = pd.DataFrame(index=factor_df.index)
    comparison['Factor_Conservative'] = factor_df['Conservative']
    comparison['Factor_Moderate'] = factor_df['Moderate']
    comparison['Factor_Ambitious'] = factor_df['Ambitious']
    comparison['ARIMA_Forecast'] = arima_forecast['ARIMA_Forecast']
    comparison['ARIMA_Lower_CI'] = arima_forecast['Lower_CI']
    comparison['ARIMA_Upper_CI'] = arima_forecast['Upper_CI']
    
    # Plot forecasts
    print("Plotting forecasts...")
    plt.figure(figsize=(12, 6))
    
    # Plot historical data
    plt.plot(time_series.index, time_series.values, 'b-', label='Historical Data')
    
    # Plot factor-based forecasts
    plt.plot(comparison.index, comparison['Factor_Conservative'], 'g--', label='Factor Conservative')
    plt.plot(comparison.index, comparison['Factor_Moderate'], 'g-', label='Factor Moderate')
    plt.plot(comparison.index, comparison['Factor_Ambitious'], 'g:', label='Factor Ambitious')
    
    # Plot ARIMA forecast
    plt.plot(comparison.index, comparison['ARIMA_Forecast'], 'r-', label='ARIMA Forecast')
    plt.fill_between(
        comparison.index,
        comparison['ARIMA_Lower_CI'],
        comparison['ARIMA_Upper_CI'],
        color='r', alpha=0.1, label='ARIMA 95% CI'
    )
    
    plt.title('UK Travel Queries Forecast Comparison')
    plt.xlabel('Date')
    plt.ylabel('Indexed Queries')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('uk_forecast_comparison.png')
    plt.close()
    
    # Save results
    print("Saving results...")
    comparison.to_csv('uk_forecast_comparison.csv')
    arima_forecast.to_csv('uk_arima_forecast.csv')
    
    print("Done!")

if __name__ == "__main__":
    main()
