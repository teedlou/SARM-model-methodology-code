import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

def adjust_historical_data():
    """Process unadjusted historical data and create adjusted versions"""
    print("Starting historical data adjustment...")
    adjustment_start_time = datetime.now()
    
    # Input and output folder paths
    input_dir = 'Strategy Testing/Unadjusted Historical Data'
    output_dir = 'Strategy Testing/Adjusted Historical Data'
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
    
    base_path = 'Strategy Testing'
    
    # Process the adjusted historical data directly in Strategy Testing folder
    folder_path = os.path.join(base_path, "Adjusted Historical Data")
    output_dir = os.path.join(base_path, "Results")
    os.makedirs(output_dir, exist_ok=True)
    
    yearly_risk_and_profit_path = os.path.join(output_dir, "Yearly Risk and Profit.csv")
    adjusted_summary_path = os.path.join(output_dir, "Adjusted Summary.csv")
    individual_company_profit_odds_path = os.path.join(output_dir, "Individual Company Profit Odds.csv")
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
    
    avg_max_risk = yearly_summary["Dollar Risk on Year Open"].mean()
    avg_yearly_profit = yearly_summary["Dollar Profit or Loss"].mean()
    adjusted_summary = pd.DataFrame([{
        "Average Yearly Dollar Risk on Year Open": round(avg_max_risk, 2),
        "Average Yearly Profit": round(avg_yearly_profit, 2),
        "Percent Return": round((avg_yearly_profit / avg_max_risk * 100 if avg_max_risk != 0 else 0), 2)
    }])
    adjusted_summary.to_csv(adjusted_summary_path, index=False)
    
    combined_percent_positive = (combined_positive_years / combined_total_years * 100) if combined_total_years != 0 else 0
    combined_percent_negative = (combined_negative_years / combined_total_years * 100) if combined_total_years != 0 else 0
    
    combined_summary = {
        "Filename": "Combined Totals",
        "Total Years": combined_total_years,
        "Positive Years": combined_positive_years,
        "Negative Years": combined_negative_years,
        "Percent Positive Years": round(combined_percent_positive, 2),
        "Percent Negative Years": round(combined_percent_negative, 2)
    }
    
    company_results_df = pd.DataFrame(company_results)
    combined_summary_df = pd.concat([pd.DataFrame([combined_summary]), company_results_df], ignore_index=True)
    
    # Ensure all columns are rounded to 2 decimal places
    combined_summary_df = combined_summary_df.round(2)
    combined_summary_df.to_csv(individual_company_profit_odds_path, index=False)
    
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
        
        # Create bar plot for strategy
        bars = plt.bar(data['Year'], data['Yearly Profit Percentage'], color='blue', alpha=0.7, label='Strategy')
        
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
        plt.title('Yearly Return % - Strategy vs S&P 500')
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
    files_processed = adjust_historical_data()
    
    # Step 2: Process results
    process_results()
    
    overall_end_time = datetime.now()
    print("\n" + "=" * 60)
    print(f"COMPLETE! Total runtime: {overall_end_time - overall_start_time}")
    print("=" * 60)

if __name__ == "__main__":
    main()