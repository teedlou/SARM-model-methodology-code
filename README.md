# Buying Pain for Long-Term Gain
*A 25-Year Analysis of Contrarian Investment Strategy Performance*

## What This Project Is About

I've always been intrigued by the contrarian investment philosophy— the idea that the best time to buy is when everyone else is selling. There's something almost quixotic about betting against market sentiment, but the underlying hypothesis is compelling: systematic market inefficiencies create exploitable opportunities for disciplined investors.

This repository documents my attempt to rigorously test that hypothesis. Over 25 years (2000-2024), I tracked what would happen if I bought individual losing stocks at the start of the year and held each of them for one calendar year. The results were more definitive than I expected.

## The Core Hypothesis

The strategy is elegantly simple: buy when others are selling. But execution requires something more ephemeral—the psychological fortitude to act antithetically to prevailing market sentiment. Most investors understand this concept intellectually, yet few can execute it consistently when their portfolio is hemorrhaging value and financial media is proclaiming economic apocalypse.

I wanted to know whether contrarian investing works not just in theory, but in practice. With real market crashes. With real human emotions. With the full panoply of market volatility that can derail even the most carefully constructed strategies.

## Why This Backtest is Analytically Accurate
Most investment strategies exhibit a pernicious gap between theoretical performance and practical implementation. They work brilliantly in backtests but falter when confronted with the messy reality of actual market conditions. This framework tests whether contrarian investing suffers from the same affliction, or whether it represents robust approach to wealth creation.

The methodology eliminates survivorship bias— a critical flaw that invalidates most historical analyses. Each trade decision uses only companies that were actually in the S&P 500 at that specific time. No retroactive adjustments, no convenient hindsight modifications.

## Data Sources and Methodology

### Historical Accuracy
The analysis relies on historically accurate S&P 500 constituent data spanning 25 years. This temporal scope captures multiple complete market cycles, ensuring the findings aren't an artifact of any particular market regime.

Special thanks to Farrell Aultman for providing the [S&P 500 Historical Data Repository](https://github.com/fja05680/sp500.git) under the MIT lisence. Without this meticulous historical record containing precise year-by-year index composition, the entire analysis would be compromised by survivorship bias.

### The Timeline
**2000-2024**: A quarter-century encompassing some of the most turbulent periods in modern financial history:
- The dot-com bubble collapse
- The 2008 financial crisis 
- The COVID-19 market disruption
- Various geopolitical and economic shocks

If contrarian investing was going to prove its mettle, it had to work through all of this.

## Key Findings

The numbers tell a remarkably consistent story across multiple market regimes.

### Performance Metrics
- **Average annual return**: 26.93%

To contextualize these results: the S&P 500 averaged approximately 10% annually over the same period. The contrarian strategy didn't just outperform—it generated nearly triple the returns of passive index investing.

### Individual Company Analysis
The granular data reveals heterogeneous outcomes across different companies and sectors. Some positions were unequivocal successes, others proved disappointing. But the aggregate pattern is unmistakable: systematic contrarian positioning generated consistent outperformance over extended periods.

### Visual Evidence
The yearly return graph provides perhaps the most compelling evidence. Blue bars represent the strategy's annual returns, while the red line tracks S&P 500 performance. The divergence is striking and persistent.

## Implementation Framework

### The Process
The analytical framework follows a systematic approach:
1. **Data Collection**: Historical price data for all S&P 500 constituents
2. **Signal Generation**: Quantitative identification of contrarian entry points
3. **Risk Management**: Disciplined position sizing based on volatility metrics
4. **Performance Tracking**: Comprehensive monitoring across multiple timeframes
5. **Attribution Analysis**: Understanding what worked and what didn't

### The Reality
The strategy is conceptually straightforward but psychologically demanding. Buying during market crashes feels viscerally wrong. Your portfolio will look terrible for months, sometimes years. Friends will question your sanity. The financial press will mock your contrarian positioning.

Yet if you can maintain conviction during these periods of maximum discomfort— if you can genuinely buy pain for long-term gain— the historical evidence suggests substantial rewards.

## Repository Structure

```
Strategy Testing/
├── Unadjusted Historical Data/     # Raw historical price data
├── Adjusted Historical Data/       # Processed data with risk calculations
├── Results/                        # Analysis outputs and visualizations
│   ├── Yearly Risk and Profit.csv
│   ├── Adjusted Summary.csv
│   ├── Individual Company Profit Odds.csv
│   └── Yearly Return Graph.png
└── Analytical Scripts
```

### Primary Script
`Adjust Historical Data and Process Results.py` represents the analytical engine of this framework. It transforms raw historical data into actionable insights through systematic quantitative analysis. Running this script generates all the performance metrics and visualizations needed to understand the strategy's efficacy.

## Broader Implications

### Market Efficiency Questions
The persistent outperformance documented here raises fundamental questions about market efficiency. If markets were truly efficient, such systematic outperformance shouldn't be possible. Yet the evidence suggests that behavioral biases create persistent inefficiencies that disciplined investors can exploit.

### Behavioral Considerations
The psychological dimension of contrarian investing cannot be understated. The strategy requires acting against every natural human instinct during periods of market stress. This represents perhaps the greatest barrier to successful implementation—not understanding the strategy, but having the temperament to execute it.

### Temporal Persistence
The consistency of results across 25 years and multiple market regimes suggests that the underlying behavioral phenomena aren't ephemeral anomalies but persistent features of human psychology in financial markets. For each file, the only constituient rows  are when the individual stock was a component in Standard and Poor's 500 Index.

## Personal Reflection

I didn't undertake this analysis to prove that contrarian investing works. I built this framework to discover whether it works. That distinction matters. I approached the investigation with genuine intellectual curiosity, allowing the data to tell its own story rather than forcing it to conform to preconceived notions.

The story the data tells is compelling. Across 25 years, through multiple market cycles and crises, systematic contrarian positioning generated meaningful outperformance. Not through luck, not through prescient market timing, but through the disciplined execution of a simple yet psychologically demanding strategy.

The framework provides both the methodology and the evidence. Whether you use it for your own investment decisions or simply to satisfy intellectual curiosity about market dynamics, the analysis stands on its own merits.

## The Ultimate Question

The data proves that contrarian investing can work. The question that remains is more personal and philosophical: do you have the psychological fortitude to buy pain for long-term gain? The market rewards those who can, but as this analysis makes clear, few possess the requisite temperament.

The opportunity exists. The evidence is compelling. The only remaining variable is human nature.

-Louie Teed
---

*This analysis maintains methodological rigor through exclusive use of historically accurate S&P 500 constituent data, eliminating survivorship bias and ensuring temporal integrity of all findings. The investigation represents an unbiased examination of contrarian investment efficacy across multiple market regimes.*