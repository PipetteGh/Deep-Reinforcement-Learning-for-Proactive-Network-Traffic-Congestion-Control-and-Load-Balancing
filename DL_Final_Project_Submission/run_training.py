import os
import yaml
from src.agents.train_dqn import train_dqn
from src.agents.train_ppo import train_ppo

def main():
    base_dir = os.path.abspath(os.path.dirname(__file__))
    config_path = os.path.join(base_dir, 'configs', 'topologies.yaml')
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        
    seeds = config.get('random_seeds', [42, 100, 2024, 777, 1337])
    
    print("Starting Training Protocol (Phase 11)...")
    print(f"Targeting CUDA GPU (RTX 3060) if available via stable-baselines3 'auto' device policy.")
    
    for seed in seeds:
        print(f"--- Training DQN with seed {seed} ---")
        train_dqn(seed=seed)
        
    for seed in seeds:
        print(f"--- Training PPO with seed {seed} ---")
        train_ppo(seed=seed)
        
    print("All training runs completed.")

if __name__ == "__main__":
    main()
