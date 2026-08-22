import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def fix_plots():
    # 1. Regenerate Burst Performance Bar Chart (Horizontal)
    agents = ['ECMP', 'DQN', 'PPO']
    rewards = [-54.12, -49.48, -58.52] # Taken from the README values for burst
    
    # Flip values so it points right and is easier to read
    # Or just plot horizontally and let them go left, but we can just use Absolute Penalty 
    # to make it positive if we want, or keep it negative but horizontal.
    
    plt.figure(figsize=(10, 4))
    y_pos = np.arange(len(agents))
    plt.barh(y_pos, rewards, color=['gray', 'red', 'blue'])
    plt.yticks(y_pos, agents)
    plt.xlabel('Overall Episode Reward (Higher is Better)')
    plt.title('Overall Reward Under Burst Traffic Constraints')
    plt.grid(True, axis='x', linestyle='--', alpha=0.7)
    plt.savefig('results/plots/burst_performance_bar.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print("Fixed visual plots generated successfully.")

if __name__ == "__main__":
    fix_plots()
