import numpy as np

# Table 1: Zero-shot Generalization on 5 Held-out Topologies (Moderate Traffic)
topologies = ['Abilene', 'Janetbackbone', 'Bellcanada', 'Colt', 'Renater2001']
ecmp_scores = np.array([-66.12, -67.85, -68.40, -67.10, -69.03])
dqn_scores  = np.array([-59.40, -61.02, -61.55, -60.10, -62.14])
ppo_scores  = np.array([-63.15, -64.80, -65.20, -64.10, -66.00])

# Paired two-tailed t-test (df = 4) across the 5 held-out topologies:
diff_dqn = dqn_scores - ecmp_scores
mean_diff_dqn = np.mean(diff_dqn)
std_diff_dqn = np.std(diff_dqn, ddof=1)
t_dqn_table = mean_diff_dqn / (std_diff_dqn / np.sqrt(5))

diff_ppo = ppo_scores - ecmp_scores
mean_diff_ppo = np.mean(diff_ppo)
std_diff_ppo = np.std(diff_ppo, ddof=1)
t_ppo_table = mean_diff_ppo / (std_diff_ppo / np.sqrt(5))

print(f"Table 1 (Topologies, paired two-tailed t-test, df=4):")
print(f"  DQN vs ECMP: mean diff = {mean_diff_dqn:.3f}, std = {std_diff_dqn:.4f}, t = {t_dqn_table:.2f} (p < 0.0001)")
print(f"  PPO vs ECMP: mean diff = {mean_diff_ppo:.3f}, std = {std_diff_ppo:.4f}, t = {t_ppo_table:.2f} (p < 0.0001)")

# Paired t-test across 5 random seeds (Burst Traffic):
ecmp_burst = np.array([-54.12, -53.20, -55.80, -53.60, -53.90])
dqn_burst  = np.array([-49.48, -48.10, -51.20, -49.00, -50.10])
ppo_burst  = np.array([-58.52, -57.10, -60.20, -58.00, -59.30])

diff_dqn_b = dqn_burst - ecmp_burst
t_dqn_burst = np.mean(diff_dqn_b) / (np.std(diff_dqn_b, ddof=1) / np.sqrt(5))

diff_ppo_b = ppo_burst - ecmp_burst
t_ppo_burst = np.mean(diff_ppo_b) / (np.std(diff_ppo_b, ddof=1) / np.sqrt(5))

print(f"\nBurst Traffic (Seeds, paired two-tailed t-test, df=4):")
print(f"  DQN vs ECMP: t = {t_dqn_burst:.2f} (p < 0.001)")
print(f"  PPO vs ECMP: t = {t_ppo_burst:.2f} (p < 0.001)")

# Per-step efficiency calculation:
# Under burst traffic:
# Mean episode length before termination / packet drop:
# ECMP: ~1050 steps, total reward = -54.12 -> -54.12 / 1050 = -0.0515
# DQN: ~1380 steps, total reward = -49.48 -> -49.48 / 1380 = -0.0359
# PPO: ~1760 steps, total reward = -58.52 -> -58.52 / 1760 = -0.0333
print(f"\nPer-step rewards:")
print(f"  ECMP: -54.12 / 1050 = {-54.12/1050:.4f}")
print(f"  DQN:  -49.48 / 1380 = {-49.48/1380:.4f}")
print(f"  PPO:  -58.52 / 1760 = {-58.52/1760:.4f}")
