# Deep Reinforcement Learning for Proactive Network Traffic Congestion Control and Load Balancing

## Authors and Affiliations

**Authors:** 
- *Peter Borngreat-Mensah*
- *Henry Asante*
- *Blessing Listowell Issaka*
- *Student IDs: 22424679, 22424186, 22424754 respectively*

**Institution Details:**
- **University:** University of Ghana
- **College:** College of Basic and Applied Sciences
- **Department:** Department of Computer Science
- **Programme:** Master of Science Computer Science (2025/2026)

---

## 1. Abstract & Project Overview

Modern Internet Service Provider (ISP) and enterprise networks suffer from transient micro-bursts and rapidly fluctuating traffic demands. Traditional traffic engineering approaches such as Equal-Cost Multi-Path (ECMP) rely on static, hash-based packet distribution. While computationally simple, these legacy methods are blind to real-time network states. Consequently, they often hash heavy "elephant" flows onto the exact same physical links causing severe bottlenecks, buffer bloat and dropped packets.

This project investigated and implemented an AI-driven solution. It provides the source code, training configurations and experimental data for evaluating Deep Reinforcement Learning (DRL) algorithms (specifically **Deep Q-Network (DQN)** and **Proximal Policy Optimization (PPO)**) for proactive load balancing across wide-area network topologies. The core objective was to train AI agents to dynamically shift flows across candidate paths in real-time thereby minimizing queue congestion and maximizing overall network throughput.

## 2. Methodology

Our approach bridged the gap between software-defined networking (SDN) concepts and advanced machine learning algorithms:

### 2.1 Dataset and Environment
- **Data Source:** We utilized real-world network topologies from the Internet Topology Zoo. The raw GraphML files were sanitized and precomputed to extract the $K$-shortest paths between all node pairs.
- **Gymnasium Environment:** We developed a custom Markov Decision Process (MDP) sandbox (`NetworkCongestionEnv`) that simulated network queues, link capacities and traffic flows. 
- **State Space:** The agents observed a 250-dimensional state vector encompassing current link utilizations (100 features), queue occupancies (100 features) and instantaneous flow demands (50 features). **PCA Analysis** revealed that Queue Occupancy and Link Utilization exhibited significantly more variance in the data distribution than raw Flow Demands, justifying telemetry normalization prior to neural network ingestion.
- **Action Space:** The agent outputted load-balancing weights to distribute active flows across the precomputed $K$-shortest paths. Our analysis illustrated a stark architectural dichotomy: PPO explored a continuous spectrum of routing weights whereas DQN was bound to 10 distinct fractional bins.
- **Reward Function:** A composite, weighted reward function heavily penalized queue overflow (congestion) while rewarding high overall link utilization (throughput).

### 2.2 Deep Reinforcement Learning Algorithms
- **Deep Q-Network (DQN):** An off-policy algorithm that learned the value of discrete load-balancing actions. It utilized a replay buffer and target networks to stabilize the learning of optimal routing policies.
- **Proximal Policy Optimization (PPO):** An on-policy actor-critic algorithm that directly optimized the routing policy gradient. It restricted policy updates to a clipped surrogate objective, preventing catastrophic forgetting and ensuring monotonic improvement. **Policy Entropy Decay tracking** demonstrated PPO's intrinsic stability, transitioning smoothly from random exploration to confident exploitation over 50,000 timesteps.

### 2.3 Experimental Setup
Models were trained across 5 independent random seeds (`42, 100, 2024, 777, 1337`) using an NVIDIA RTX 3060 GPU to ensure statistical rigor. Testing was conducted on strictly *unseen* network topologies under various adversarial traffic profiles: `moderate`, `burst` and `congestion`.

## 3. Comprehensive Findings and Results

Our rigorous experimental suite demonstrated that DRL agents significantly outperformed traditional static heuristics under volatile conditions but faced fundamental physical limits under saturation.

### 3.1 Superior Performance under Moderate Traffic
During moderate traffic scenarios, both DRL agents consistently and cleanly outperformed traditional static heuristics (paired t-tests: DQN $t=136.930, p<0.001$; PPO $t=25.329, p<0.001$). This represented the optimal operating window for AI-driven routing controllers.

### 3.2 Burst Handling and Per-Step Efficiency
During highly variable traffic bursts:
- **Total Reward:** DQN substantially outperformed the ECMP baseline (-49.48 vs -54.12, $t=21.705, p<0.001$), while PPO scored -58.52 in total episodic reward.
- **Per-Step Efficiency:** PPO survived ~1800 steps before packet drops vs DQN's ~1400 steps. On a per-step basis, PPO achieved $-0.0325$/step compared to DQN's $-0.0353$/step, confirming superior per-step efficiency despite cumulative episodic scoring penalizing prolonged survival in lossy settings.

### 3.3 The Saturation Limit (Honest Negative Result)
Under sustained, heavy congestion, the network became fundamentally saturated. DRL performed worse than ECMP under saturation (-80.41 and -80.43 vs -73.78). The fact that DQN and PPO scored almost identically suggests the cause is not the action space. We suspect that continued path-shifting under saturation is counterproductive, but our environment does not model reordering costs, so we cannot confirm this.

### 3.4 Generalization Performance Data

The table below outlines the exact measurements extracted from our simulations. All tests were performed zero-shot on topologies the models were never trained on.

| Agent | Traffic Mode | Mean Utilization | Congestion Penalty | Overall Reward |
|-------|--------------|------------------|--------------------|----------------|
| ECMP  | moderate     | 92.44%          | 0.330              | -67.70         |
| DQN   | moderate     | 88.27%          | 0.279              | -60.84         |
| PPO   | moderate     | 92.58%          | 0.294              | -64.65         |
| ECMP  | burst        | 81.31%          | 0.254              | -54.12         |
| DQN   | burst        | 75.27%          | 0.210              | -49.48         |
| PPO   | burst        | 83.32%          | 0.223              | -58.52         |
| ECMP  | congestion   | 99.84%          | 0.243              | -73.78         |
| DQN   | congestion   | 99.59%          | 0.394              | -80.41         |
| PPO   | congestion   | 99.49%          | 0.408              | -80.43         |

*(Metrics extracted directly from `results/generalization.csv` across evaluation episodes per condition).*

## 4. Repository Structure

- `configs/`: Hyperparameter settings for DQN, PPO, the reward function and topology splits.
- `data/processed/`: Normalized GraphML graphs and precomputed k-shortest paths from the Internet Topology Zoo.
- `models/`: Frozen checkpoints of the trained DQN and PPO neural networks (.zip).
- `results/`: Output CSVs and comprehensive high-resolution visualization plots (`results/plots/`).
- `src/agents/`: Training scripts and implementations of the DRL algorithms using Stable-Baselines3.
- `src/baselines/`: The static ECMP implementation for benchmark comparisons.
- `src/environment/`: The core Gymnasium-compatible Markov Decision Process sandbox.
- `src/traffic/`: Procedural traffic generation module (normal, moderate, burst, congestion).
- `src/evaluation/`: Scripts to run zero-shot generalization testing and plot the raw data.
- `generate_v3_stats_and_plots.py`: Script to generate updated accessible plots and statistical tests.
- `create_presentation.py`: Generates the final 10-slide PowerPoint presentation with presenter notes.

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
   python generate_v3_stats_and_plots.py
   python create_presentation.py
   ```

## Academic Integrity Statement

Every numerical result, graph and table located in the `results/` folder originates directly from an executed Python runtime. No simulated data points have been fabricated. Code relies exclusively on the `stable-baselines3`, `networkx` and `gymnasium` frameworks.
