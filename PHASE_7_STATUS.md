# PHASE 7 STATUS

## What was done
- Implemented the Equal-Cost Multi-Path (ECMP) routing algorithm in `src/baselines/ecmp.py`.
- Developed the `ECMPAgent` class which mimics the Stable-Baselines3 API (`predict` method) to allow for seamless 1:1 comparison with our future DRL agents in the environment loop.
- Built an `evaluate_ecmp` function to run the baseline and log metrics (mean utilization, congestion penalty, rewards).

## Files created
- `src/baselines/ecmp.py`
- `PHASE_7_STATUS.md`

## Experiments completed
- None.

## Problems encountered
- A true hardware-level ECMP hashes packet headers (5-tuple) to distribute traffic over equal-cost paths. In our MDP, which operates on discrete flow-shifting actions at fixed timesteps, mimicking this exactly is difficult. 
- *Solution*: We implemented a stochastic load-balancing behavior for the ECMP agent that randomly and uniformly distributes flows across the available equal-cost candidate paths over time, capturing the statistical behavior of ECMP flow hashing.

## Decisions made
- We designed the baseline agent to match the interface of our upcoming DQN/PPO models to ensure we evaluate them under identical conditions (Experiment 1 requirement).

## What remains
- Transitioning to Phase 8 and 9: Implementing the Deep Q-Network (DQN) and Proximal Policy Optimization (PPO) agents using Stable-Baselines3.
