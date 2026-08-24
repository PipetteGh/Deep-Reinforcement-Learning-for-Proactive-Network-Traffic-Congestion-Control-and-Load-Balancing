import os
import yaml
import pandas as pd
import numpy as np
from stable_baselines3 import DQN, PPO
from src.environment.network_congestion_env import NetworkCongestionEnv
from src.baselines.ecmp import evaluate_ecmp

def evaluate_agent(model, env, num_episodes=5):
    results = {
        "mean_utilization": [],
        "congestion_penalty": [],
        "rewards": []
    }
    
    for ep in range(num_episodes):
        obs, _ = env.reset()
        done = False
        truncated = False
        ep_reward = 0
        
        while not (done or truncated):
            action, _ = model.predict(obs, deterministic=True)
            obs, reward, done, truncated, info = env.step(action)
            ep_reward += reward
            
        results["mean_utilization"].append(info["mean_utilization"])
        results["congestion_penalty"].append(info["congestion_penalty"])
        results["rewards"].append(ep_reward)
        
    return results

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    with open(os.path.join(base_dir, 'configs', 'topologies.yaml'), 'r') as f:
        tops = yaml.safe_load(f)
        
    test_topologies = tops.get('test_topologies', [])
    seeds = tops.get('random_seeds', [42, 100, 2024, 777, 1337])
    traffic_modes = ['moderate', 'burst', 'congestion']
    
    # We will pick the first seed's trained model as our champion for simplicity in this evaluation
    seed = seeds[0]
    
    dqn_path = os.path.join(base_dir, 'models', 'dqn', f'dqn_final_seed_{seed}.zip')
    ppo_path = os.path.join(base_dir, 'models', 'ppo', f'ppo_final_seed_{seed}.zip')
    
    try:
        dqn_model = DQN.load(dqn_path)
        ppo_model = PPO.load(ppo_path)
    except FileNotFoundError:
        print("Models not found. Make sure training (Phase 11) is completed.")
        return
        
    results_data = []
    
    env = NetworkCongestionEnv(
        topology_dir=os.path.join(base_dir, 'data', 'processed'),
        topologies=test_topologies,
        seed=999 # Use an unseen seed for evaluation
    )
    
    print("Evaluating generalization on unseen topologies and traffic patterns...")
    
    for mode in traffic_modes:
        print(f"Testing traffic mode: {mode}")
        env.traffic_mode = mode
        
        # Test ECMP
        print("  Running ECMP Baseline...")
        ecmp_res = evaluate_ecmp(env, num_episodes=10)
        results_data.append({
            'Agent': 'ECMP',
            'Traffic': mode,
            'Mean Utilization': np.mean(ecmp_res['mean_utilization']),
            'Congestion Penalty': np.mean(ecmp_res['congestion_penalty']),
            'Reward': np.mean(ecmp_res['rewards'])
        })
        
        # Test DQN
        print("  Running DQN Agent...")
        dqn_res = evaluate_agent(dqn_model, env, num_episodes=10)
        results_data.append({
            'Agent': 'DQN',
            'Traffic': mode,
            'Mean Utilization': np.mean(dqn_res['mean_utilization']),
            'Congestion Penalty': np.mean(dqn_res['congestion_penalty']),
            'Reward': np.mean(dqn_res['rewards'])
        })
        
        # Test PPO
        print("  Running PPO Agent...")
        ppo_res = evaluate_agent(ppo_model, env, num_episodes=10)
        results_data.append({
            'Agent': 'PPO',
            'Traffic': mode,
            'Mean Utilization': np.mean(ppo_res['mean_utilization']),
            'Congestion Penalty': np.mean(ppo_res['congestion_penalty']),
            'Reward': np.mean(ppo_res['rewards'])
        })
        
    df = pd.DataFrame(results_data)
    results_path = os.path.join(base_dir, 'results', 'generalization.csv')
    df.to_csv(results_path, index=False)
    print(f"\nGeneralization testing complete. Results saved to {results_path}")
    print(df)

if __name__ == "__main__":
    main()
