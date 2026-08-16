import os
import yaml
from stable_baselines3 import PPO
from src.environment.network_congestion_env import NetworkCongestionEnv
from stable_baselines3.common.callbacks import CheckpointCallback

def train_ppo(seed=42):
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    with open(os.path.join(base_dir, 'configs', 'ppo.yaml'), 'r') as f:
        config = yaml.safe_load(f)
    
    with open(os.path.join(base_dir, 'configs', 'topologies.yaml'), 'r') as f:
        tops = yaml.safe_load(f)
        
    env = NetworkCongestionEnv(
        topology_dir=os.path.join(base_dir, 'data', 'processed'),
        topologies=tops['training_topologies'],
        seed=seed
    )
    
    model = PPO(
        config['policy'],
        env,
        learning_rate=config['learning_rate'],
        n_steps=config['n_steps'],
        batch_size=config['batch_size'],
        n_epochs=config['n_epochs'],
        gamma=config['gamma'],
        gae_lambda=config['gae_lambda'],
        clip_range=config['clip_range'],
        ent_coef=config['ent_coef'],
        vf_coef=config['vf_coef'],
        max_grad_norm=config['max_grad_norm'],
        verbose=1,
        seed=seed
    )
    
    checkpoint_callback = CheckpointCallback(
        save_freq=10000, 
        save_path=os.path.join(base_dir, 'models', 'ppo'),
        name_prefix=f'ppo_model_seed_{seed}'
    )
    
    print(f"Starting PPO training for {config['timesteps']} timesteps with seed {seed}...")
    model.learn(total_timesteps=config['timesteps'], callback=checkpoint_callback)
    
    final_model_path = os.path.join(base_dir, 'models', 'ppo', f'ppo_final_seed_{seed}')
    model.save(final_model_path)
    print(f"PPO training complete. Model saved to {final_model_path}")

if __name__ == "__main__":
    train_ppo()
