#!/usr/bin/env python3
"""
Enhanced UK Travel Queries Forecast Model

This script enhances the existing factor-based forecast model with:
1. Anomaly Detection: Identifies and adjusts outliers in historical data
2. Time Series Forecasting: Implements ARIMA models for comparison
3. Bayesian Forecasting: Incorporates uncertainty and confidence intervals

Usage:
    python uk_forecast_enhanced_model.py

Requirements:
    - pandas
    - numpy
    - matplotlib
    - statsmodels
    - scipy
    - prophet (Facebook Prophet)
    - pymc3 (for Bayesian modeling)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from scipy import stats
import os
import warnings
warnings.filterwarnings('ignore')

# Try to import Prophet, but continue if not available
try:
    from prophet import Prophet
    prophet_available = True
except ImportError:
    prophet_available = False
    print("Facebook Prophet not available. Prophet forecasting will be skipped.")

# Try to import PyMC3, but continue if not available
try:
    import pymc3 as pm
    import theano.tensor as tt
    pymc3_available = True
except ImportError:
    pymc3_available = False
    print("PyMC3 not available. Bayesian forecasting will be skipped.")

class EnhancedForecastModel:
    def __init__(self, csv_path):
        """Initialize the enhanced forecast model with data from the CSV file."""
        self.csv_path = csv_path
        self.load_data()
        self.prepare_time_series()
        
    def load_data(self):
        """Load data from the CSV file and extract historical queries."""
        try:
            # Try to use pandas to read the CSV directly
            # This is a simpler approach but might not work with the custom format
            try:
                # Skip rows until we find the HISTORICAL QUERIES section
                skip_rows = 0
                with open(self.csv_path, 'r') as file:
                    for line in file:
                        skip_rows += 1
                        if 'HISTORICAL QUERIES' in line:
                            break
                
                # Read the historical queries section
                self.historical_data = pd.read_csv(
                    self.csv_path, 
                    skiprows=skip_rows+1,  # Skip the section header and column header
                    nrows=60,  # Assuming there are at most 60 rows of historical data
                    usecols=[0, 1, 2],  # Only use the first three columns
                    names=['Month', 'Year', 'Indexed_Queries']  # Set column names
                )
                
                # Convert Year to integer and Indexed_Queries to float
                self.historical_data['Year'] = self.historical_data['Year'].astype(int)
                self.historical_data['Indexed_Queries'] = self.historical_data['Indexed_Queries'].astype(float)
                
                # Remove any rows with NaN values
                self.historical_data = self.historical_data.dropna()
                
                print(f"Loaded {len(self.historical_data)} rows of historical data")
                
            except Exception as e:
                print(f"Error reading CSV with pandas: {e}")
                print("Falling back to manual parsing...")
                
                # Manual parsing as a fallback
                with open(self.csv_path, 'r') as file:
                    content = file.read()
                
                # Split the content by section markers
                sections = content.split('====================')
                
                # Find the historical queries section
                historical_queries_section = None
                for section in sections:
                    if 'HISTORICAL QUERIES' in section:
                        historical_queries_section = section
                        break
                
                if historical_queries_section is None:
                    raise ValueError("Historical queries section not found in the CSV file")
                
                # Parse the historical queries section
                lines = historical_queries_section.strip().split('\n')
                
                # Find the header line
                header_line_idx = -1
                for i, line in enumerate(lines):
                    if 'Month,Year,Indexed Queries' in line:
                        header_line_idx = i
                        break
                
                if header_line_idx == -1:
                    raise ValueError("Header line not found in historical queries section")
                
                # Skip the header lines
                data_lines = lines[header_line_idx+1:]
                
                # Create a DataFrame
                data = []
                for line in data_lines:
                    if not line.strip() or ',' not in line:
                        continue
                    
                    parts = line.split(',')
                    if len(parts) >= 3 and parts[2].strip():
                        try:
                            month = parts[0].strip()
                            year = int(parts[1].strip())
                            queries = float(parts[2].strip())
                            data.append({'Month': month, 'Year': year, 'Indexed_Queries': queries})
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing line: {line}, error: {e}")
                
                self.historical_data = pd.DataFrame(data)
                print(f"Loaded {len(self.historical_data)} rows of historical data using manual parsing")
        
        except Exception as e:
            print(f"Error loading data: {e}")
            raise
        
    def prepare_time_series(self):
        """Prepare the time series data for analysis."""
        # Create a date column
        self.historical_data['Date'] = pd.to_datetime(
            self.historical_data['Year'].astype(str) + '-' + 
            self.historical_data['Month'].apply(lambda x: {
                'January': '01', 'February': '02', 'March': '03', 'April': '04',
                'May': '05', 'June': '06', 'July': '07', 'August': '08',
                'September': '09', 'October': '10', 'November': '11', 'December': '12'
            }[x]) + '-01'
        )
        
        # Sort by date
        self.historical_data = self.historical_data.sort_values('Date')
        
        # Create a time series
        self.time_series = self.historical_data.set_index('Date')['Indexed_Queries']
        
    def detect_outliers(self, method='zscore', threshold=3.0):
        """
        Detect outliers in the historical data.
        
        Parameters:
        - method: Method to use for outlier detection ('zscore', 'iqr')
        - threshold: Threshold for outlier detection
        
        Returns:
        - DataFrame with outliers flagged
        """
        data = self.historical_data.copy()
        
        if method == 'zscore':
            # Z-score method
            z_scores = stats.zscore(data['Indexed_Queries'])
            data['Outlier'] = abs(z_scores) > threshold
            data['Z_Score'] = z_scores
            
        elif method == 'iqr':
            # IQR method
            Q1 = data['Indexed_Queries'].quantile(0.25)
            Q3 = data['Indexed_Queries'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            data['Outlier'] = (data['Indexed_Queries'] < lower_bound) | (data['Indexed_Queries'] > upper_bound)
            
        else:
            raise ValueError(f"Unknown outlier detection method: {method}")
        
        self.outliers = data[data['Outlier']]
        return data
    
    def adjust_outliers(self, method='median_window', window_size=3):
        """
        Adjust outliers in the historical data.
        
        Parameters:
        - method: Method to use for outlier adjustment ('median_window', 'mean_window', 'linear_interp')
        - window_size: Size of the window for median/mean methods
        
        Returns:
        - Series with adjusted values
        """
        # Detect outliers if not already done
        if not hasattr(self, 'outliers'):
            self.detect_outliers()
        
        # Create a copy of the time series
        adjusted_series = self.time_series.copy()
        
        # Get the indices of outliers
        outlier_indices = self.outliers.index
        
        for idx in outlier_indices:
            if method == 'median_window':
                # Use median of surrounding values
                window_start = max(0, self.time_series.index.get_loc(idx) - window_size // 2)
                window_end = min(len(self.time_series), self.time_series.index.get_loc(idx) + window_size // 2 + 1)
                window_values = self.time_series.iloc[window_start:window_end]
                # Exclude the outlier itself from the window
                window_values = window_values[window_values.index != idx]
                if not window_values.empty:
                    adjusted_series.loc[idx] = window_values.median()
                
            elif method == 'mean_window':
                # Use mean of surrounding values
                window_start = max(0, self.time_series.index.get_loc(idx) - window_size // 2)
                window_end = min(len(self.time_series), self.time_series.index.get_loc(idx) + window_size // 2 + 1)
                window_values = self.time_series.iloc[window_start:window_end]
                # Exclude the outlier itself from the window
                window_values = window_values[window_values.index != idx]
                if not window_values.empty:
                    adjusted_series.loc[idx] = window_values.mean()
                
            elif method == 'linear_interp':
                # Use linear interpolation
                adjusted_series.loc[idx] = np.nan
                
        # Fill any NaN values with linear interpolation
        if method == 'linear_interp':
            adjusted_series = adjusted_series.interpolate(method='linear')
        
        self.adjusted_series = adjusted_series
        return adjusted_series
    
    def fit_arima_model(self, p=1, d=1, q=1):
        """
        Fit an ARIMA model to the adjusted time series.
        
        Parameters:
        - p: Order of the AR term
        - d: Order of differencing
        - q: Order of the MA term
        
        Returns:
        - Fitted ARIMA model
        """
        # Use adjusted series if available, otherwise use original
        series = self.adjusted_series if hasattr(self, 'adjusted_series') else self.time_series
        
        # Fit ARIMA model
        model = ARIMA(series, order=(p, d, q))
        self.arima_model = model.fit()
        return self.arima_model
    
    def forecast_arima(self, steps=12):
        """
        Generate forecasts using the ARIMA model.
        
        Parameters:
        - steps: Number of steps to forecast
        
        Returns:
        - DataFrame with forecasts and confidence intervals
        """
        # Fit ARIMA model if not already done
        if not hasattr(self, 'arima_model'):
            self.fit_arima_model()
        
        # Generate forecast
        forecast = self.arima_model.forecast(steps=steps)
        forecast_index = pd.date_range(start=self.time_series.index[-1], periods=steps+1, freq='MS')[1:]
        
        # Get confidence intervals
        pred_ci = self.arima_model.get_forecast(steps=steps).conf_int()
        
        # Create forecast DataFrame
        forecast_df = pd.DataFrame({
            'ARIMA_Forecast': forecast,
            'Lower_CI': pred_ci.iloc[:, 0],
            'Upper_CI': pred_ci.iloc[:, 1]
        }, index=forecast_index)
        
        self.arima_forecast = forecast_df
        return forecast_df
    
    def fit_prophet_model(self):
        """
        Fit a Prophet model to the adjusted time series.
        
        Returns:
        - Fitted Prophet model
        """
        if not prophet_available:
            print("Prophet not available. Skipping Prophet forecasting.")
            return None
        
        # Use adjusted series if available, otherwise use original
        series = self.adjusted_series if hasattr(self, 'adjusted_series') else self.time_series
        
        # Prepare data for Prophet
        df = pd.DataFrame({
            'ds': series.index,
            'y': series.values
        })
        
        # Fit Prophet model
        model = Prophet(yearly_seasonality=True, weekly_seasonality=False, daily_seasonality=False)
        model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
        model.fit(df)
        
        self.prophet_model = model
        return model
    
    def forecast_prophet(self, periods=12):
        """
        Generate forecasts using the Prophet model.
        
        Parameters:
        - periods: Number of periods to forecast
        
        Returns:
        - DataFrame with forecasts and confidence intervals
        """
        if not prophet_available:
            print("Prophet not available. Skipping Prophet forecasting.")
            return None
        
        # Fit Prophet model if not already done
        if not hasattr(self, 'prophet_model'):
            self.fit_prophet_model()
        
        # Create future dataframe
        future = self.prophet_model.make_future_dataframe(periods=periods, freq='MS')
        
        # Generate forecast
        forecast = self.prophet_model.predict(future)
        
        # Extract relevant columns
        prophet_forecast = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
        prophet_forecast = prophet_forecast.rename(columns={
            'ds': 'Date',
            'yhat': 'Prophet_Forecast',
            'yhat_lower': 'Lower_CI',
            'yhat_upper': 'Upper_CI'
        })
        prophet_forecast = prophet_forecast.set_index('Date')
        
        self.prophet_forecast = prophet_forecast
        return prophet_forecast
    
    def bayesian_forecast(self, periods=12, samples=1000):
        """
        Generate forecasts using Bayesian methods.
        
        Parameters:
        - periods: Number of periods to forecast
        - samples: Number of samples for the Bayesian model
        
        Returns:
        - DataFrame with forecasts and credible intervals
        """
        if not pymc3_available:
            print("PyMC3 not available. Skipping Bayesian forecasting.")
            return None
        
        # Use adjusted series if available, otherwise use original
        series = self.adjusted_series if hasattr(self, 'adjusted_series') else self.time_series
        
        # Prepare data
        data = series.values
        T = len(data)
        
        # Define the Bayesian model
        with pm.Model() as model:
            # Define priors for the parameters
            sigma = pm.HalfCauchy('sigma', beta=10)
            
            # Define the AR(1) process
            alpha = pm.Normal('alpha', mu=0, sigma=10)
            beta = pm.Normal('beta', mu=0.9, sigma=0.1)
            
            # Define the likelihood
            obs = pm.AR('obs', alpha, beta, sigma=sigma, observed=data)
            
            # Sample from the posterior
            trace = pm.sample(samples, tune=1000, return_inferencedata=False)
        
        # Generate forecasts
        last_value = data[-1]
        forecasts = []
        lower_cis = []
        upper_cis = []
        
        # Extract posterior samples
        alpha_samples = trace['alpha']
        beta_samples = trace['beta']
        sigma_samples = trace['sigma']
        
        # Generate forecasts for each period
        for i in range(periods):
            # Generate forecast samples
            forecast_samples = alpha_samples + beta_samples * last_value + np.random.normal(0, sigma_samples)
            
            # Calculate forecast and credible intervals
            forecast = np.mean(forecast_samples)
            lower_ci = np.percentile(forecast_samples, 2.5)
            upper_ci = np.percentile(forecast_samples, 97.5)
            
            # Store results
            forecasts.append(forecast)
            lower_cis.append(lower_ci)
            upper_cis.append(upper_ci)
            
            # Update last value for next period
            last_value = forecast
        
        # Create forecast DataFrame
        forecast_index = pd.date_range(start=series.index[-1], periods=periods+1, freq='MS')[1:]
        bayesian_forecast = pd.DataFrame({
            'Bayesian_Forecast': forecasts,
            'Lower_CI': lower_cis,
            'Upper_CI': upper_cis
        }, index=forecast_index)
        
        self.bayesian_forecast = bayesian_forecast
        return bayesian_forecast
    
    def compare_with_factor_model(self, factor_model_path):
        """
        Compare the statistical forecasts with the factor-based model.
        
        Parameters:
        - factor_model_path: Path to the factor-based model CSV file
        
        Returns:
        - DataFrame with comparison of forecasts
        """
        # Read the factor-based model CSV
        with open(factor_model_path, 'r') as file:
            content = file.read()
        
        # Split the content by section markers
        sections = content.split('====================')
        
        # Find the forecast results section
        forecast_section = None
        for section in sections:
            if 'FORECAST RESULTS' in section:
                forecast_section = section
                break
        
        if forecast_section is None:
            raise ValueError("Forecast results section not found in the CSV file")
        
        # Parse the forecast results section
        lines = forecast_section.strip().split('\n')
        
        # Skip the header lines
        data_lines = []
        for line in lines:
            if 'Month,2024 Queries,Conservative,Moderate,Ambitious' in line:
                continue
            if line.strip() and ',' in line:
                data_lines.append(line)
        
        # Create a DataFrame
        data = []
        for line in data_lines:
            parts = line.split(',')
            if len(parts) >= 5 and parts[1].strip() and parts[2].strip() and parts[3].strip() and parts[4].strip():
                month = parts[0].strip()
                queries_2024 = float(parts[1].strip())
                conservative = float(parts[2].strip())
                moderate = float(parts[3].strip())
                ambitious = float(parts[4].strip())
                data.append({
                    'Month': month,
                    '2024_Queries': queries_2024,
                    'Conservative': conservative,
                    'Moderate': moderate,
                    'Ambitious': ambitious
                })
        
        factor_forecast = pd.DataFrame(data)
        
        # Create a date column for 2025
        factor_forecast['Date'] = pd.to_datetime(
            '2025-' + 
            factor_forecast['Month'].apply(lambda x: {
                'January': '01', 'February': '02', 'March': '03', 'April': '04',
                'May': '05', 'June': '06', 'July': '07', 'August': '08',
                'September': '09', 'October': '10', 'November': '11', 'December': '12'
            }[x]) + '-01'
        )
        
        # Set the date as index
        factor_forecast = factor_forecast.set_index('Date')
        
        # Combine with statistical forecasts
        comparison = pd.DataFrame(index=factor_forecast.index)
        comparison['Factor_Conservative'] = factor_forecast['Conservative']
        comparison['Factor_Moderate'] = factor_forecast['Moderate']
        comparison['Factor_Ambitious'] = factor_forecast['Ambitious']
        
        # Add ARIMA forecast if available
        if hasattr(self, 'arima_forecast'):
            comparison['ARIMA_Forecast'] = self.arima_forecast['ARIMA_Forecast']
            comparison['ARIMA_Lower_CI'] = self.arima_forecast['Lower_CI']
            comparison['ARIMA_Upper_CI'] = self.arima_forecast['Upper_CI']
        
        # Add Prophet forecast if available
        if hasattr(self, 'prophet_forecast'):
            comparison['Prophet_Forecast'] = self.prophet_forecast['Prophet_Forecast']
            comparison['Prophet_Lower_CI'] = self.prophet_forecast['Lower_CI']
            comparison['Prophet_Upper_CI'] = self.prophet_forecast['Upper_CI']
        
        # Add Bayesian forecast if available
        if hasattr(self, 'bayesian_forecast'):
            comparison['Bayesian_Forecast'] = self.bayesian_forecast['Bayesian_Forecast']
            comparison['Bayesian_Lower_CI'] = self.bayesian_forecast['Lower_CI']
            comparison['Bayesian_Upper_CI'] = self.bayesian_forecast['Upper_CI']
        
        self.comparison = comparison
        return comparison
    
    def plot_outliers(self):
        """Plot the time series with outliers highlighted."""
        if not hasattr(self, 'outliers'):
            self.detect_outliers()
        
        plt.figure(figsize=(12, 6))
        plt.plot(self.time_series.index, self.time_series.values, 'b-', label='Original Data')
        plt.scatter(self.outliers.index, self.outliers['Indexed_Queries'], color='red', label='Outliers')
        
        if hasattr(self, 'adjusted_series'):
            plt.plot(self.adjusted_series.index, self.adjusted_series.values, 'g--', label='Adjusted Data')
        
        plt.title('Time Series with Outliers')
        plt.xlabel('Date')
        plt.ylabel('Indexed Queries')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('uk_outliers_detection.png')
        plt.close()
    
    def plot_forecasts(self):
        """Plot the forecasts from different models."""
        if not hasattr(self, 'comparison'):
            raise ValueError("No comparison data available. Run compare_with_factor_model first.")
        
        plt.figure(figsize=(12, 6))
        
        # Plot historical data
        plt.plot(self.time_series.index, self.time_series.values, 'b-', label='Historical Data')
        
        # Plot factor-based forecasts
        plt.plot(self.comparison.index, self.comparison['Factor_Conservative'], 'g--', label='Factor Conservative')
        plt.plot(self.comparison.index, self.comparison['Factor_Moderate'], 'g-', label='Factor Moderate')
        plt.plot(self.comparison.index, self.comparison['Factor_Ambitious'], 'g:', label='Factor Ambitious')
        
        # Plot ARIMA forecast if available
        if 'ARIMA_Forecast' in self.comparison.columns:
            plt.plot(self.comparison.index, self.comparison['ARIMA_Forecast'], 'r-', label='ARIMA Forecast')
            plt.fill_between(
                self.comparison.index,
                self.comparison['ARIMA_Lower_CI'],
                self.comparison['ARIMA_Upper_CI'],
                color='r', alpha=0.1, label='ARIMA 95% CI'
            )
        
        # Plot Prophet forecast if available
        if 'Prophet_Forecast' in self.comparison.columns:
            plt.plot(self.comparison.index, self.comparison['Prophet_Forecast'], 'm-', label='Prophet Forecast')
            plt.fill_between(
                self.comparison.index,
                self.comparison['Prophet_Lower_CI'],
                self.comparison['Prophet_Upper_CI'],
                color='m', alpha=0.1, label='Prophet 95% CI'
            )
        
        # Plot Bayesian forecast if available
        if 'Bayesian_Forecast' in self.comparison.columns:
            plt.plot(self.comparison.index, self.comparison['Bayesian_Forecast'], 'c-', label='Bayesian Forecast')
            plt.fill_between(
                self.comparison.index,
                self.comparison['Bayesian_Lower_CI'],
                self.comparison['Bayesian_Upper_CI'],
                color='c', alpha=0.1, label='Bayesian 95% CI'
            )
        
        plt.title('UK Travel Queries Forecast Comparison')
        plt.xlabel('Date')
        plt.ylabel('Indexed Queries')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        # Save the plot
        plt.savefig('uk_forecast_comparison.png')
        plt.close()
    
    def save_results(self):
        """Save the results to CSV files."""
        # Save the comparison data
        if hasattr(self, 'comparison'):
            self.comparison.to_csv('uk_forecast_comparison.csv')
        
        # Save the outliers data
        if hasattr(self, 'outliers'):
            outliers_df = self.historical_data.copy()
            outliers_df['Outlier'] = outliers_df.index.isin(self.outliers.index)
            if hasattr(self, 'adjusted_series'):
                outliers_df['Adjusted_Queries'] = self.adjusted_series
            outliers_df.to_csv('uk_outliers_detection.csv')
        
        # Save the ARIMA forecast
        if hasattr(self, 'arima_forecast'):
            self.arima_forecast.to_csv('uk_arima_forecast.csv')
        
        # Save the Prophet forecast
        if hasattr(self, 'prophet_forecast'):
            self.prophet_forecast.to_csv('uk_prophet_forecast.csv')
        
        # Save the Bayesian forecast
        if hasattr(self, 'bayesian_forecast'):
            self.bayesian_forecast.to_csv('uk_bayesian_forecast.csv')

def main():
    """Main function to run the enhanced forecast model."""
    # Define paths
    aligned_model_path = 'Travel_Queries_Forecast_UK_Aligned.csv'
    
    # Create the enhanced forecast model
    model = EnhancedForecastModel(aligned_model_path)
    
    # Detect and adjust outliers
    print("Detecting and adjusting outliers...")
    model.detect_outliers(method='zscore', threshold=3.0)
    model.adjust_outliers(method='median_window', window_size=3)
    model.plot_outliers()
    
    # Fit ARIMA model and generate forecast
    print("Fitting ARIMA model and generating forecast...")
    model.fit_arima_model(p=1, d=1, q=1)
    model.forecast_arima(steps=12)
    
    # Fit Prophet model and generate forecast if available
    if prophet_available:
        print("Fitting Prophet model and generating forecast...")
        model.fit_prophet_model()
        model.forecast_prophet(periods=12)
    
    # Generate Bayesian forecast if available
    if pymc3_available:
        print("Generating Bayesian forecast...")
        model.bayesian_forecast(periods=12, samples=1000)
    
    # Compare with factor-based model
    print("Comparing with factor-based model...")
    model.compare_with_factor_model(aligned_model_path)
    
    # Plot forecasts
    print("Plotting forecasts...")
    model.plot_forecasts()
    
    # Save results
    print("Saving results...")
    model.save_results()
    
    print("Done!")

if __name__ == "__main__":
    main()
