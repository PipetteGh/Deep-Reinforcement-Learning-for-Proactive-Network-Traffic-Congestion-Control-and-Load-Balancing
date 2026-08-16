# PHASE 3, 4, 5, & 6 STATUS

## What was done
- Built `src/environment/network_congestion_env.py`, a custom Gymnasium environment.
- Formulated the **Markov Decision Process (MDP)** (Phase 4): 
  - State space is a fixed-size vector containing: link utilization (100 links), queue occupancy (100 links), and flow demands (50 flows).
- Defined the **Action Space** (Phase 5): 
  - Discrete action space with 3 choices for DQN compatibility: [0: keep path, 1: shift most congested flow to 2nd shortest path, 2: shift to 3rd shortest path].
- Developed **Traffic Generator** (Phase 6): 
  - `src/traffic/traffic_generator.py` can dynamically simulate "normal", "moderate", "heavy", "burst", and "congestion" traffic profiles.

## Files created
- `src/environment/network_congestion_env.py`
- `src/traffic/traffic_generator.py`
- `PHASE_3_6_STATUS.md`

## Experiments completed
- None.

## Problems encountered
- Dynamic graphs with variable node/edge counts cannot be natively passed to standard MLP-based RL algorithms (like DQN/PPO in Stable-Baselines3). 
- *Solution*: We adopted a fixed observation array (padding missing links/flows with zeros) to enable the algorithm to generalize across different topologies using the same neural architecture.

## Decisions made
- We combined the implementation of Phases 3 to 6 as they represent the cohesive construction of the reinforcement learning sandbox. 

## What remains
- Transitioning to Phase 7: Implement Equal-Cost Multi-Path (ECMP) routing as our baseline.
