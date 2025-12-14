import generate_data
import simulation
import analysis
import visualizations
import os

def main():
    print("🚀 Starting Supermarket Queue Simulation System...")
    print("-" * 50)
    
    # 1. Generate Data
    print("\n[1/4] Generating Customer Data...")
    generate_data.generate_data(num_customers=500, mean_inter_arrival=1.0, mean_service_time=2.5)
    
    # 2. Run Simulation
    print("\n[2/4] Running Simulation Engine...")
    simulation.run_simulation()
    
    # 3. Analyze Results
    print("\n[3/4] Analyzing Performance Metrics...")
    analysis.analyze_results()
    
    # 4. Visualize
    print("\n[4/4] Generating Visualizations...")
    visualizations.generate_visualizations()
    
    print("-" * 50)
    print("✅ System execution complete!")
    print(f"📂 Outputs available in: {os.path.abspath('outputs')}")
    print(f"📄 Report available in: {os.path.abspath('analysis_report.txt')}")

if __name__ == "__main__":
    main()
