# Supermarket Checkout Queue Simulation

## 📌 Project Overview
This project simulates a supermarket checkout system to model queue performance. It uses a discrete-event simulation approach (`SimPy`) to model 3 parallel checkout counters served by a single queue (or efficient dispatching). The system generates synthetic data, simulates customer flow, computes performance metrics, and produces visual analytics.

## 📂 Directory Structure
```
/supermarket-checkout-simulation
│── main.py              # Entry point to run the full system
│── customers.csv        # Synthetic dataset (auto-generated)
│── generate_data.py     # Module for data generation
│── simulation.py        # Core simulation engine (SimPy)
│── analysis.py          # Metric calculation and reporting
│── visualizations.py    # Chart generation (Matplotlib/Seaborn)
│── simulation_results.csv # Raw output from simulation
│── analysis_report.txt  # Summary of metrics
│── outputs/             # Folder containing generated charts
│    │── waiting_time_dist.png
│    │── counter_utilization.png
│    │── throughput_over_time.png
│    │── queue_length_over_time.png
│    │── gantt_chart.png
│    │── service_time_dist.png
│── README.md            # This file
```

## 🚀 How to Run the Simulation
1. **Prerequisites**: Ensure you have Python 3 installed.
   Required libraries: `simpy`, `pandas`, `numpy`, `matplotlib`, `seaborn`.
   ```bash
   pip install simpy pandas numpy matplotlib seaborn
   ```

2. **Run the System**:
   Execute the main script to perform the entire pipeline (Data Generation -> Simulation -> Analysis -> Visualization).
   ```bash
   python main.py
   ```

3. **Check Results**:
   - Console output will show a summary report.
   - Detailed metrics are in `analysis_report.txt`.
   - Charts are saved in the `outputs/` directory.

## 📊 Metrics Explained

- **Average Waiting Time**: The mean time a customer spends in the queue before reaching a counter.
- **Throughput**: Usage rate of the system, measured in customers served per hour.
- **Counter Utilization**: The percentage of time a server is busy serving customers.
    - *Ideal Zone*: 70-85%.
    - *Bottleneck*: >85%.
    - *Underutilized*: <50%.
- **95th Percentile Waiting Time**: 95% of customers waited less than this amount. Useful for SLA tracking.
- **Workload Balance**: Measures if customers are distributed evenly across the 3 counters.

## 🧠 System Description & Assumptions
- **Queue Discipline**: FCFS (First-Come, First-Served).
- **Service Configuration**: 3 Parallel Servers (M/M/3). Customers go to the first available server.
- **Arrival Pattern**: Poisson arrival process (Exponentially distributed inter-arrival times).
- **Service Time**: Random durations (Exponential distribution + minimum service buffer).
- **Assumption**: Use of a shared queue model (or efficient dispatcher) ensures no server sits idle if there is a customer waiting, maximizing efficiency.

## 🖼️ Sample Outputs
The system automatically generates charts to help visualize the queue dynamics, including:
- **Gantt Chart**: To see exactly when each server was busy.
- **Queue Length over Time**: To identify peak congestion periods.

---
*Developed for EEX5362: Performance Modelling*
