"""
PROJECT: INVESTMENT YIELD ROLLING FORECAST ENGINE
AUTHOR: Dr. Brian Penrod, DBA
DATE: 2026-01-28

OBJECTIVE:
    Generate a 12-month rolling forecast for investment portfolio income (NII).
    This engine models 'New Money Yield' sensitivity against historical 'Book Yield'
    to stress-test liquidity and income under varying interest rate regimes.

OUTPUT:
    - Console Summary of Financial Impact
    - Board-Ready Excel File ('Rolling_Forecast_Output.xlsx') with formatted schedules.
"""

import pandas as pd
import numpy as np
import datetime

# --- SECTION 1: CONFIGURATION (THE CONTROL PANEL) ---
# Strategic Value: We define assumptions here to allow for rapid Scenario Analysis.

# SCENARIO: Interest Rate Compression
# We assume market rates drop by 50 basis points (-0.50%).
SCENARIO_YIELD_SHOCK = -0.005  

# GROWTH: Portfolio Reinvestment & New Premiums
# We assume the asset base grows by 0.5% month-over-month.
MONTHLY_ASSET_GROWTH = 0.005   

# TIMING: Forecast Horizon
FORECAST_MONTHS = 12
START_DATE = datetime.date(2025, 1, 1)

def generate_historical_data():
    """
    Simulates 'Actuals' from the accounting system (e.g., Clearwater/Aladdin).
    In a production environment, this would be a SQL query.
    """
    dates = pd.date_range(start='2024-01-01', periods=12, freq='ME') # Month End
    
    # Simulate a $50M Portfolio with slight variance in Book Yield
    data = pd.DataFrame({
        'Date': dates,
        'Type': 'Actual',
        'Portfolio_Balance': [50_000_000 * (1.002**i) for i in range(12)],
        # Book Yield oscillates around 4.5%
        'Yield_Annualized': [0.045 + np.random.normal(0, 0.0005) for _ in range(12)] 
    })
    
    # Calculate Monthly NII (Net Investment Income)
    data['Net_Investment_Income'] = data['Portfolio_Balance'] * (data['Yield_Annualized'] / 12)
    
    return data

def run_forecast_engine(actuals_df):
    """
    Extends the historical data into the future using Scenario logic.
    """
    last_balance = actuals_df['Portfolio_Balance'].iloc[-1]
    baseline_yield = actuals_df['Yield_Annualized'].mean()
    
    # Create Future Dates
    future_dates = pd.date_range(start=START_DATE, periods=FORECAST_MONTHS, freq='ME')
    
    forecast_rows = []
    
    current_balance = last_balance
    
    # Apply 'New Money Yield' Logic: Baseline Yield + The Shock Scenario
    projected_yield = baseline_yield + SCENARIO_YIELD_SHOCK
    
    for date in future_dates:
        # 1. Grow the Asset Base
        current_balance = current_balance * (1 + MONTHLY_ASSET_GROWTH)
        
        # 2. Calculate Projected Income based on New Yield
        monthly_income = current_balance * (projected_yield / 12)
        
        forecast_rows.append({
            'Date': date,
            'Type': 'Forecast',
            'Portfolio_Balance': current_balance,
            'Yield_Annualized': projected_yield,
            'Net_Investment_Income': monthly_income
        })
        
    forecast_df = pd.DataFrame(forecast_rows)
    
    # Merge Actuals and Forecast
    full_model = pd.concat([actuals_df, forecast_df], ignore_index=True)
    return full_model

def export_to_excel(df, filename="Rolling_Forecast_Output.xlsx"):
    """
    Exports data to Excel with 'Board-Ready' formatting.
    Demonstrates proficiency in both Python and Executive Reporting.
    """
    writer = pd.ExcelWriter(filename, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Rolling_Forecast', index=False)
    
    workbook = writer.book
    worksheet = writer.sheets['Rolling_Forecast']
    
    # Define Formats
    fmt_currency = workbook.add_format({'num_format': '$#,##0.00'})
    fmt_percent = workbook.add_format({'num_format': '0.00%'})
    fmt_header = workbook.add_format({'bold': True, 'bg_color': '#D3D3D3', 'border': 1})
    fmt_date = workbook.add_format({'num_format': 'mmm-yyyy'})
    
    # Apply Formats
    worksheet.set_column('A:A', 15, fmt_date)      # Date Column
    worksheet.set_column('B:B', 12)                # Type Column
    worksheet.set_column('C:C', 20, fmt_currency)  # Balance
    worksheet.set_column('D:D', 15, fmt_percent)   # Yield
    worksheet.set_column('E:E', 20, fmt_currency)  # Income
    
    # Conditional Formatting: Highlight the 'Forecast' section for clarity
    worksheet.conditional_format('A2:E25', {
        'type': 'formula',
        'criteria': '=$B2="Forecast"',
        'format': workbook.add_format({'bg_color': '#E6FFCC'}) # Light Green for Forecast
    })

    writer.close()
    print(f"[SUCCESS] Executive Report generated: {filename}")

# --- EXECUTION BLOCK ---
if __name__ == "__main__":
    print("--- INITIATING YIELD FORECAST ENGINE ---")
    print(f"SCENARIO: Yield Shock of {SCENARIO_YIELD_SHOCK*10000:.0f} basis points")
    
    # 1. Ingest Data
    hist_data = generate_historical_data()
    
    # 2. Run Logic
    final_model = run_forecast_engine(hist_data)
    
    # 3. Analyze Variance (Forecast Total vs. Run Rate)
    forecast_total = final_model[final_model['Type']=='Forecast']['Net_Investment_Income'].sum()
    print(f"TOTAL FORECASTED NII (Next 12 Mos): ${forecast_total:,.2f}")
    
    # 4. Deliver Output
    export_to_excel(final_model)