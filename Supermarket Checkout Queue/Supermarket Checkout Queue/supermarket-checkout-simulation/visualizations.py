import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import os

# ============================================
# 🎨 PREMIUM THEME CONFIGURATION
# ============================================
# Dark theme with vibrant accent colors
DARK_BG = '#1a1a2e'
CARD_BG = '#16213e'
ACCENT_1 = '#e94560'  # Vibrant Pink/Red
ACCENT_2 = '#0f3460'  # Deep Blue
ACCENT_3 = '#00d9ff'  # Cyan
ACCENT_4 = '#7b2cbf'  # Purple
TEXT_COLOR = '#eaeaea'
GRID_COLOR = '#2a2a4a'

# Gradient colors for bars
GRADIENT_COLORS = ['#e94560', '#ff6b6b', '#feca57']
SERVER_COLORS = ['#00d9ff', '#7b2cbf', '#e94560']

def apply_dark_theme(ax, fig):
    """Apply consistent dark theme to axes and figure."""
    fig.patch.set_facecolor(DARK_BG)
    ax.set_facecolor(CARD_BG)
    ax.tick_params(colors=TEXT_COLOR, which='both')
    ax.xaxis.label.set_color(TEXT_COLOR)
    ax.yaxis.label.set_color(TEXT_COLOR)
    ax.title.set_color(TEXT_COLOR)
    for spine in ax.spines.values():
        spine.set_color(GRID_COLOR)
    ax.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.3)

def generate_visualizations(results_file='simulation_results.csv'):
    df = pd.read_csv(results_file)
    
    # Create outputs directory
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.size'] = 11

    # --- 1. Waiting Time Distribution (Premium) ---
    fig, ax = plt.subplots(figsize=(12, 7))
    apply_dark_theme(ax, fig)
    
    # Histogram with gradient effect
    n, bins, patches = ax.hist(df['Wait Time'], bins=30, edgecolor='white', linewidth=0.5, alpha=0.9)
    
    # Apply gradient to bars
    cm = plt.cm.get_cmap('magma')
    bin_centers = 0.5 * (bins[:-1] + bins[1:])
    col = bin_centers - min(bin_centers)
    col /= max(col) if max(col) > 0 else 1
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    # Add KDE line
    from scipy.stats import gaussian_kde
    kde = gaussian_kde(df['Wait Time'])
    x_kde = np.linspace(df['Wait Time'].min(), df['Wait Time'].max(), 200)
    ax2 = ax.twinx()
    ax2.plot(x_kde, kde(x_kde), color=ACCENT_3, linewidth=3, label='Density')
    ax2.set_facecolor('none')
    ax2.tick_params(colors=TEXT_COLOR)
    ax2.set_ylabel('Density', color=TEXT_COLOR)
    
    # Add mean and 95th percentile lines
    mean_wait = df['Wait Time'].mean()
    p95_wait = df['Wait Time'].quantile(0.95)
    ax.axvline(mean_wait, color=ACCENT_3, linestyle='--', linewidth=2.5, label=f'Mean: {mean_wait:.2f} min')
    ax.axvline(p95_wait, color=ACCENT_1, linestyle='--', linewidth=2.5, label=f'95th %: {p95_wait:.2f} min')
    
    ax.set_title('⏱️ Customer Waiting Time Distribution', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Waiting Time (minutes)', fontsize=12)
    ax.set_ylabel('Number of Customers', fontsize=12)
    ax.legend(loc='upper right', facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    
    plt.tight_layout()
    plt.savefig('outputs/waiting_time_dist.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 2. Counter Utilization (Premium Card Style) ---
    simulation_end_time = df['Service End Time'].max()
    server_stats = df.groupby('Server ID')['Service Time'].sum().reset_index()
    server_stats['Utilization (%)'] = (server_stats['Service Time'] / simulation_end_time) * 100
    
    fig, ax = plt.subplots(figsize=(10, 7))
    apply_dark_theme(ax, fig)
    
    bars = ax.bar(server_stats['Server ID'].astype(str), server_stats['Utilization (%)'], 
                  color=SERVER_COLORS, edgecolor='white', linewidth=2, width=0.6)
    
    # Add glow effect
    for bar, color in zip(bars, SERVER_COLORS):
        bar.set_alpha(0.9)
        # Add value labels on top
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 1, f'{height:.1f}%',
                ha='center', va='bottom', fontsize=14, fontweight='bold', color=TEXT_COLOR)
    
    # Add threshold line
    ax.axhline(85, color=ACCENT_1, linestyle='--', linewidth=2, alpha=0.7, label='Bottleneck Threshold (85%)')
    ax.axhline(50, color='#4ade80', linestyle='--', linewidth=2, alpha=0.7, label='Optimal Zone (50%)')
    
    ax.set_ylim(0, 110)
    ax.set_title('🖥️ Counter Utilization Performance', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Counter ID', fontsize=12)
    ax.set_ylabel('Utilization (%)', fontsize=12)
    ax.legend(loc='upper right', facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    
    plt.tight_layout()
    plt.savefig('outputs/counter_utilization.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 3. Throughput Over Time (Premium Line Chart) ---
    df['Completion Hour'] = (df['Service End Time'] // 60).astype(int)
    throughput = df.groupby('Completion Hour').size().reset_index(name='Customer Count')
    
    fig, ax = plt.subplots(figsize=(12, 6))
    apply_dark_theme(ax, fig)
    
    ax.fill_between(throughput['Completion Hour'], throughput['Customer Count'], alpha=0.3, color=ACCENT_3)
    ax.plot(throughput['Completion Hour'], throughput['Customer Count'], 
            marker='o', markersize=10, linewidth=3, color=ACCENT_3, markeredgecolor='white', markeredgewidth=2)
    
    # Add data labels
    for x, y in zip(throughput['Completion Hour'], throughput['Customer Count']):
        ax.annotate(f'{y}', (x, y), textcoords='offset points', xytext=(0, 10),
                   ha='center', fontsize=10, color=TEXT_COLOR, fontweight='bold')
    
    ax.set_title('📈 Throughput Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Hour of Simulation', fontsize=12)
    ax.set_ylabel('Customers Served', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('outputs/throughput_over_time.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 4. Queue Length Over Time (Area Chart) ---
    arrivals = pd.DataFrame({'time': df['Arrival Time'], 'change': 1})
    services = pd.DataFrame({'time': df['Service Start Time'], 'change': -1})
    events = pd.concat([arrivals, services]).sort_values('time')
    events['Queue Length'] = events['change'].cumsum()
    
    fig, ax = plt.subplots(figsize=(14, 6))
    apply_dark_theme(ax, fig)
    
    ax.fill_between(events['time'], events['Queue Length'], step='post', alpha=0.4, color=ACCENT_4)
    ax.step(events['time'], events['Queue Length'], where='post', linewidth=2, color=ACCENT_4)
    
    # Highlight peak
    max_queue = events['Queue Length'].max()
    max_time = events[events['Queue Length'] == max_queue]['time'].iloc[0]
    ax.scatter([max_time], [max_queue], color=ACCENT_1, s=200, zorder=5, edgecolor='white', linewidth=2)
    ax.annotate(f'Peak: {max_queue}', (max_time, max_queue), textcoords='offset points', 
                xytext=(10, 10), fontsize=12, color=ACCENT_1, fontweight='bold',
                arrowprops=dict(arrowstyle='->', color=ACCENT_1))
    
    ax.set_title('📊 Queue Length Over Time', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Time (minutes)', fontsize=12)
    ax.set_ylabel('Customers in Queue', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('outputs/queue_length_over_time.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 5. Gantt Chart (Premium Timeline) ---
    subset = df.head(40)  # First 40 for readability
    
    fig, ax = plt.subplots(figsize=(16, 8))
    apply_dark_theme(ax, fig)
    
    for i, (idx, row) in enumerate(subset.iterrows()):
        server_id = int(row['Server ID'])
        color = SERVER_COLORS[server_id - 1]
        
        # Draw bar
        ax.barh(y=server_id, width=row['Service Time'], left=row['Service Start Time'], 
                color=color, edgecolor='white', linewidth=0.5, alpha=0.85, height=0.6)
        
        # Add customer ID
        if row['Service Time'] > 1:  # Only label if bar is wide enough
            ax.text(row['Service Start Time'] + row['Service Time']/2, server_id, 
                    f"C{int(row['Customer ID'])}", ha='center', va='center', 
                    color='white', fontsize=8, fontweight='bold')
    
    ax.set_xlabel('Time (minutes)', fontsize=12)
    ax.set_ylabel('Counter ID', fontsize=12)
    ax.set_yticks([1, 2, 3])
    ax.set_yticklabels(['Counter 1', 'Counter 2', 'Counter 3'])
    ax.set_title('🗓️ Service Timeline (Gantt Chart - First 40 Customers)', fontsize=16, fontweight='bold', pad=20)
    
    # Legend
    legend_patches = [mpatches.Patch(color=c, label=f'Counter {i+1}') for i, c in enumerate(SERVER_COLORS)]
    ax.legend(handles=legend_patches, loc='upper right', facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    
    plt.tight_layout()
    plt.savefig('outputs/gantt_chart.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 6. Service Time Histogram (Premium) ---
    fig, ax = plt.subplots(figsize=(12, 7))
    apply_dark_theme(ax, fig)
    
    n, bins, patches = ax.hist(df['Service Time'], bins=25, edgecolor='white', linewidth=0.5, alpha=0.9)
    
    # Apply gradient
    cm = plt.cm.get_cmap('viridis')
    col = (bins[:-1] - min(bins[:-1])) / (max(bins[:-1]) - min(bins[:-1]) + 0.001)
    for c, p in zip(col, patches):
        plt.setp(p, 'facecolor', cm(c))
    
    mean_service = df['Service Time'].mean()
    ax.axvline(mean_service, color=ACCENT_1, linestyle='--', linewidth=2.5, label=f'Mean: {mean_service:.2f} min')
    
    ax.set_title('⚡ Service Time Distribution', fontsize=16, fontweight='bold', pad=20)
    ax.set_xlabel('Service Time (minutes)', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.legend(facecolor=CARD_BG, edgecolor=GRID_COLOR, labelcolor=TEXT_COLOR)
    
    plt.tight_layout()
    plt.savefig('outputs/service_time_dist.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    # --- 7. NEW: Dashboard Summary (Combined Metrics) ---
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.patch.set_facecolor(DARK_BG)
    fig.suptitle('🛒 SUPERMARKET QUEUE PERFORMANCE DASHBOARD', fontsize=20, fontweight='bold', color=TEXT_COLOR, y=0.98)
    
    # Metric Cards
    metrics = [
        ('Total Customers', f"{len(df)}", '👥'),
        ('Avg Wait Time', f"{df['Wait Time'].mean():.1f} min", '⏱️'),
        ('Throughput', f"{(len(df) / (df['Service End Time'].max() / 60)):.1f}/hr", '📈'),
        ('95th % Wait', f"{df['Wait Time'].quantile(0.95):.1f} min", '⚠️'),
        ('Avg Utilization', f"{server_stats['Utilization (%)'].mean():.1f}%", '🔄'),
        ('Peak Queue', f"{int(events['Queue Length'].max())}", '📊')
    ]
    
    for ax, (title, value, emoji) in zip(axes.flatten(), metrics):
        apply_dark_theme(ax, fig)
        ax.text(0.5, 0.6, emoji, fontsize=50, ha='center', va='center', transform=ax.transAxes)
        ax.text(0.5, 0.3, value, fontsize=28, ha='center', va='center', transform=ax.transAxes, 
                color=ACCENT_3, fontweight='bold')
        ax.text(0.5, 0.1, title, fontsize=14, ha='center', va='center', transform=ax.transAxes, color=TEXT_COLOR)
        ax.set_xticks([])
        ax.set_yticks([])
    
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.savefig('outputs/dashboard_summary.png', dpi=150, facecolor=DARK_BG)
    plt.close()

    print("✅ All premium visualizations generated in 'outputs/' folder.")

if __name__ == "__main__":
    generate_visualizations()
