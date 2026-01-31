# 📊 Quantitative Strategy Backtesting

> Quantitative analysis project comparing different investment strategies on a universe of U.S. equities (2015-2026)

## 🎯 Project Objective

This project compares three investment strategies using real market data:
- **Buy & Hold** on the S&P 500 (baseline)
- **Equal-Weighted**: monthly equal-weight allocation
- **Momentum 12-1**: selection of top 5 stocks based on momentum

The complete analysis automatically generates an interactive HTML report with visualizations and performance statistics.

## 📁 Project Structure

```
backtest-strategies/
│
├── backtest_step_by_step.ipynb          # Detailed Jupyter Notebook (exploration)
├── backtest_with_html_output_fr.py      # Python script (French report)
├── backtest_with_html_output_eng.py     # Python script (English report)
├── backtest_report.html                 # Generated report (FR)
├── backtest_report_en.html              # Generated report (EN)
└── README.md                            # This file
```

## 🚀 Installation & Usage

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### 1. Clone the repository

```bash
git clone https://github.com/your-username/backtest-strategies.git
cd backtest-strategies
```

### 2. Install dependencies

```bash
pip install yfinance pandas numpy matplotlib
```

### 3. Run the backtest

**Option A: Jupyter Notebook (detailed exploration)**
```bash
jupyter notebook backtest_step_by_step.ipynb
```
→ Ideal for understanding each step of the process

**Option B: Python Script (automatic report)**
```bash
# French version
python backtest_with_html_output_fr.py

# English version
python backtest_with_html_output_eng.py
```
→ Directly generates the HTML report

### 4. View results

Open `backtest_report_en.html` in your browser to see:
- Cumulative performance curves
- Drawdown analysis
- Returns distribution
- Comparative metrics table (CAGR, Sharpe, volatility, max DD)

## 📊 Methodology

### Investment Universe
19 U.S. large-cap stocks:
```
AAPL, MSFT, AMZN, GOOGL, META, NVDA, BRK-B, JPM, JNJ, V, 
PG, UNH, MA, HD, XOM, BAC, KO, DIS, PEP
```

### Tested Strategies

**1. Buy & Hold Benchmark (S&P 500)**
- Passive reference strategy
- Benchmark: `^GSPC`

**2. Equal-Weighted Portfolio**
- Monthly rebalancing
- Equal weight for each stock (1/N)
- Avoids mega-cap concentration

**3. Momentum 12-1 (Top 5)**
- Signal: 12-month return, skip 1 month
- Selection: Top 5 stocks each month
- Trend-following quantitative strategy

### Calculated Metrics

| Metric | Description |
|--------|-------------|
| **CAGR** | Compound Annual Growth Rate |
| **Volatility** | Annualized standard deviation of returns |
| **Sharpe Ratio** | Risk-adjusted return (RF = 4.25%) |
| **Max Drawdown** | Maximum loss from peak |

## 🛠️ Tech Stack

- **Data**: `yfinance` (Yahoo Finance API)
- **Calculations**: `pandas`, `numpy`
- **Visualization**: `matplotlib`
- **Output**: HTML/CSS (custom minimalist design)

## 📈 Expected Results

The HTML report presents:
- ✅ Visual performance comparison
- ✅ Risk/return analysis for each strategy
- ✅ Identification of outperformance periods
- ✅ Risk assessment (drawdown, volatility)

## 💡 Possible Improvements

- [ ] Add other factors (value, quality, low-vol)
- [ ] Implement rebalancing with transaction costs
- [ ] Backtest on different periods (rolling windows)
- [ ] Add statistical tests (t-test, bootstrap)
- [ ] Integrate correlation analysis

## 📝 Important Notes

- **Data**: Dividend and split-adjusted prices
- **Frequency**: Monthly rebalancing (end of month)
- **Survivorship Bias**: Current universe may create bias (surviving stocks)
- **Disclaimer**: Academic project - past performance does not predict future results

## 🎓 Academic Context

Project completed as part of my quantitative finance studies.

**Skills demonstrated:**
- Design and implementation of rigorous backtests
- Financial data manipulation (time series)
- Risk-adjusted performance metrics calculation
- Automated analysis reporting
- Results documentation and presentation

---

⭐ If you found this project useful, feel free to star it!
