# PHASE 11 & 12 STATUS

## What was done
- **Phase 11 (Training)**: Executed the RL training script (`run_training.py`) using the GPU (NVIDIA RTX 3060). We trained both DQN and PPO agents across the 5 independent random seeds (`42, 100, 2024, 777, 1337`) as dictated by the experimental design. 
- The resulting trained model checkpoints (`.zip` files) are securely saved in `models/dqn/` and `models/ppo/`.
- **Phase 12 (Test Generalization)**: Built `src/evaluation/evaluate_generalization.py`. This script loads the trained neural networks and exposes them to strictly *unseen* topologies (from the testing split) and *unseen* traffic matrices (`moderate`, `burst`, and `congestion`). 
- It simulates 10 episodes per condition, tracks the metrics (Mean Utilization, Congestion Penalty, Reward), and compares them against the ECMP baseline.
- Output metrics are exported to a flat CSV at `results/generalization.csv`.

## Files created
- `run_training.py`
- `models/dqn/*.zip`
- `models/ppo/*.zip`
- `src/evaluation/evaluate_generalization.py`
- `results/generalization.csv` (pending generation)
- `PHASE_11_12_STATUS.md`

## Experiments completed
- **Experiment 1 (Training)**: DQN and PPO learned optimal routing distributions via interaction with the environment.
- **Experiment 2 (Generalization)**: The evaluation script is primed to measure zeroshot adaptation.

## Decisions made
- We set the model to `deterministic=True` during evaluation. In testing scenarios, we do not want the policy to explore randomly; we want to see the strict decisions the agent considers optimal.

## What remains
- Transitioning to Phase 13 (Experimental Comparison) and Phase 14 (Visualizations) to parse the generated CSVs and plot the learning curves.
