import pandas as pd
import numpy as np

def analyze_results(results_file='simulation_results.csv'):
    df = pd.read_csv(results_file)
    
    # --- 1. Average Waiting Time ---
    avg_waiting_time = df['Wait Time'].mean()
    
    # --- 2. Throughput ---
    # Customers per Hour
    start_time = df['Arrival Time'].min()
    end_time = df['Service End Time'].max()
    total_duration_minutes = end_time - start_time
    total_customers = len(df)
    throughput_per_hour = (total_customers / total_duration_minutes) * 60
    
    # --- 3. Counter Utilization ---
    # Utilization = (Total Busy Time) / (Total Simulation Time)
    # We should calculate this PER SERVER
    server_stats = df.groupby('Server ID')['Service Time'].sum().reset_index()
    server_stats.columns = ['Server ID', 'Total Busy Time']
    server_stats['Utilization (%)'] = (server_stats['Total Busy Time'] / end_time) * 100
    
    # --- 4. 95th Percentile Wait Time ---
    wait_time_p95 = df['Wait Time'].quantile(0.95)
    
    # --- 5. Workload Balance ---
    # We can look at the standard deviation of "Total Busy Time" or "Customer Count" across servers
    customers_per_server = df.groupby('Server ID').size().reset_index(name='Customer Count')
    workload_std = customers_per_server['Customer Count'].std()
    
    # --- 6. Total Time in System ---
    avg_time_in_system = df['Time in System'].mean()
    
    # --- Identification of Bottlenecks ---
    # Heuristic: If queueing delay is significant compared to service time
    # Or utilization is very high (> 85%)
    avg_service_time = df['Service Time'].mean()
    utilization_mean = server_stats['Utilization (%)'].mean()
    
    bottleneck_msg = []
    if utilization_mean > 85:
        bottleneck_msg.append(f"HIGH SYSTEM UTILIZATION ({utilization_mean:.1f}%). Servers are near capacity.")
    else:
        bottleneck_msg.append(f"System utilization is healthy ({utilization_mean:.1f}%).")
        
    if avg_waiting_time > avg_service_time:
         bottleneck_msg.append("Wait time exceeds service time. Process is bottlenecked by service rate.")
    
    # --- Output Report ---
    report = f"""
    ==================================================
    🛒 SUPERMARKET CHECKOUT SIMULATION REPORT
    ==================================================
    
    📊 OVERALL METRICS
    ------------------
    Total Customers Served: {total_customers}
    Total Simulation Time : {total_duration_minutes:.2f} minutes
    Throughput            : {throughput_per_hour:.2f} customers/hour
    Average Waiting Time  : {avg_waiting_time:.2f} minutes
    Average Time in System: {avg_time_in_system:.2f} minutes
    95th % Waiting Time   : {wait_time_p95:.2f} minutes
    
    🖥️ COUNTER METRICS
    ------------------
    """
    
    for _, row in server_stats.iterrows():
        sid = int(row['Server ID'])
        util = row['Utilization (%)']
        count = customers_per_server[customers_per_server['Server ID'] == sid]['Customer Count'].values[0]
        report += f"Counter {sid}: {util:.2f}% Utilization | Served {count} customers\n    "
        
    report += f"""
    Workload Imbalance (StdDev of counts): {workload_std:.2f}
    
    🚨 BOTTLENECK ANALYSIS
    ----------------------
    {chr(10).join(bottleneck_msg)}
    ==================================================
    """
    
    print(report)
    
    # Save simple metrics to text file
    with open('analysis_report.txt', 'w') as f:
        f.write(report)
        
    return server_stats

if __name__ == "__main__":
    analyze_results()
