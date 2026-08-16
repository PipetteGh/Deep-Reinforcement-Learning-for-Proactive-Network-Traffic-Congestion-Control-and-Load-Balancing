# PHASE 8, 9, & 10 STATUS

## What was done
- Implemented **Deep Q-Network (DQN)** (Phase 8) in `src/agents/train_dqn.py`. Configured the neural network, experience replay, epsilon exploration strategy, and learning rate through `configs/dqn.yaml`.
- Implemented **Proximal Policy Optimization (PPO)** (Phase 9) in `src/agents/train_ppo.py`. Configured the rollout size, batch size, epochs, and clipping parameters through `configs/ppo.yaml`.
- Both agents use the `MlpPolicy` from `stable-baselines3`, configured to train on the selected topologies using the established `NetworkCongestionEnv`.
- Formulated a weighted **Reward Function** (Phase 10) matching the environment's metrics: `(0.4 * normalized_throughput) - (0.3 * normalized_latency) - (0.2 * packet_loss) - (0.1 * congestion_penalty)`. Saved this to `configs/reward.yaml` and integrated dynamic config loading into the Gymnasium environment.

## Files created
- `src/agents/train_dqn.py`
- `configs/dqn.yaml`
- `models/dqn/`
- `src/agents/train_ppo.py`
- `configs/ppo.yaml`
- `models/ppo/`
- `configs/reward.yaml`
- `PHASE_8_10_STATUS.md`

## Experiments completed
- Setup and compilation of training scripts verified. No full training loops run yet (scheduled for Phase 11).

## Problems encountered
- Reinforcement learning libraries like `stable-baselines3` expect strict numpy scalar float types for rewards. The Python environment reward logic occasionally returned nested floats or ints, which caused `EnvChecker` warnings. 
- *Solution*: Coerced the final calculated reward specifically to `float(reward)`.

## Decisions made
- We set the default training timesteps for DQN and PPO to `50000` inside their configurations to ensure they can run within a reasonable timeframe, with checkpoint callbacks saving every 10,000 steps.

## What remains
- Transitioning to Phase 11 (Training Procedure): Executing the training scripts across the random seeds.
