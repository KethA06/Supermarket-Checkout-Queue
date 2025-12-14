import simpy
import pandas as pd
import numpy as np

class CheckoutLane:
    def __init__(self, env, lane_id):
        self.env = env
        self.lane_id = lane_id
        self.busy_time = 0
        self.customers_served = []

    def serve(self, customer, queue_store):
        """
        Continuous process: wait for customer, serve, repeat.
        """
        while True:
            # Wait for a customer to arrive in the shared queue
            customer_data = yield queue_store.get()
            
            # Customer is now dequeued. 
            # In a real line, the customer moves to the counter.
            
            start_service_time = self.env.now
            wait_time = start_service_time - customer_data['arrival_time']
            
            # Log usage
            service_duration = customer_data['service_time']
            
            # Simulate Service
            yield self.env.timeout(service_duration)
            
            end_service_time = self.env.now
            self.busy_time += service_duration
            
            # Record metrics for this customer
            record = {
                'Customer ID': customer_data['id'],
                'Arrival Time': customer_data['arrival_time'],
                'Service Start Time': start_service_time,
                'Service End Time': end_service_time,
                'Service Time': service_duration,
                'Wait Time': wait_time,
                'Server ID': self.lane_id,
                'Time in System': wait_time + service_duration
            }
            self.customers_served.append(record)

def customer_generator(env, customers_df, queue_store):
    """
    Generates customers based on the arrival times in the dataframe.
    """
    # Iterate through each customer in the sorted dataframe
    # We assume dataframe is sorted by Arrival Time
    for index, row in customers_df.iterrows():
        arrival_time = row['Arrival Time']
        yield env.timeout(arrival_time - env.now)  # Wait until arrival time
        
        customer_payload = {
            'id': int(row['Customer ID']),
            'arrival_time': arrival_time,
            'service_time': row['Service Time']
        }
        
        # Put customer in the SHARED queue
        # The servers (CheckoutLanes) will pull from this queue
        yield queue_store.put(customer_payload)

def run_simulation(input_file='customers.csv', num_servers=3):
    # Load data
    df = pd.read_csv(input_file)
    
    # Sort just in case
    df = df.sort_values('Arrival Time')
    
    env = simpy.Environment()
    
    # Shared Queue (FCFS by default in SimPy Store)
    queue_store = simpy.Store(env)
    
    # Create Servers
    servers = [CheckoutLane(env, i+1) for i in range(num_servers)]
    
    # Start Server Processes
    for server in servers:
        env.process(server.serve(None, queue_store))
        
    # Start Customer Generator
    env.process(customer_generator(env, df, queue_store))
    
    # Run until all customers are processed
    # A simple way is to run until a large time, or better:
    # We can't easily know when the store is empty unless we track count.
    # We will run for (last_arrival + sum of max service times + buffer) 
    # Or just run until the process is done? 
    # SimPy env.run() goes until no events. Since servers wait forever on queue.get(), 
    # we need a termination condition.
    
    last_arrival = df['Arrival Time'].iloc[-1]
    # Estimation: run enough time for the queue to clear
    # A safer way: Check queue length and active processing?
    # Simplest: Run for Last Arrival + 1000 mins buffer.
    env.run(until=last_arrival + 1000)
    
    # Collect results
    all_records = []
    for server in servers:
        all_records.extend(server.customers_served)
        
    results_df = pd.DataFrame(all_records)
    results_df = results_df.sort_values('Customer ID')
    
    # Save results
    output_file = 'simulation_results.csv'
    results_df.to_csv(output_file, index=False)
    print(f"✅ Simulation complete. Results saved to {output_file}")
    return results_df, servers

if __name__ == "__main__":
    run_simulation()
