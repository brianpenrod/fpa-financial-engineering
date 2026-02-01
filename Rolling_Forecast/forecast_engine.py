import yaml
import pandas as pd
import os

def load_config():
    # Load drivers.yaml
    config_path = os.path.join(os.path.dirname(__file__), 'drivers.yaml')
    with open(config_path, 'r') as file:
        return yaml.safe_load(file)

def run_forecast(months=12):
    config = load_config()
    
    rev_drivers = config['revenue_drivers']
    opex_drivers = config['opex_drivers']
    scenarios = config['scenarios']
    
    # Base values
    leads = rev_drivers['monthly_leads']
    conversion = rev_drivers['conversion_rate']
    acv = rev_drivers['avg_contract_value']
    churn = rev_drivers['churn_rate']
    
    marketing_spend = opex_drivers['marketing_spend_per_lead']
    headcount_cost = opex_drivers['headcount_cost_per_month']
    fixed_overhead = opex_drivers['fixed_overhead']
    
    all_results = []
    
    for scenario_name, scenario_params in scenarios.items():
        growth_factor = scenario_params['growth_factor']
        
        # Initialize revenue for waterfall (assuming starting from 0 or carry over, 
        # prompt implies calculating from scratch but using previous month mechanism)
        current_total_revenue = 0 
        
        for month in range(1, months + 1):
            # Calculations
            # New Revenue (Monthly impact of annual ACV)
            new_revenue = (leads * conversion * (acv / 12)) * growth_factor
            
            # Total Revenue (Waterfall)
            total_revenue = current_total_revenue * (1 - churn) + new_revenue
            current_total_revenue = total_revenue # Update for next month
            
            # Variable OpEx
            variable_opex = leads * marketing_spend
            
            # Fixed OpEx
            fixed_opex = headcount_cost + fixed_overhead
            
            # EBITDA
            ebitda = total_revenue - (variable_opex + fixed_opex)
            
            all_results.append({
                'Scenario': scenario_name,
                'Month': month,
                'New_Revenue': new_revenue,
                'Total_Revenue': total_revenue,
                'Variable_OpEx': variable_opex,
                'Fixed_OpEx': fixed_opex,
                'EBITDA': ebitda
            })
            
    # Create DataFrame
    df = pd.DataFrame(all_results)
    
    # Save to CSV
    output_path = os.path.join(os.path.dirname(__file__), 'rolling_forecast_results.csv')
    df.to_csv(output_path, index=False)
    print(f"Forecast saved to {output_path}")
    
    # Print Bear sample
    print("\n--- Bear Case (First 5 Months) ---")
    bear_case = df[df['Scenario'] == 'bear'].head()
    print(bear_case.to_string(index=False))

if __name__ == "__main__":
    run_forecast()
