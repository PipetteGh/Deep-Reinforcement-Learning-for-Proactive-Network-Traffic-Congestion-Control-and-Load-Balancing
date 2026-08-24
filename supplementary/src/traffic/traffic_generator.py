import random
import numpy as np

class TrafficGenerator:
    def __init__(self, nodes, valid_pairs, max_flows=50):
        self.nodes = nodes
        self.valid_pairs = valid_pairs
        self.max_flows = max_flows
        
    def generate(self, mode="normal"):
        """
        Generates synthetic traffic workloads for the network.
        Modes: normal, moderate, heavy, burst, congestion
        """
        active_flows = []
        num_flows = min(self.max_flows, len(self.nodes) * 2)
        
        for _ in range(num_flows):
            src, dst = random.sample(self.nodes, 2)
            pair = f"{src}_{dst}"
            if pair in self.valid_pairs:
                demand = self._sample_demand(mode)
                active_flows.append({"src": src, "dst": dst, "demand": demand, "pair": pair})
                
        return active_flows

    def _sample_demand(self, mode):
        # Base capacity is 1.0 in normalized space
        if mode == "normal":
            return np.random.uniform(0.1, 0.3)
        elif mode == "moderate":
            return np.random.uniform(0.3, 0.6)
        elif mode == "heavy":
            return np.random.uniform(0.6, 0.9)
        elif mode == "burst":
            # 80% chance of normal, 20% chance of huge burst
            if random.random() < 0.2:
                return np.random.uniform(1.0, 1.5)
            else:
                return np.random.uniform(0.1, 0.3)
        elif mode == "congestion":
            # Sustained high demand guaranteed to overflow queues
            return np.random.uniform(0.9, 1.2)
        else:
            return np.random.uniform(0.1, 0.3)
