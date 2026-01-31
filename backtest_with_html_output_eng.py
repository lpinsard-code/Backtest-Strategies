import datetime
import time
import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_universe():
    tickers = [
        'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NVDA', 'BRK-B', 'JPM', 'JNJ', 'V',
        'PG', 'UNH', 'MA', 'HD', 'XOM', 'BAC', 'KO', 'DIS', 'PEP'
    ]
    benchmark_ticker = '^GSPC'
    start_date = '2015-01-01'
    end_date = datetime.datetime.now().strftime('%Y-%m-%d')
    return tickers, benchmark_ticker, start_date, end_date


def download_prices(tickers, benchmark_ticker, start_date, end_date):
    symbols = list(tickers) + [benchmark_ticker]
    prices_d = yf.download(symbols, start=start_date, end=end_date, auto_adjust=False, progress=False)['Adj Close']
    if isinstance(prices_d, pd.Series):
        prices_d = prices_d.to_frame()
    return prices_d


def resample_month_end(prices_d):
    try:
        return prices_d.resample('ME').last()
    except ValueError:
        return prices_d.resample('M').last()


def compute_returns(prices_m, tickers, benchmark_ticker):
    monthly_prices = prices_m[tickers]
    bench_prices = prices_m[[benchmark_ticker]]
    monthly_returns = monthly_prices.pct_change()
    bench_returns = bench_prices.pct_change()
    return monthly_prices, bench_prices, monthly_returns, bench_returns


def buy_and_hold_curve(returns):
    returns = returns.dropna()
    return (1 + returns).cumprod()


def equal_weight_returns(monthly_returns):
    return monthly_returns.mean(axis=1, skipna=True)


def benchmark_drawdown(curve_100):
    running_max = curve_100.cummax()
    return curve_100 / running_max - 1


def momentum_12_1_signal(monthly_prices):
    mom_12_1 = (monthly_prices.shift(1) / monthly_prices.shift(13)) - 1
    return mom_12_1.shift(1)


def top_n_weights(signal, top_n):
    ranks = signal.rank(axis=1, ascending=False, method='first')
    selected = ranks.le(top_n)
    weights = selected.astype(float)
    weights = weights.div(weights.sum(axis=1), axis=0)
    return weights


def portfolio_returns(weights, monthly_returns):
    port_returns = (weights * monthly_returns).sum(axis=1)
    return port_returns.to_frame(name='portfolio_returns').dropna()


def align_series(port_returns, bench_returns, ew_returns):
    common_idx = port_returns.index.intersection(bench_returns.dropna().index)
    port_returns_aligned = port_returns.loc[common_idx]
    bench_returns_aligned = bench_returns.loc[common_idx]
    ew_returns_aligned = ew_returns.loc[common_idx]
    return port_returns_aligned, bench_returns_aligned, ew_returns_aligned


def perf_stats(r, rf_annual=0.0):
    if isinstance(r, pd.DataFrame):
        r = r.iloc[:, 0]
    r = pd.Series(r).dropna()
    rf_monthly = rf_annual / 12
    n = len(r)
    cagr = (1 + r).prod() ** (12 / n) - 1
    vol = r.std() * np.sqrt(12)
    excess = r - rf_monthly
    denom = excess.std()
    sharpe = np.nan if denom == 0 else excess.mean() / denom * np.sqrt(12)
    curve = (1 + r).cumprod()
    dd = curve / curve.cummax() - 1
    max_dd = dd.min()
    return pd.Series({'CAGR': cagr, 'Volatility': vol, 'Sharpe': sharpe, 'MaxDD': max_dd, 'Months': n})


def format_stats(stats):
    stats_fmt = stats.copy()
    for row in ['CAGR', 'Volatility', 'MaxDD']:
        if row in stats_fmt.index:
            stats_fmt.loc[row] = stats_fmt.loc[row] * 100
    def fmt_value(x, row_name):
        if row_name in ['CAGR', 'Volatility', 'MaxDD']:
            return f'{x:,.2f}%'
        if row_name == 'Sharpe':
            return f'{x:,.2f}'
        if row_name == 'Months':
            try:
                return f'{int(round(float(x)))}'
            except Exception:
                return str(x)
        return str(x)
    out = pd.DataFrame(index=stats_fmt.index, columns=stats_fmt.columns)
    for r in stats_fmt.index:
        for c in stats_fmt.columns:
            v = stats_fmt.loc[r, c]
            out.loc[r, c] = fmt_value(v, r)
    return out


def plot_to_base64(fig):
    """Convert matplotlib figure to base64 string for HTML embedding"""
    buf = BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', facecolor='#0a0e1a')
    buf.seek(0)
    img_str = base64.b64encode(buf.read()).decode()
    buf.close()
    plt.close(fig)
    return img_str


def create_plot(series_list, title, ylabel):
    """Create a plot and return as base64 string"""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0e1a')
    ax.set_facecolor('#0f1419')
    
    colors = ['#00d4ff', '#ff3366', '#ffaa00']
    for idx, (s, label) in enumerate(series_list):
        ax.plot(s, label=label, linewidth=2.5, color=colors[idx % len(colors)])
    
    ax.set_title(title, color='#ffffff', fontsize=16, fontweight='600', pad=20)
    ax.set_ylabel(ylabel, color='#8b95a5', fontsize=12)
    ax.set_xlabel('Date', color='#8b95a5', fontsize=12)
    ax.legend(framealpha=0.9, facecolor='#1a1f2e', edgecolor='#2a3142', labelcolor='#ffffff')
    ax.grid(True, alpha=0.15, color='#2a3142')
    ax.tick_params(colors='#8b95a5')
    ax.spines['bottom'].set_color('#2a3142')
    ax.spines['top'].set_color('#2a3142')
    ax.spines['right'].set_color('#2a3142')
    ax.spines['left'].set_color('#2a3142')
    
    return plot_to_base64(fig)


def create_histogram(data, title):
    """Create a histogram and return as base64 string"""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='#0a0e1a')
    ax.set_facecolor('#0f1419')
    
    ax.hist(data, bins=30, color='#00d4ff', alpha=0.7, edgecolor='#00a8cc')
    ax.set_title(title, color='#ffffff', fontsize=16, fontweight='600', pad=20)
    ax.set_xlabel('Return', color='#8b95a5', fontsize=12)
    ax.set_ylabel('Frequency', color='#8b95a5', fontsize=12)
    ax.grid(True, alpha=0.15, color='#2a3142')
    ax.tick_params(colors='#8b95a5')
    ax.spines['bottom'].set_color('#2a3142')
    ax.spines['top'].set_color('#2a3142')
    ax.spines['right'].set_color('#2a3142')
    ax.spines['left'].set_color('#2a3142')
    
    return plot_to_base64(fig)


def generate_html_report(tickers, benchmark_ticker, start_date, end_date, 
                        bh_bench_img, ew_img, dd_img, hist_img, comparison_img,
                        stats_df, bench_dd_min):
    """Generate HTML report with all results - ENGLISH VERSION"""
    
    stats_html = stats_df.to_html(classes='stats-table', border=0)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Backtest Strategies Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Work+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --bg-primary: #0a0e1a;
            --bg-secondary: #0f1419;
            --bg-card: #1a1f2e;
            --border-color: #2a3142;
            --text-primary: #ffffff;
            --text-secondary: #8b95a5;
            --accent-blue: #00d4ff;
            --accent-pink: #ff3366;
            --accent-orange: #ffaa00;
        }}
        
        body {{
            font-family: 'Work Sans', sans-serif;
            background: linear-gradient(135deg, var(--bg-primary) 0%, #0d1118 100%);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            padding: 0;
            margin: 0;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 60px 40px;
        }}
        
        header {{
            text-align: center;
            margin-bottom: 80px;
            position: relative;
        }}
        
        h1 {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 20px;
            background: linear-gradient(135deg, var(--accent-blue) 0%, var(--accent-pink) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -2px;
        }}
        
        .subtitle {{
            font-size: 1.2rem;
            color: var(--text-secondary);
            font-weight: 300;
            margin-bottom: 10px;
        }}
        
        .meta {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
            color: var(--text-secondary);
            margin-top: 20px;
            padding: 15px;
            background: var(--bg-card);
            border-radius: 8px;
            display: inline-block;
            border: 1px solid var(--border-color);
        }}
        
        .section {{
            margin-bottom: 70px;
            animation: fadeInUp 0.6s ease-out;
            animation-fill-mode: both;
        }}
        
        .section:nth-child(1) {{ animation-delay: 0.1s; }}
        .section:nth-child(2) {{ animation-delay: 0.2s; }}
        .section:nth-child(3) {{ animation-delay: 0.3s; }}
        .section:nth-child(4) {{ animation-delay: 0.4s; }}
        .section:nth-child(5) {{ animation-delay: 0.5s; }}
        .section:nth-child(6) {{ animation-delay: 0.6s; }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        h2 {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.8rem;
            margin-bottom: 15px;
            color: var(--accent-blue);
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        
        h2::before {{
            content: '';
            width: 4px;
            height: 30px;
            background: linear-gradient(180deg, var(--accent-blue), var(--accent-pink));
            border-radius: 2px;
        }}
        
        .description {{
            color: var(--text-secondary);
            margin-bottom: 30px;
            font-size: 1rem;
            line-height: 1.8;
            max-width: 800px;
        }}
        
        .chart-container {{
            background: var(--bg-card);
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 25px;
            border: 1px solid var(--border-color);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }}
        
        .chart-container:hover {{
            transform: translateY(-5px);
            border-color: var(--accent-blue);
        }}
        
        .chart-container img {{
            width: 100%;
            height: auto;
            display: block;
            border-radius: 8px;
        }}
        
        .stats-table {{
            width: 100%;
            background: var(--bg-card);
            border-radius: 12px;
            overflow: hidden;
            border-collapse: collapse;
            border: 1px solid var(--border-color);
        }}
        
        .stats-table th {{
            background: linear-gradient(135deg, #1a2332 0%, #1e2738 100%);
            color: var(--accent-blue);
            font-family: 'JetBrains Mono', monospace;
            padding: 18px 24px;
            text-align: left;
            font-weight: 600;
            font-size: 0.95rem;
            border-bottom: 2px solid var(--accent-blue);
        }}
        
        .stats-table td {{
            padding: 18px 24px;
            border-bottom: 1px solid var(--border-color);
            color: var(--text-primary);
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.9rem;
        }}
        
        .stats-table tr:last-child td {{
            border-bottom: none;
        }}
        
        .stats-table tr:hover {{
            background: rgba(0, 212, 255, 0.05);
        }}
        
        .stats-table tbody tr:nth-child(even) {{
            background: rgba(255, 255, 255, 0.02);
        }}
        
        .highlight-box {{
            background: var(--bg-card);
            border-left: 4px solid var(--accent-pink);
            padding: 20px 25px;
            margin: 25px 0;
            border-radius: 8px;
            border: 1px solid var(--border-color);
        }}
        
        .highlight-box strong {{
            color: var(--accent-orange);
            font-family: 'JetBrains Mono', monospace;
        }}
        
        footer {{
            text-align: center;
            margin-top: 100px;
            padding: 40px;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
        }}
        
        .ticker-list {{
            font-family: 'JetBrains Mono', monospace;
            color: var(--accent-blue);
            background: var(--bg-secondary);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 0.85rem;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 40px 20px;
            }}
            
            h1 {{
                font-size: 2.5rem;
            }}
            
            h2 {{
                font-size: 1.4rem;
            }}
            
            .chart-container {{
                padding: 20px;
            }}
            
            .stats-table th,
            .stats-table td {{
                padding: 12px 16px;
                font-size: 0.85rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>Backtest Strategies Report</h1>
            <p class="subtitle">Comparative Analysis of Investment Strategies</p>
            <div class="meta">
                Period: {start_date} → {end_date}<br>
                Benchmark: <span class="ticker-list">{benchmark_ticker}</span><br>
                Universe: <span class="ticker-list">{', '.join(tickers[:5])}</span> + {len(tickers)-5} others
            </div>
        </header>

        <div class="section">
            <h2>Buy & Hold Strategy — Benchmark</h2>
            <p class="description">
                Performance of a simple buy-and-hold strategy on the S&P 500 index. 
                This strategy serves as a baseline to evaluate the performance of other approaches.
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{bh_bench_img}" alt="Buy and Hold Benchmark">
            </div>
        </div>

        <div class="section">
            <h2>Equal-Weighted Strategy</h2>
            <p class="description">
                An approach that allocates equal weight to each stock in the universe, 
                rebalanced monthly. This method avoids excessive concentration in large-cap stocks.
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{ew_img}" alt="Equal-Weighted Strategy">
            </div>
        </div>

        <div class="section">
            <h2>Benchmark Drawdown</h2>
            <p class="description">
                Drawdown measures the maximum decline from the highest peak. 
                It illustrates the potential loss risk and strategy volatility.
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{dd_img}" alt="Benchmark Drawdown">
            </div>
            <div class="highlight-box">
                <strong>Maximum Drawdown:</strong> {bench_dd_min:.2%}
            </div>
        </div>

        <div class="section">
            <h2>Returns Distribution</h2>
            <p class="description">
                Histogram of the benchmark's monthly returns. 
                This visualization allows observation of the statistical distribution and identification of return normality.
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{hist_img}" alt="Returns Histogram">
            </div>
        </div>

        <div class="section">
            <h2>Strategy Comparison</h2>
            <p class="description">
                Comparison between the Momentum (12-1) strategy, Equal-Weighted strategy, and Benchmark. 
                The Momentum strategy selects the 5 stocks with the best performance over 12 months (excluding the last month).
            </p>
            <div class="chart-container">
                <img src="data:image/png;base64,{comparison_img}" alt="Strategy Comparison">
            </div>
        </div>

        <div class="section">
            <h2>Performance Statistics</h2>
            <p class="description">
                Summary table of key metrics: annualized return (CAGR), volatility, 
                Sharpe ratio, and maximum drawdown. Risk-free rate: 4.25%.
            </p>
            <div class="chart-container">
                {stats_html}
            </div>
        </div>

        <footer>
            <p>Report generated on {datetime.datetime.now().strftime('%m/%d/%Y at %H:%M')}</p>
            <p style="margin-top: 10px; font-size: 0.8rem;">Past performance does not predict future results.</p>
        </footer>
    </div>
</body>
</html>"""
    
    return html_content


def main():
    print("🚀 Starting backtest...")
    
    tickers, benchmark_ticker, start_date, end_date = get_universe()
    print(f"📊 Downloading data for {len(tickers)} stocks...")

    prices_d = download_prices(tickers, benchmark_ticker, start_date, end_date)
    prices_m = resample_month_end(prices_d)
    monthly_prices, bench_prices, monthly_returns, bench_returns = compute_returns(prices_m, tickers, benchmark_ticker)

    print("📈 Generating charts...")
    
    # Chart 1: Buy and Hold Benchmark
    buy_and_hold_bench_curve = buy_and_hold_curve(bench_returns)
    bh_bench_100 = 100 * buy_and_hold_bench_curve
    bh_bench_img = create_plot([(bh_bench_100, 'Benchmark Buy & Hold')], 
                               'Buy and Hold Strategy on Benchmark', 'Cumulative Return')

    # Chart 2: Equal-Weighted
    ew_returns = equal_weight_returns(monthly_returns)
    ew_curve = buy_and_hold_curve(ew_returns)
    ew_100 = 100 * ew_curve
    ew_img = create_plot([(ew_100, 'Equal-Weighted')], 
                         'Equal-Weighted Strategy', 'Cumulative Return')

    # Chart 3: Drawdown
    bench_dd = benchmark_drawdown(bh_bench_100)
    dd_img = create_plot([(bench_dd, 'Benchmark Drawdown')], 
                         'Benchmark Drawdown', 'Drawdown')
    bench_dd_min_value = bench_dd.min()
    bench_dd_min = float(bench_dd_min_value.iloc[0]) if hasattr(bench_dd_min_value, 'iloc') else float(bench_dd_min_value)

    # Chart 4: Histogram
    hist_img = create_histogram(bench_returns.dropna().values.flatten(), 
                                'Benchmark Returns Histogram')

    # Momentum strategy
    print("🎯 Calculating Momentum strategy...")
    mom_signal = momentum_12_1_signal(monthly_prices)
    top_n = 5
    weights = top_n_weights(mom_signal, top_n)
    port_returns = portfolio_returns(weights, monthly_returns)

    port_returns_aligned, bench_returns_aligned, ew_returns_aligned = align_series(
        port_returns, bench_returns, ew_returns)

    port_curve = buy_and_hold_curve(port_returns_aligned)
    bench_curve = buy_and_hold_curve(bench_returns_aligned)
    ew_curve2 = buy_and_hold_curve(ew_returns_aligned)

    port_100 = 100 * port_curve
    bench_100 = 100 * bench_curve
    ew_100_2 = 100 * ew_curve2

    # Chart 5: Comparison
    comparison_img = create_plot(
        [(port_100, f'Momentum Strategy (Top {top_n})'),
         (bench_100, 'Benchmark (Buy & Hold)'),
         (ew_100_2, 'Equal-Weighted Strategy')],
        'Cumulative Returns Comparison',
        'Cumulative Return'
    )

    # Performance stats
    print("📊 Computing performance statistics...")
    stats = pd.concat(
        [
            perf_stats(port_returns_aligned, rf_annual=0.0425).rename('Momentum 12-1 TopN'),
            perf_stats(ew_returns_aligned, rf_annual=0.0425).rename('Equal-Weight'),
            perf_stats(bench_returns_aligned, rf_annual=0.0425).rename('Benchmark')
        ],
        axis=1
    )
    stats_formatted = format_stats(stats)

    # Generate HTML
    print("🎨 Generating HTML report...")
    html_content = generate_html_report(
        tickers, benchmark_ticker, start_date, end_date,
        bh_bench_img, ew_img, dd_img, hist_img, comparison_img,
        stats_formatted, bench_dd_min
    )

    # Save HTML
    output_file = 'backtest_report_en.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ Report successfully generated: {output_file}")
    print("\n📊 Performance statistics:")
    print(stats_formatted)


if __name__ == '__main__':
    main()
