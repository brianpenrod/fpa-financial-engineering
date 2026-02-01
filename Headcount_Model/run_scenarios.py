import pandas as pd
from datetime import datetime, timedelta

def run_scenarios():
    # Load roster with costs
    try:
        df = pd.read_csv('roster_with_costs.csv')
    except FileNotFoundError:
        print("Error: roster_with_costs.csv not found.")
        return

    # Base Case
    base_cost = df['Fully_Loaded_Cost'].sum()
    
    # --- Scenario A: RIF (Top 10% by Cost) ---
    # Sort by cost descending
    df_sorted = df.sort_values(by='Fully_Loaded_Cost', ascending=False)
    
    # Determine cutoff for top 10%
    num_employees = len(df)
    cut_count = int(num_employees * 0.10)
    
    # Remove top 10%
    df_rif = df_sorted.iloc[cut_count:]
    rif_cost = df_rif['Fully_Loaded_Cost'].sum()
    rif_savings = base_cost - rif_cost
    rif_savings_pct = (rif_savings / base_cost) * 100

    # --- Scenario B: Hiring Delay (50% cost reduction for < 6 months tenure) ---
    # Convert Start_Date to datetime
    df['Start_Date'] = pd.to_datetime(df['Start_Date'])
    
    cutoff_date = datetime.now() - timedelta(days=6*30) # Approx 6 months
    
    # Calculate delayed costs
    def apply_delay(row):
        cost = row['Fully_Loaded_Cost']
        if row['Start_Date'] > cutoff_date:
            return cost * 0.5
        return cost

    delay_cost = df.apply(apply_delay, axis=1).sum()
    delay_savings = base_cost - delay_cost
    delay_savings_pct = (delay_savings / base_cost) * 100
    
    # --- Compile Report ---
    report_data = [
        ['Base Case', base_cost, 0.0, 0.0],
        ['Scenario A: RIF (Top 10%)', rif_cost, rif_savings, rif_savings_pct],
        ['Scenario B: Hiring Delay (<6mo)', delay_cost, delay_savings, delay_savings_pct]
    ]
    
    df_report = pd.DataFrame(report_data, columns=['Scenario Name', 'Total Cost', 'Savings ($)', 'Savings (%)'])
    
    # Formatting for display
    print("\n--- Scenario Comparison Table ---")
    print(df_report.to_string(index=False, formatters={
        'Total Cost': '${:,.2f}'.format,
        'Savings ($)': '${:,.2f}'.format,
        'Savings (%)': '{:.1f}%'.format
    }))
    
    # Save Report
    df_report.to_csv('scenario_impact_report.csv', index=False)
    print("\nReport saved to 'scenario_impact_report.csv'")

if __name__ == "__main__":
    run_scenarios()
