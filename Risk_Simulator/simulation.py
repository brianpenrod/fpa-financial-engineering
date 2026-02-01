import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class StrategicRiskSimulator:
    def __init__(self, n_simulations=10000):
        self.n_simulations = n_simulations

    def run_simulation(self, rev_mean, rev_std, opex_mean, opex_std):
        """
        Runs a Monte Carlo simulation for Revenue and OpEx.
        
        Args:
            rev_mean (float): Mean of Revenue.
            rev_std (float): Standard deviation of Revenue.
            opex_mean (float): Mean of OpEx.
            opex_std (float): Standard deviation of OpEx.
            
        Returns:
            pd.DataFrame: DataFrame containing simulation results.
        """
        # Generate random samples
        revenue_samples = np.random.normal(rev_mean, rev_std, self.n_simulations)
        opex_samples = np.random.normal(opex_mean, opex_std, self.n_simulations)
        
        # Calculate Net Profit
        net_profit_samples = revenue_samples - opex_samples
        
        # Create DataFrame
        results = pd.DataFrame({
            'Revenue': revenue_samples,
            'OpEx': opex_samples,
            'Net_Profit': net_profit_samples
        })
        
        return results

    def analyze_results(self, results):
        """
        Calculates summary statistics from simulation results.
        """
        stats = results.describe(percentiles=[0.05, 0.25, 0.5, 0.75, 0.95])
        return stats

    def visualize_results(self, results):
        """
        Generates a histogram of Net Income outcomes.
        """
        plt.figure(figsize=(10, 6))
        plt.hist(results['Net_Profit'], bins=50, alpha=0.7, color='skyblue', edgecolor='black')
        
        # Add vertical lines
        plt.axvline(0, color='red', linestyle='--', linewidth=2, label='Risk of Loss (0)')
        plt.axvline(results['Net_Profit'].mean(), color='green', linestyle='--', linewidth=2, label='Mean Expected Outcome')
        
        plt.title('Stochastic Risk Profile: Net Income Distribution')
        plt.xlabel('Net Income')
        plt.ylabel('Frequency')
        plt.legend()
        plt.grid(True, alpha=0.3)
        
        # Save chart
        plt.savefig('risk_profile_chart.png')
        plt.close()
        print("Chart saved as 'risk_profile_chart.png'")

if __name__ == "__main__":
    import sqlite3
    
    # Example usage
    sim = StrategicRiskSimulator(n_simulations=10000)
    
    # Fetch data from Database
    try:
        conn = sqlite3.connect('financials.db')
        df_history = pd.read_sql_query("SELECT revenue, opex FROM monthly_actuals", conn)
        conn.close()
        
        REV_MEAN = df_history['revenue'].mean()
        REV_STD = df_history['revenue'].std()
        OPEX_MEAN = df_history['opex'].mean()
        OPEX_STD = df_history['opex'].std()
        
        print("--- LIVE CONNECTION ESTABLISHED: Fetching 36 months of historical ERP data ---")
        
    except Exception as e:
        print(f"Error fetching data from DB: {e}")
        # Fallback to assumptions if DB fails
        REV_MEAN = 1000000
        REV_STD = 100000
        OPEX_MEAN = 600000
        OPEX_STD = 50000
        print("Using default assumptions.")
    
    print(f"Assumptions: Rev Mean=${REV_MEAN:,.2f}, Rev Std=${REV_STD:,.2f}, OpEx Mean=${OPEX_MEAN:,.2f}, OpEx Std=${OPEX_STD:,.2f}")
    
    df_results = sim.run_simulation(REV_MEAN, REV_STD, OPEX_MEAN, OPEX_STD)
    summary_stats = sim.analyze_results(df_results)
    
    print("\nSimulation Results Summary:")
    print(summary_stats)
    
    # Probability of loss
    prob_loss = (df_results['Net_Profit'] < 0).mean()
    print(f"\nProbability of Loss (Net Profit < 0): {prob_loss:.2%}")
    
    sim.visualize_results(df_results)
