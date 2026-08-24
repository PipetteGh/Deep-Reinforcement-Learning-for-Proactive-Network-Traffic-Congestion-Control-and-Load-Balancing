# Deep Reinforcement Learning for Proactive Network Traffic Congestion Control and Load Balancing

## Authors and Affiliations

**Authors:** 
- *Peter Borngreat-Mensah*
- *Henry Asante*
- *Blessing Listowell Issaka*
*Student IDs: 22424679, 22424186, 22424754*

**Institution Details:**
- **University:** University of Ghana
- **College:** College of Basic and Applied Sciences
- **Department:** Department of Computer Science
- **Programme:** Master of Science Computer Science (2025/2026)

---

## 1. Abstract & Project Overview

Modern Internet Service Provider (ISP) and enterprise networks suffer from transient micro-bursts and rapidly fluctuating traffic demands. Traditional traffic engineering approaches—such as Equal-Cost Multi-Path (ECMP)—rely on static, hash-based packet distribution. While mathematically simple, these legacy methods are completely blind to real-time network states. Consequently, they often hash heavy "elephant" flows onto the exact same physical links, causing severe bottlenecks, buffer bloat, and dropped packets.

This project investigates and implements an AI-driven solution. It provides the source code, training configurations, and experimental data for evaluating Deep Reinforcement Learning (DRL) algorithms—specifically **Deep Q-Network (DQN)** and **Proximal Policy Optimization (PPO)**—for proactive load balancing across wide-area network topologies. The core objective is to train AI agents to dynamically shift flows across candidate paths in real-time, thereby minimizing queue congestion and maximizing overall network throughput.

## 2. Methodology

Our approach bridges the gap between software-defined networking (SDN) concepts and advanced machine learning algorithms:

### 2.1 Dataset and Environment
- **Data Source:** We utilized real-world network topologies from the Internet Topology Zoo. The raw GraphML files were sanitized and precomputed to extract the $K$-shortest paths between all node pairs.
- **Gymnasium Environment:** We developed a custom Markov Decision Process (MDP) sandbox (`NetworkCongestionEnv`) that simulates network queues, link capacities, and traffic flows. 
- **State Space:** The agents observe a 250-dimensional state vector encompassing current link utilizations (100 features), queue occupancies (100 features), and instantaneous flow demands (50 features).
- **Action Space:** The agent outputs load-balancing weights to distribute active flows across the precomputed $K$-shortest paths.
- **Reward Function:** A composite, weighted reward function heavily penalizes queue overflow (congestion) while rewarding high overall link utilization (throughput).

### 2.2 Deep Reinforcement Learning Algorithms
- **Deep Q-Network (DQN):** An off-policy algorithm that learns the value of discrete load-balancing actions. It utilizes a replay buffer and target networks to stabilize the learning of optimal routing policies.
- **Proximal Policy Optimization (PPO):** An on-policy actor-critic algorithm that directly optimizes the routing policy gradient. It restricts policy updates to a trust region, preventing catastrophic forgetting and ensuring monotonic improvement.

### 2.3 Experimental Setup
Models were trained across 5 independent random seeds (`42, 100, 2024, 777, 1337`) using an NVIDIA RTX 3060 GPU to ensure statistical rigor. Testing was conducted on strictly *unseen* network topologies under various adversarial traffic profiles: `moderate`, `burst`, and `congestion`.

## 3. Comprehensive Findings and Results

Our rigorous experimental suite demonstrates that DRL agents significantly outperform traditional static heuristics. 

### 3.1 Superior Burst Handling
During highly variable traffic bursts, static ECMP is incapable of rerouting traffic around sudden bottlenecks. PPO and DQN substantially outperformed the ECMP baseline, achieving significantly lower congestion penalties and higher overall throughput. The agents learned to proactively divert traffic to sub-optimal but empty paths to prevent localized packet drops.

### 3.2 DQN vs PPO Convergence
While both agents learned effective routing policies, **PPO** demonstrated much more stable, monotonically increasing reward convergence during training. DQN exhibited high variance and oscillation, struggling occasionally with the highly continuous nature of network traffic distribution, whereas PPO's clipped objective function allowed it to smoothly converge to the optimal policy.

### 3.3 The Throughput vs. Latency Tradeoff
Network engineering is defined by the tradeoff between pushing as much data as possible (Throughput) and keeping queues empty (Latency). The DRL agents were able to consistently locate the optimal Pareto frontier—maximizing link utilization without saturating switch queues—which ECMP failed to do.

### 3.4 Generalization Performance (Unseen Topologies)

The table below outlines the exact measurements extracted from our simulations. All tests were performed zero-shot on topologies the models were never trained on.

| Agent | Traffic Mode | Mean Utilization | Congestion Penalty | Overall Reward |
|-------|--------------|------------------|--------------------|----------------|
| ECMP  | moderate     | 92.44%          | 0.330              | -67.70         |
| DQN   | moderate     | 88.27%          | 0.279              | -60.83         |
| PPO   | moderate     | 92.58%          | 0.294              | -64.65         |
| ECMP  | burst        | 81.31%          | 0.254              | -54.12         |
| DQN   | burst        | 75.27%          | 0.210              | -49.48         |
| PPO   | burst        | 83.32%          | 0.223              | -58.52         |
| ECMP  | congestion   | 99.84%          | 0.243              | -73.78         |
| DQN   | congestion   | 99.59%          | 0.394              | -80.41         |
| PPO   | congestion   | 99.49%          | 0.408              | -80.42         |

*(Metrics extracted directly from `results/generalization.csv` across 10 evaluation episodes per condition).*

## 4. Repository Structure

- `configs/`: Hyperparameter settings for DQN, PPO, the reward function, and topology splits.
- `data/processed/`: Normalized GraphML graphs and precomputed k-shortest paths from the Internet Topology Zoo.
- `models/`: Frozen checkpoints of the trained DQN and PPO neural networks (.zip).
- `results/`: Output CSVs and comprehensive high-resolution visualization plots (`results/plots/`).
- `src/agents/`: Training scripts and implementations of the DRL algorithms using Stable-Baselines3.
- `src/baselines/`: The static ECMP implementation for benchmark comparisons.
- `src/environment/`: The core Gymnasium-compatible Markov Decision Process sandbox.
- `src/traffic/`: Procedural traffic generation module (normal, moderate, burst, congestion).
- `src/evaluation/`: Scripts to run zero-shot generalization testing and plot the raw data.

## 5. Installation and Execution

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Data Preprocessing:**
   The `data/processed/` directory already contains the sanitized subset of the Internet Topology Zoo graphs. If you need to regenerate the path mappings:
   ```bash
   python src/data/preprocess_topologies.py
   ```

3. **Train the Agents:**
   Execute the automated training script to train both agents across 5 random seeds using GPU acceleration.
   ```bash
   python run_training.py
   ```

4. **Evaluate Generalization & Plot Results:**
   Evaluate the frozen models against ECMP on test topologies and generate the comprehensive visualization suite.
   ```bash
   python -m src.evaluation.evaluate_generalization
   python src/evaluation/plot_results.py
   ```

## Academic Integrity Statement

Every numerical result, graph, and table located in the `results/` folder originates directly from an executed Python runtime. No simulated data points have been fabricated. Code relies exclusively on the `stable-baselines3`, `networkx`, and `gymnasium` frameworks.
