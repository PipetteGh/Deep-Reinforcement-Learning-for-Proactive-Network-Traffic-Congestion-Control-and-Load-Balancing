import numpy as np
import random

class ECMPAgent:
    """
    Equal-Cost Multi-Path (ECMP) routing baseline.
    Does not learn from observations. Instead, it statically hashes/distributes 
    flows across all paths that have an equal (or near-equal) cost.
    """
    def __init__(self, env):
        self.env = env
        
    def predict(self, obs, state=None, episode_start=None, deterministic=True):
        """
        Mimics the Stable-Baselines3 predict signature.
        For ECMP, the action is to uniformly select among equal-cost paths for the active flows.
        Because our Gym action space is (0: keep, 1: shift to path 2, 2: shift to path 3) for a random flow,
        an ECMP agent would ideally just uniformly random distribute traffic.
        """
        # A true ECMP distributes flows over equal cost paths at flow arrival.
        # To simulate this in our MDP step format, we can randomly take action 1 or 2 
        # to continuously balance the load across candidate paths.
        action = random.choice([0, 1, 2])
        return action, None

def evaluate_ecmp(env, num_episodes=5):
    """
    Evaluates the ECMP baseline on the given environment.
    """
    agent = ECMPAgent(env)
    
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
            action, _ = agent.predict(obs)
            obs, reward, done, truncated, info = env.step(action)
            ep_reward += reward
            
        results["mean_utilization"].append(info["mean_utilization"])
        results["congestion_penalty"].append(info["congestion_penalty"])
        results["rewards"].append(ep_reward)
        
    return results
