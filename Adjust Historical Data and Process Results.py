import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import json

def adjust_historical_data():
    """Process unadjusted historical data and create adjusted versions"""
    print("Starting historical data adjustment...")
    adjustment_start_time = datetime.now()
    
    # Input and output folder paths
    input_dir = 'SARM model testing/Unadjusted Historical Data'
    output_dir = 'SARM model testing/Adjusted Historical Data'
    os.makedirs(output_dir, exist_ok=True)
    
    processed_files = 0
    
    for file_name in filter(lambda f: f.endswith('.csv'), os.listdir(input_dir)):
        input_file_path, output_file_path = os.path.join(input_dir, file_name), os.path.join(output_dir, file_name)
        df = pd.read_csv(input_file_path)
        
        if {'timestamp', 'open', 'close_with_splits'}.issubset(df.columns):
            df['timestamp (for week ended)'] = pd.to_datetime(df['timestamp'])
            df['(%) change open-close this week'] = ((df['close_with_splits'] - df['open']) / df['open'] * 100)
            df['($) risk on open this week'] = -df['(%) change open-close this week'].shift(1)
            df['abs ($) risk on open this week'] = df['($) risk on open this week'].abs()
            df['profit or loss'] = df['(%) change open-close this week'] * df['($) risk on open this week'] / 100
            
            df = df.round(2).sort_values('timestamp (for week ended)').reset_index(drop=True)
            df.to_csv(output_file_path, index=False)
            processed_files += 1
        else:
            print(f"Skipping {file_name}: Required columns not found.")
    
    adjustment_end_time = datetime.now()
    print(f"Historical data adjustment complete! Files processed: {processed_files}")
    print(f"Adjustment runtime: {adjustment_end_time - adjustment_start_time}")
    
    return processed_files

def process_results():
    """Process the adjusted historical data and generate results"""
    print("\nStarting results processing...")
    processing_start_time = datetime.now()
    
    base_path = 'SARM model testing'
    
    # Process the adjusted historical data directly in SARM model testing folder
    folder_path = os.path.join(base_path, "Adjusted Historical Data")
    output_dir = os.path.join(base_path, "Results")
    os.makedirs(output_dir, exist_ok=True)
    
    yearly_risk_and_profit_path = os.path.join(output_dir, "Yearly Risk and Profit.csv")
    risk_adjusted_metrics_path = os.path.join(output_dir, "Risk-Adjusted Metrics.json")
    yearly_return_graph_path = os.path.join(output_dir, "Yearly Return Graph.png")
    
    total_absolute_sum = 0
    total_regular_sum = 0
    weekly_data = []
    profit_or_loss_data = []
    company_results = []
    
    combined_total_years = 0
    combined_positive_years = 0
    combined_negative_years = 0
    
    for file_name in filter(lambda f: f.endswith(".csv"), os.listdir(folder_path)):
        df = pd.read_csv(os.path.join(folder_path, file_name))
        df.replace([np.inf, -np.inf], 0, inplace=True)
        df = df[df["($) risk on open this week"] > 0]
        df["timestamp (for week ended)"] = pd.to_datetime(df["timestamp (for week ended)"], errors='coerce')
        df.dropna(subset=["timestamp (for week ended)"], inplace=True)
        
        total_absolute_sum += df["($) risk on open this week"].sum()
        total_regular_sum += df["profit or loss"].sum()
        
        weekly_data.append(
            df.groupby("timestamp (for week ended)")["($) risk on open this week"].sum().reset_index()
        )
        profit_or_loss_data.append(
            df.groupby("timestamp (for week ended)")["profit or loss"].sum().reset_index()
        )
        
        total_years = len(df)
        positive_years = (df["profit or loss"] > 0).sum()
        negative_years = (df["profit or loss"] <= 0).sum()
        
        combined_total_years += total_years
        combined_positive_years += positive_years
        combined_negative_years += negative_years
        
        percent_positive = (positive_years / total_years * 100) if total_years != 0 else 0
        percent_negative = (negative_years / total_years * 100) if total_years != 0 else 0
        
        company_results.append({
            "Filename": file_name,
            "Total Years": total_years,
            "Positive Years": positive_years,
            "Negative Years": negative_years,
            "Percent Positive Years": round(percent_positive, 2),
            "Percent Negative Years": round(percent_negative, 2)
        })
    
    weekly_combined = pd.concat(weekly_data).groupby("timestamp (for week ended)").sum().reset_index()
    profit_combined = pd.concat(profit_or_loss_data).groupby("timestamp (for week ended)").sum().reset_index()
    
    final_weekly = weekly_combined.merge(
        profit_combined, on="timestamp (for week ended)", how="left"
    )
    final_weekly["Year"] = final_weekly["timestamp (for week ended)"].dt.year
    
    yearly_summary = final_weekly.groupby("Year").agg({
        "($) risk on open this week": "max",
        "profit or loss": "sum"
    }).reset_index()
    
    # Rename columns
    yearly_summary.rename(columns={
        "($) risk on open this week": "Dollar Risk on Year Open",
        "profit or loss": "Dollar Profit or Loss"
    }, inplace=True)
    
    yearly_summary["Yearly Profit Percentage"] = (
        yearly_summary["Dollar Profit or Loss"] / yearly_summary["Dollar Risk on Year Open"] * 100
    ).round(2)
    
    # Sort by year and calculate cumulative CAGR
    yearly_summary = yearly_summary.sort_values("Year")
    yearly_summary["Cumulative CAGR"] = calculate_cumulative_return(yearly_summary["Yearly Profit Percentage"])
    
    # Ensure all columns are rounded to 2 decimal places
    yearly_summary = yearly_summary.round(2)
    yearly_summary.to_csv(yearly_risk_and_profit_path, index=False)
    
    # Create and save the plot
    plot_success = create_yearly_return_plot(yearly_summary, yearly_return_graph_path)
    if plot_success:
        print("Plot created successfully")
    else:
        print("Failed to create plot")
    
    # Calculate and save risk-adjusted metrics
    create_risk_adjusted_metrics(yearly_summary, risk_adjusted_metrics_path)
    
    processing_end_time = datetime.now()
    print(f"Results processing complete! Runtime: {processing_end_time - processing_start_time}")

def calculate_cumulative_return(returns):
    """Calculate cumulative return from a series of annual returns"""
    cumulative = 100  # Start with base 100
    cumulative_returns = []
    
    for ret in returns:
        # Add the percentage return to the running total
        cumulative = cumulative * (1 + ret/100)
        cumulative_returns.append(round(cumulative - 100, 2))
    
    return cumulative_returns

def create_risk_adjusted_metrics(yearly_data, output_path):
    """Calculate and save risk-adjusted metrics for SARM model and S&P 500"""
    # S&P 500 data
    sp500_data = {
        2000: -9.10, 2001: -11.89, 2002: -22.10, 2003: 28.68, 2004: 10.88,
        2005: 4.91, 2006: 15.79, 2007: 5.49, 2008: -37.00, 2009: 26.46,
        2010: 15.06, 2011: 2.11, 2012: 16.00, 2013: 32.39, 2014: 13.69,
        2015: 1.38, 2016: 11.96, 2017: 21.83, 2018: -4.38, 2019: 31.49,
        2020: 18.40, 2021: 28.71, 2022: -18.11, 2023: 26.29, 2024: 25.02
    }
    
    # Get SARM model returns from yearly data
    strategy_returns = yearly_data['Yearly Profit Percentage'].tolist()
    
    # Calculate the true average annual return for SARM model (total profit / total risk)
    total_dollar_profit = yearly_data['Dollar Profit or Loss'].sum()
    total_dollar_risk = yearly_data['Dollar Risk on Year Open'].sum()
    strategy_avg_annual_return = (total_dollar_profit / total_dollar_risk * 100) if total_dollar_risk != 0 else 0
    
    # Get S&P 500 returns for matching years
    years = yearly_data['Year'].tolist()
    sp500_returns = [sp500_data.get(year, 0) for year in years]
    
    # Calculate metrics for both
    strategy_metrics = calculate_metrics(strategy_returns, override_avg_return=strategy_avg_annual_return)
    sp500_metrics = calculate_metrics(sp500_returns)
    
    # Calculate differences
    differences = {
        "average_annual_return": round(strategy_metrics["average_annual_return"] - sp500_metrics["average_annual_return"], 2),
        "sharpe_ratio": round(strategy_metrics["sharpe_ratio"] - sp500_metrics["sharpe_ratio"], 2),
        "sortino_ratio": round(strategy_metrics["sortino_ratio"] - sp500_metrics["sortino_ratio"], 2),
        "maximum_drawdown": round(strategy_metrics["maximum_drawdown"] - sp500_metrics["maximum_drawdown"], 2)
    }
    
    # Create final output
    output = {
        "sarm_model": {
            "average_annual_return": strategy_metrics["average_annual_return"],
            "sharpe_ratio": strategy_metrics["sharpe_ratio"],
            "sortino_ratio": strategy_metrics["sortino_ratio"],
            "maximum_drawdown": strategy_metrics["maximum_drawdown"]
        },
        "sp500": {
            "average_annual_return": sp500_metrics["average_annual_return"],
            "sharpe_ratio": sp500_metrics["sharpe_ratio"],
            "sortino_ratio": sp500_metrics["sortino_ratio"],
            "maximum_drawdown": sp500_metrics["maximum_drawdown"]
        },
        "differences": differences
    }
    
    # Save to JSON file
    with open(output_path, 'w') as f:
        json.dump(output, f, indent=2)
    
    print(f"Risk-adjusted metrics saved to {output_path}")

def calculate_metrics(returns, override_avg_return=None):
    """Calculate risk metrics for a given set of returns"""
    # returns_array = np.array(returns)  # Not used
    
    # Average annual return
    avg_return = override_avg_return if override_avg_return is not None else np.mean(returns)
    
    # Standard deviation (volatility)
    std_dev = np.std(returns, ddof=1)
    
    # Sharpe ratio (assuming 2% risk-free rate)
    risk_free_rate = 2.0
    sharpe_ratio = (avg_return - risk_free_rate) / std_dev if std_dev > 0 else 0
    
    # Sortino ratio (using downside deviation)
    downside_returns = [r for r in returns if r < 0]
    downside_std = np.std(downside_returns, ddof=1) if len(downside_returns) > 1 else 0
    sortino_ratio = (avg_return - risk_free_rate) / downside_std if downside_std > 0 else 0
    
    # Maximum drawdown
    max_drawdown = min(returns) if returns else 0
    
    return {
        "average_annual_return": round(avg_return, 2),
        "sharpe_ratio": round(sharpe_ratio, 2),
        "sortino_ratio": round(sortino_ratio, 2),
        "maximum_drawdown": round(max_drawdown, 2),
        "volatility": round(std_dev, 2),
        "downside_volatility": round(downside_std, 2)
    }

def create_yearly_return_plot(data, output_path):
    """Create and save a bar plot of yearly returns with S&P 500 comparison"""
    try:
        plt.figure(figsize=(12, 8))
        
        # S&P 500 data
        sp500_data = {
            2000: -9.10, 2001: -11.89, 2002: -22.10, 2003: 28.68, 2004: 10.88,
            2005: 4.91, 2006: 15.79, 2007: 5.49, 2008: -37.00, 2009: 26.46,
            2010: 15.06, 2011: 2.11, 2012: 16.00, 2013: 32.39, 2014: 13.69,
            2015: 1.38, 2016: 11.96, 2017: 21.83, 2018: -4.38, 2019: 31.49,
            2020: 18.40, 2021: 28.71, 2022: -18.11, 2023: 26.29, 2024: 25.02
        }
        
        # Filter S&P 500 data to match available years in strategy data
        years = data['Year'].tolist()
        sp500_returns = [sp500_data.get(year, 0) for year in years]
        
        # Create bar plot for SARM model
        bars = plt.bar(data['Year'], data['Yearly Profit Percentage'], color='blue', alpha=0.7, label='SARM Model')
        
        # Add S&P 500 line
        plt.plot(years, sp500_returns, color='red', marker='o', linewidth=2, markersize=6, label='S&P 500')
        
        # Add value labels on top of each bar
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width()/2., height,
                    f'{height:.1f}%',
                    ha='center', va='bottom', fontsize=8)
        
        plt.xlabel('Year')
        plt.ylabel('Percent (%)')
        plt.title('Yearly Return % - SARM Model vs S&P 500')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(output_path)
        plt.close()
        return True
    except Exception as e:
        print(f"Error creating plot: {e}")
        return False

def main():
    """Main function that runs both adjustment and processing"""
    overall_start_time = datetime.now()
    
    print("=" * 60)
    print("ADJUST HISTORICAL DATA AND PROCESS RESULTS")
    print("=" * 60)
    
    # Step 1: Adjust historical data
    adjust_historical_data()
    
    # Step 2: Process results
    process_results()
    
    overall_end_time = datetime.now()
    print("\n" + "=" * 60)
    print(f"COMPLETE! Total runtime: {overall_end_time - overall_start_time}")
    print("=" * 60)

if __name__ == "__main__":
    main()