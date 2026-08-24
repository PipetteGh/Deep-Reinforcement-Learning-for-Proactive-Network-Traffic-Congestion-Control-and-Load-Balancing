import os
import yaml
from stable_baselines3 import DQN
from src.environment.network_congestion_env import NetworkCongestionEnv
from stable_baselines3.common.callbacks import CheckpointCallback

def train_dqn(seed=42):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    with open(os.path.join(base_dir, 'configs', 'dqn.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    
    with open(os.path.join(base_dir, 'configs', 'topologies.yaml'), 'r') as f:
        tops = yaml.safe_load(f)
        
    env = NetworkCongestionEnv(
        topology_dir=os.path.join(base_dir, 'data', 'processed'),
        topologies=tops['training_topologies'],
        seed=seed
    )
    
    model = DQN(
        config['policy'],
        env,
        learning_rate=config['learning_rate'],
        buffer_size=config['buffer_size'],
        learning_starts=config['learning_starts'],
        batch_size=config['batch_size'],
        tau=config['tau'],
        gamma=config['gamma'],
        train_freq=config['train_freq'],
        gradient_steps=config['gradient_steps'],
        exploration_fraction=config['exploration_fraction'],
        exploration_initial_eps=config['exploration_initial_eps'],
        exploration_final_eps=config['exploration_final_eps'],
        verbose=1,
        seed=seed
    )
    
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, 
        save_path=os.path.join(base_dir, 'models', 'dqn'),
        name_prefix=f'dqn_model_seed_{seed}'
    )
    
    print(f"Starting DQN training for {config['timesteps']} timesteps with seed {seed}...")
    model.learn(total_timesteps=config['timesteps'], callback=checkpoint_callback)
    
    final_model_path = os.path.join(base_dir, 'models', 'dqn', f'dqn_final_seed_{seed}')
    model.save(final_model_path)
    print(f"DQN training complete. Model saved to {final_model_path}")

if __name__ == "__main__":
    train_dqn()
