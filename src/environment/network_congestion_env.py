import gymnasium as gym
from gymnasium import spaces
import numpy as np
import networkx as nx
import json
import os
import random

MAX_LINKS = 100
MAX_FLOWS = 50

class NetworkCongestionEnv(gym.Env):
    """
    Custom Environment that follows gym interface.
    Models network congestion and proactive load balancing.
    """
    metadata = {'render.modes': ['console']}

    def __init__(self, topology_dir, topologies, seed=None):
        super(NetworkCongestionEnv, self).__init__()
        
        self.topology_dir = topology_dir
        self.topologies = topologies
        self.current_topology_name = None
        self.graph = None
        self.paths = None
        
        # State: [link_utilization (MAX_LINKS), queue_occupancy (MAX_LINKS), flow_demands (MAX_FLOWS)]
        # Total size = 250
        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(MAX_LINKS * 2 + MAX_FLOWS,), dtype=np.float32
        )
        
        # Action space: Discrete(3)
        # 0: Keep current routing
        # 1: Move highest-congested flow to candidate path 2
        # 2: Move highest-congested flow to candidate path 3
        self.action_space = spaces.Discrete(3)
        
        self.edge_mapping = {}
        self.active_flows = []
        self.flow_routes = {}
        
        # For tracking metrics
        self.current_step = 0
        self.max_steps = 200
        
        self.seed(seed)
        
    def seed(self, seed=None):
        self.np_random, seed = gym.utils.seeding.np_random(seed)
        random.seed(seed)
        return [seed]

    def _load_topology(self, topology_name):
        self.current_topology_name = topology_name
        graph_path = os.path.join(self.topology_dir, f"{topology_name}_processed.graphml")
        paths_path = os.path.join(self.topology_dir, f"{topology_name}_paths.json")
        
        self.graph = nx.read_graphml(graph_path)
        with open(paths_path, 'r') as f:
            self.paths = json.load(f)
            
        # Create a fixed mapping of edges to indices (up to MAX_LINKS)
        self.edge_mapping = {e: i for i, e in enumerate(self.graph.edges()) if i < MAX_LINKS}
        
    def _generate_traffic(self):
        # Use the Phase 6 Traffic Generator
        from src.traffic.traffic_generator import TrafficGenerator
        nodes = list(self.graph.nodes())
        tg = TrafficGenerator(nodes, self.paths, max_flows=MAX_FLOWS)
        self.active_flows = tg.generate(mode=getattr(self, 'traffic_mode', 'normal'))
        self.flow_routes = {f["pair"]: 0 for f in self.active_flows}
                
    def _calculate_state(self):
        link_utils = np.zeros(MAX_LINKS, dtype=np.float32)
        queue_occs = np.zeros(MAX_LINKS, dtype=np.float32)
        flow_dems = np.zeros(MAX_FLOWS, dtype=np.float32)
        
        # Calculate load on each link based on active flows and their current routes
        link_loads = {e: 0.0 for e in self.graph.edges()}
        link_loads.update({(v, u): 0.0 for u, v in self.graph.edges()}) # Undirected safety
        
        for i, flow in enumerate(self.active_flows):
            if i >= MAX_FLOWS: break
            flow_dems[i] = flow["demand"]
            
            pair = flow["pair"]
            route_idx = self.flow_routes.get(pair, 0)
            if route_idx < len(self.paths[pair]):
                path = self.paths[pair][route_idx]
                for u, v in zip(path[:-1], path[1:]):
                    if (u, v) in link_loads:
                        link_loads[(u, v)] += flow["demand"]
                    elif (v, u) in link_loads:
                        link_loads[(v, u)] += flow["demand"]
                        
        # Map to state array
        for (u, v), load in link_loads.items():
            if (u, v) in self.edge_mapping:
                idx = self.edge_mapping[(u, v)]
                # Capacity from graph (normalized bw is just a proxy here, assume capacity = 1.0 for now)
                cap = float(self.graph.edges[u, v].get('bw_norm', 1.0)) 
                cap = max(cap, 0.1) # Prevent div by 0
                
                util = min(load / cap, 1.0)
                link_utils[idx] = util
                
                # Simple queue model: if util > 0.8, queue builds up
                if util > 0.8:
                    queue_occs[idx] = min((util - 0.8) * 5.0, 1.0)
                else:
                    queue_occs[idx] = 0.0
                    
        return np.concatenate([link_utils, queue_occs, flow_dems])

    def reset(self, seed=None, options=None):
        if seed is not None:
            self.seed(seed)
            
        topology_name = random.choice(self.topologies)
        self._load_topology(topology_name)
        self._generate_traffic()
        
        self.current_step = 0
        state = self._calculate_state()
        return state, {}

    def step(self, action):
        self.current_step += 1
        
        # Apply action (Phase 5 implementation)
        # Find the most "congested" flow (the one traversing the most utilized links)
        # To simplify, we just shift a random flow to path idx `action`
        if action > 0 and len(self.active_flows) > 0:
            target_flow = random.choice(self.active_flows)
            pair = target_flow["pair"]
            if action < len(self.paths[pair]):
                self.flow_routes[pair] = action
                
        # Calculate new state
        next_state = self._calculate_state()
        
        # Load Reward Config (Phase 10)
        import yaml
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        try:
            with open(os.path.join(base_dir, 'configs', 'reward.yaml'), 'r') as f:
                rew_cfg = yaml.safe_load(f)
        except:
            rew_cfg = {'w_throughput': 0.4, 'w_latency': 0.3, 'w_packet_loss': 0.2, 'w_congestion': 0.1}
            
        link_utils = next_state[:MAX_LINKS]
        queue_occs = next_state[MAX_LINKS:2*MAX_LINKS]
        
        # Calculate components
        mean_util = np.mean(link_utils[link_utils > 0]) if np.any(link_utils > 0) else 0.0
        normalized_throughput = 1.0 - mean_util # Simplified proxy for successful delivery
        
        normalized_latency = np.mean(queue_occs[queue_occs > 0]) if np.any(queue_occs > 0) else 0.0
        packet_loss = np.sum(queue_occs == 1.0) / MAX_LINKS # Proxy: saturated queues drop packets
        congestion_penalty = np.sum(queue_occs) / MAX_LINKS
        
        # Weighted formulation
        reward = (rew_cfg['w_throughput'] * normalized_throughput) - \
                 (rew_cfg['w_latency'] * normalized_latency) - \
                 (rew_cfg['w_packet_loss'] * packet_loss) - \
                 (rew_cfg['w_congestion'] * congestion_penalty)
        
        terminated = self.current_step >= self.max_steps
        truncated = False
        info = {
            "mean_utilization": mean_util,
            "congestion_penalty": congestion_penalty,
            "packet_loss": packet_loss
        }
        
        return next_state, float(reward), terminated, truncated, info

    def render(self, mode='console'):
        if mode == 'console':
            print(f"Step: {self.current_step}, Topology: {self.current_topology_name}")
