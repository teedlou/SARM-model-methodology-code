# SARM model logic

## Overview

This repository contains the implementation code and methodology demonstration for my research paper:

"The SARM model: A Strategic Approach For Exploiting Temporary Performance Deviations of the Constituents of Standard & Poor's 500 Index"

Louie Teed, July 16, 2025

Contact - teedlouie@gmail.com

## Core Methodology

The SARM model uses a weighted allocation approach based on the magnitude of losses:


Wi = |Li|/Σ|Lj|


Where:
- **Wi** = The weight (portion) of total investment allocated to stock i
- **Li** = The percentage loss of stock i in the previous year (negative value)
- **|Li|** = The absolute value of the loss
- **Σ|Lj|** = The sum of absolute losses for all selected stocks

### Example
If three stocks had returns of -40%, -30%, and -20%:
- Total absolute losses: 40 + 30 + 20 = 90
- Stock 1 weight: 40/90 = 44.4%
- Stock 2 weight: 30/90 = 33.3%
- Stock 3 weight: 20/90 = 22.2%

## Data Processing Pipeline

### 1. Historical Data Adjustment (`adjust_historical_data()`)

The function processes raw S&P 500 weekly price data:

# Input: Unadjusted CSV files with columns: timestamp, open, close_with_splits
# Output: Adjusted CSV files with calculated risk and profit metrics

**Processing Steps:**
1. **Yearly Return Calculation**: `(close - open) / open * 100`
2. **Risk Calculation**: Uses previous year's performance inverted as risk indicator
3. **Profit/Loss Calculation**: `weekly_return * risk_from_previous_week / 100`
4. **Data Validation**: Ensures all required columns exist and handles edge cases

### 2. Results Processing (`process_results()`)

This function aggregates individual stock data to generate portfolio-level metrics:

**Key Operations:**

1. **Data Aggregation**:
   - Combines yearly data from all stocks
   - Groups by timestamp to calculate portfolio-wide metrics
   - Filters out invalid data (infinity values, missing timestamps)

2. **Yearly Summary Generation**:
   - Calculates maximum dollar risk per year
   - Sums total profit/loss for the year
   - Computes yearly return percentage

3. **Risk-Adjusted Metrics Calculation**:
   - **Sharpe Ratio**: `(return - risk_free_rate) / volatility`
   - **Sortino Ratio**: `(return - risk_free_rate) / downside_volatility`
   - **Maximum Drawdown**: Largest peak-to-trough decline
   - **Average Annual Return**: total compounded return/24 year data set
4. **Visualization Creation**:
   - Generates bar chart comparing the SARM model returns to S&P 500 returns over the same period
   - Adds performance labels and trend lines

## File Structure Explained

SARM-model-logic/
│
├── Adjust Historical Data and Process Results.py
│   └── Main script containing all processing logic
│
├── SARM model testing/
│   ├── Unadjusted Historical Data/
│   │   └── Raw CSV files (one per S&P 500 company)
│   │       Format: timestamp, open, close_with_splits
│   │
│   ├── Adjusted Historical Data/
│   │   └── Processed CSV files with risk/profit calculations
│   │       Added columns: yearly_change_%, risk$, profit_loss
│   │
│   └── Results/
│       ├── Yearly Risk and Profit.csv
│       │   └── Annual summary: year, risk, profit, return%, CAGR
│       │
│       ├── Risk-Adjusted Metrics.json
│       │   └── Comparative metrics: SARM vs S&P 500
│       │
│       └── Yearly Return Graph.png
│           └── Visual comparison chart


### Yearly Risk Calculation Logic

The model uses a unique approach to risk calculation:
1. Each year's performance determines the risk for the NEXT year
2. Negative returns create positive risk allocations (contrarian approach)
3. Risk is proportional to the magnitude of the previous year's loss

### Portfolio Rebalancing

- **Frequency**: Annual (based on prior year's performance)
- **Selection Criteria**: Stocks with negative annual returns
- **Position Sizing**: Proportional to loss magnitude
- **Execution**: Beginning and end of each year


## Performance Metrics (2000-2024)

| Metric | SARM Model | S&P 500 | Difference |
|--------|------------|---------|------------|
| Average Annual Return | 26.93% | 9.36% | +17.57% |
| Sharpe Ratio | 0.89 | 0.40 | +0.49 |
| Sortino Ratio | 1.80 | 0.63 | +1.17 |
| Maximum Drawdown | -40.6% | -37.0% | -3.6% |

## Usage Instructions

1. **View pre-prepared data**:  unadjusted historical data CSV files are automatically placed in the `Unadjusted Historical Data` folder 

2. **Run Processing**:
   ```bash
   python "Adjust Historical Data and Process Results.py"
   ```

3. **Review Results**: Check the `Results` folder for:
   - Performance metrics
   - Yearly returns visualization
   - Risk-adjusted comparisons

## Technical Requirements

- Python 3.x
- pandas
- numpy
- matplotlib
- json (standard library)


## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.