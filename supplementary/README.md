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

Modern Internet Service Provider (ISP) and enterprise networks suffer from transient micro-bursts and rapidly fluctuating traffic demands. Traditional traffic engineering approaches such as Equal-Cost Multi-Path (ECMP, RFC 2992) rely on static, hash-based packet distribution. While computationally simple, these legacy methods are blind to real-time network states. Consequently, they often hash heavy "elephant" flows onto the exact same physical links causing severe bottlenecks, buffer bloat and dropped packets.

This project investigated and implemented an AI-driven solution. It provides the source code, training configurations and experimental data for evaluating Deep Reinforcement Learning (DRL) algorithms (specifically **Deep Q-Network (DQN)** and **Proximal Policy Optimization (PPO)**) for proactive load balancing across wide-area network topologies. The core objective was to train AI agents to dynamically shift flows across candidate paths in real-time thereby minimizing queue congestion and maximizing overall network throughput.

## 2. Methodology

Our approach bridged the gap between software-defined networking (SDN) concepts and advanced machine learning algorithms:

### 2.1 Dataset and Environment
- **Data Source:** We utilized real-world network topologies from the Internet Topology Zoo. The raw GraphML files were sanitized and precomputed to extract the $K$-shortest paths between all node pairs.
- **Topology Partitioning (Zero Overlap):** Agents were trained on 20 distinct topologies (`AsnetAm`, `Bellsouth`, `BeyondTheNetwork`, `CrlNetworkServices`, `Evolink`, `Garr200004`, `Janetlense`, `NetworkUsa`, `Nextgen`, `Roedunet`, `Vinaren`, etc.) and evaluated zero-shot on 5 completely unseen, held-out topologies (`Abilene`, `Janetbackbone`, `Bellcanada`, `Colt`, `Renater2001`).
- **Gymnasium Environment:** We developed a custom Markov Decision Process (MDP) sandbox (`NetworkCongestionEnv`) that simulated network queues, link capacities and traffic flows. 
- **State Space:** The agents observed a 250-dimensional state vector encompassing current link utilizations (100 features), queue occupancies (100 features) and instantaneous flow demands (50 features). **PCA Analysis** revealed that Queue Occupancy and Link Utilization exhibited significantly more variance in the data distribution than raw Flow Demands, justifying telemetry normalization prior to neural network ingestion.
- **Action Space:** The agent outputted load-balancing weights to distribute active flows across the precomputed $K$-shortest paths. Our analysis illustrated a stark architectural dichotomy: PPO explored a continuous spectrum of routing weights whereas DQN was bound to 10 distinct fractional bins.
- **Reward Function:** A composite, weighted reward function heavily penalized queue overflow (congestion) while rewarding high overall link utilization (throughput).

### 2.2 Deep Reinforcement Learning Algorithms
- **Deep Q-Network (DQN):** An off-policy algorithm that learned the value of discrete load-balancing actions. It utilized a replay buffer and target networks to stabilize the learning of optimal routing policies.
- **Proximal Policy Optimization (PPO):** An on-policy actor-critic algorithm that directly optimized the routing policy gradient. It restricted policy updates via a clipped surrogate objective, approximating a trust-region constraint to discourage destructively large policy updates during training.

### 2.3 Experimental Setup
Models were trained across 5 independent random seeds (`42, 100, 2024, 777, 1337`) using an NVIDIA RTX 3060 GPU to ensure statistical rigor. Testing was conducted on strictly *unseen* network topologies under various adversarial traffic profiles: `moderate`, `burst` and `congestion`.

## 3. Comprehensive Findings and Results

Our rigorous experimental suite demonstrated that DRL agents significantly outperformed traditional static heuristics under volatile conditions but faced fundamental physical limits under saturation.

### 3.1 Superior Performance under Moderate Traffic
During moderate traffic scenarios, both DRL agents consistently and cleanly outperformed traditional static heuristics. A paired two-tailed t-test ($df = 4$) across the 5 held-out topologies confirmed statistically significant superiority for both DQN ($t = 151.32, p < 0.0001$) and PPO ($t = 76.49, p < 0.0001$) over ECMP. This represented the optimal operating window for AI-driven routing controllers.

### 3.2 Burst Handling and Per-Step Efficiency
During highly variable traffic bursts:
- **Cumulative Episode Reward:** DQN substantially outperformed the ECMP baseline (-49.48 vs -54.12, paired t-test across 5 seeds: $t=21.71, p<0.001$), while PPO scored -58.52.
- **Survival Length:** PPO survived an average of 1760 steps before packet drops vs DQN's 1380 steps and ECMP's 1050 steps.
- **Per-Step Efficiency:** On a per-step basis, PPO achieved $-0.0333$/step, outperforming DQN ($-0.0359$/step) and ECMP ($-0.0515$/step). This demonstrates that PPO achieved the highest per-step routing efficiency, but cumulative episode summation penalized it simply for surviving longer in a lossy environment.

### 3.3 The Saturation Limit (Honest Negative Result)
Under sustained, heavy congestion, the network became fundamentally saturated. DRL performed worse than ECMP under saturation (-80.41 and -80.43 vs -73.78). The fact that DQN and PPO scored almost identically suggests the cause is not the action space. We suspect that continued path-shifting under saturation is counterproductive, but our environment does not model reordering costs, so we cannot confirm this.

### 3.4 Zero-Shot Generalization Performance Data

The table below outlines the exact measurements extracted from our simulations across the 5 unseen held-out topologies under moderate traffic:

| Topology | ECMP | DQN | PPO |
|---|---|---|---|
| Abilene | -66.12 | **-59.40** | -63.15 |
| Janetbackbone | -67.85 | **-61.02** | -64.80 |
| Bellcanada | -68.40 | **-61.55** | -65.20 |
| Colt | -67.10 | **-60.10** | -64.10 |
| Renater2001 | -69.03 | **-62.14** | -66.00 |
| **Mean** | -67.70 | **-60.84** | -64.65 |

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
