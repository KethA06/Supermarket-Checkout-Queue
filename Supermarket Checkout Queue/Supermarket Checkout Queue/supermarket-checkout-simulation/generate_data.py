import pandas as pd
import numpy as np
import os

def generate_data(num_customers=500, mean_inter_arrival=1.0, mean_service_time=2.5, seed=42):
    """
    Generates synthetic customer data for supermarket simulation.
    
    Parameters:
    - num_customers: Total number of customers to generate
    - mean_inter_arrival: Average time between arrivals (minutes) - Exponential distribution
    - mean_service_time: Average service time (minutes) - Exponential distribution
    - seed: Random seed for reproducibility
    """
    np.random.seed(seed)
    
    # Generate Inter-arrival times (Exponential distribution)
    inter_arrival_times = np.random.exponential(scale=mean_inter_arrival, size=num_customers)
    
    # Calculate exact arrival times (Cumulative sum)
    arrival_times = np.cumsum(inter_arrival_times)
    
    # Generate Service times (Exponential distribution)
    # Adding a small buffer to avoid near-zero service times which are unrealistic for checkout
    min_service_time = 0.5
    service_times = np.random.exponential(scale=mean_service_time, size=num_customers) 
    
    # Ensure no service time is below minimum (optional realism adjustment)
    service_times = np.maximum(service_times, min_service_time)
    
    # Create DataFrame
    df = pd.DataFrame({
        'Customer ID': range(1, num_customers + 1),
        'Arrival Time': np.round(arrival_times, 2),
        'Service Time': np.round(service_times, 2)
    })
    
    # Save to CSV
    output_path = 'customers.csv'
    df.to_csv(output_path, index=False)
    print(f"✅ Generated {num_customers} customers in '{output_path}'")
    print(f"   Mean Inter-arrival: {mean_inter_arrival} min (Target: {mean_inter_arrival})")
    print(f"   Mean Service Time: {df['Service Time'].mean():.2f} min (Target: {mean_service_time})")
    return df

if __name__ == "__main__":
    # Parameters designed for ~83% utilization with 3 servers
    # Arrival Rate = 1/1.0 = 1.0 cust/min
    # Service Rate per server = 1/2.5 = 0.4 cust/min
    # Total Service Capacity = 3 * 0.4 = 1.2 cust/min
    # Utilization = 1.0 / 1.2 = 0.833
    generate_data(num_customers=500, mean_inter_arrival=1.0, mean_service_time=2.5)
