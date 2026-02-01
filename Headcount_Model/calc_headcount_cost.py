import pandas as pd

def calculate_fully_loaded(row):
    base_salary = row['Base_Salary']
    role = row['Role']
    
    # Bonus
    if role in ['Analyst', 'Manager']:
        bonus_rate = 0.10
    else: # Director, VP
        bonus_rate = 0.20
    bonus = base_salary * bonus_rate
    
    # Employer FICA (6.2% capped at $11,439)
    fica_tax = min(base_salary * 0.062, 11439)
    
    # Employer Medicare (1.45% no cap)
    medicare_tax = base_salary * 0.0145
    
    # FUTA ($42 flat)
    futa_tax = 42
    
    # Benefits ($12,000 flat)
    benefits = 12000
    
    fully_loaded_cost = base_salary + bonus + fica_tax + medicare_tax + futa_tax + benefits
    return fully_loaded_cost

def main():
    # Load current roster
    try:
        df = pd.read_csv('current_roster.csv')
    except FileNotFoundError:
        print("Error: current_roster.csv not found.")
        return

    # Calculate Fully Loaded Cost
    df['Fully_Loaded_Cost'] = df.apply(calculate_fully_loaded, axis=1)
    
    # Summary Table
    total_base = df['Base_Salary'].sum()
    total_loaded = df['Fully_Loaded_Cost'].sum()
    burden_rate = total_loaded / total_base if total_base > 0 else 0
    
    print("\n--- Headcount Cost Summary ---")
    print(f"Total Base Salary:      ${total_base:,.2f}")
    print(f"Total Fully Loaded Cost: ${total_loaded:,.2f}")
    print(f"Burden Rate:            {burden_rate:.2f}x")
    
    # Save detailed result
    df.to_csv('roster_with_costs.csv', index=False)
    print("\nDetailed results saved to 'roster_with_costs.csv'")

if __name__ == "__main__":
    main()
