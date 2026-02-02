# FP&A Financial Engineering Portfolio

## 1. Executive Summary
This repository houses the "heavy lift" logic engines used for complex financial modeling. Unlike standard Excel workbooks, these modules utilize Python (Pandas/NumPy) to handle high-dimensionality problems that break spreadsheets: stochastic risk simulation, roster-level headcount planning, and driver-based rolling forecasts.

**Philosophy:** Excel is for *presentation*; Python is for *calculation*.

---

## MODULE A: The Headcount & Comp War Room ("Project Bravo")
### Business Problem
Headcount (HC) typically comprises 60-70% of Operating Expenses. Managing it in Excel leads to:
* **Broken Formulas:** When rows are added/deleted for new hires.
* **Burden Rate Errors:** Failure to accurately calculate FICA tax caps (Social Security wage base limits) or variable benefit tiers.
* **Static Planning:** Inability to instantly answer, "What is the P&L impact if we delay all Engineering hires by 3 months?"

### The Solution
A distinct Python module that ingests a roster (current + TBH) and calculates **Fully Loaded Cost** at the employee level.

### Key Features
* **Tax Logic:** Automatically applies FICA caps (e.g., stopping Social Security tax collection after the wage base limit is hit).
* **Scenario Toggling:** "Boolean" flags to instantly model Reduction in Force (RIF) or Hiring Freeze scenarios without deleting data.
* **Roster Reconciliation:** Automates the diff between "Finance Plan" vs. "HRIS Actuals."

---

## MODULE B: Stochastic Risk Simulator ("Project Alpha")
### Business Problem
Traditional variance analysis is deterministic—it compares a single Budget number to a single Actual number. It ignores **probability** and **tail risk**.

### The Solution
A Monte Carlo simulation engine that replaces point-estimates with probability distributions.

### Key Features
* **Volatility Modeling:** Simulates 10,000+ iterations of key drivers (e.g., Volume, Price, FX Rates) based on historical standard deviation.
* **Confidence Intervals:** Outputs P&L metrics as ranges (e.g., "We are 95% confident Net Income will land between $X and $Y") rather than a false precise number.
* **Tail Risk Identification:** Quantifies the "Black Swan" worst-case scenarios that static budgets miss.

---

## MODULE C: Driver-Based Rolling Forecast ("Project Charlie")
### Business Problem
Annual budgets become obsolete by Q1. Organizations need a "Rolling Forecast" that updates continuously, but manual Excel processes are too slow to support this cadence.

### The Solution
A "Headless" forecasting engine where assumptions (Drivers) are decoupled from the calculation logic.

### Key Features
* **Configuration-Based:** Drivers (Growth %, Retention %, Churn %) are stored in a separate configuration file (YAML/JSON), allowing for instant re-forecasting without touching code.
* **Waterfall Modeling:** Automatically generates revenue waterfalls to show cohort retention over time.
* **Speed:** Reduces the forecast cycle from days to minutes.

---

## Tech Stack
* **Language:** Python 3.9+
* **Libraries:** Pandas, NumPy, Scikit-Learn (for simulations)
* **Input/Output:** SQL Queries, Excel Flat Files, CSV

## Projects
1. **[Risk Simulator](./Risk_Simulator)** - Stochastic Monte Carlo engine for revenue variance analysis.
2. **[Headcount Model](./Headcount_Model)** - Algo-driven labor cost modeling with RIF/Hiring Freeze scenario toggles.
3. **[Rolling Forecast](./Rolling_Forecast)** - Driver-based P&L engine using YAML configurations.
