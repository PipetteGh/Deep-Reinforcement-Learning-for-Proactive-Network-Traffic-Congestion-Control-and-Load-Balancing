import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # --- Slide 1: Title ---
    slide = prs.slides.add_slide(prs.slide_layouts[0])
    slide.shapes.title.text = "Deep Reinforcement Learning for Proactive Network Traffic Congestion Control"
    slide.placeholders[1].text = "Authors: Peter Borngreat-Mensah, Henry Asante, Blessing Listowell Issaka\nMSc Computer Science, Cohort B, University of Ghana"
    slide.notes_slide.notes_text_frame.text = "Welcome the audience and supervisor. Introduce the topic: evaluating Deep Reinforcement Learning for proactive network load balancing and congestion avoidance across wide-area ISP networks."
    
    # --- Slide 2: Problem Statement ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "The Problem: Static Routing & Micro-Bursts"
    slide.placeholders[1].text = (
        "- Wide-area networks experience heavy volatility and sudden micro-bursts.\n"
        "- Equal-Cost Multi-Path (ECMP) relies on static packet header hashing.\n"
        "- ECMP is stateless and blind to real-time link queue telemetry.\n"
        "- Hash collisions map heavy 'elephant flows' onto the same bottleneck links."
    )
    slide.notes_slide.notes_text_frame.text = "Explain that traditional ECMP doesn't look at how full a link is; it just hashes packet headers. When massive elephant flows collide, it causes severe bottlenecks and buffer overflows."

    # --- Slide 3: Research Objectives ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Research Objectives"
    slide.placeholders[1].text = (
        "1. Evaluate Deep Reinforcement Learning (DQN and PPO) for proactive load balancing.\n"
        "2. Implement intelligent agents within a Software-Defined Network (SDN) framework.\n"
        "3. Evaluate Zero-Shot Generalization on 5 completely unseen ISP topologies.\n"
        "4. Uncover physical operating limits under sustained network saturation."
    )
    slide.notes_slide.notes_text_frame.text = "State our core goals: comparing value-based DQN vs policy-gradient PPO against ECMP, testing true zero-shot transferability across topologies, and identifying the physical boundaries of DRL routing."

    # --- Slide 4: Methodology - State Space & Features ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Methodology: State Space & PCA Variance"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "MDP State Representation:"
    p = tf.add_paragraph()
    p.text = "- 250-dimensional continuous telemetry vector.\n- Top 100 links (utilization ratio).\n- Top 100 queues (buffer occupancy).\n- 50 Flow Demands.\n- Deterministic zero-padding for topologies with < 100 links."
    p = tf.add_paragraph()
    p.text = "- PCA confirmed highest variance in Queue and Link states, motivating feature normalization."
    try:
        slide.shapes.add_picture('results/plots/feature_importance.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        print(f"Skipped image: {e}")
    slide.notes_slide.notes_text_frame.text = "Explain that the 250-feature state vector captures real-time link and buffer utilization. Zero-padding allows the policy network to ingest any topology shape without retraining."

    # --- Slide 5: Methodology - Action Space Dichotomy ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Methodology: Continuous vs Discrete Actions"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "Action Space Architecture:"
    p = tf.add_paragraph()
    p.text = "- PPO: Explores a fully continuous probability distribution over routing paths.\n- DQN: Bound to 10 discrete routing bins.\n- Reward Function: Penalizes queue congestion and packet drops while rewarding balanced utilization."
    try:
        slide.shapes.add_picture('results/plots/action_space_dist.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Highlight the design dichotomy: PPO outputs fine-grained continuous routing probabilities across K-shortest paths, whereas DQN chooses from 10 discrete fractions."

    # --- Slide 6: Moderate Traffic Performance ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Primary Success: Moderate Traffic Regime"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "Optimal Operating Window:"
    p = tf.add_paragraph()
    p.text = "- Moderate traffic is where BOTH DRL agents cleanly outperform ECMP.\n- DQN achieved -60.84 and PPO achieved -64.65 vs ECMP's -67.70 (both p < 0.001).\n- DQN maintained lower median link utilization (0.88 vs 0.92) by proactively leveraging secondary paths."
    try:
        slide.shapes.add_picture('results/plots/utilization_boxplot.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Point to the boxplot. Moderate traffic represents the sweet spot for DRL. DQN and PPO both achieve statistically significant improvements over ECMP by balancing loads across empty backup paths."

    # --- Slide 7: Burst Traffic & Per-Step Efficiency ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Burst Traffic & Per-Step Efficiency"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "Episode vs Per-Step Dynamics:"
    p = tf.add_paragraph()
    p.text = "- Total Reward: DQN (-49.48) beat ECMP (-54.12), while PPO scored -58.52.\n- Survival Time: PPO survived ~1800 steps before packet drops vs DQN's ~1400 steps.\n- Per-Step Efficiency: PPO achieved -0.0325/step vs DQN's -0.0353/step.\n- Cumulative scoring penalizes PPO simply for surviving longer in lossy settings."
    try:
        slide.shapes.add_picture('results/plots/burst_performance_bar.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Explain the crucial insight from our review: PPO survived ~1800 steps vs DQN's ~1400, achieving higher per-step reward (-0.0325 vs -0.0353). Cumulative episodic totals penalize it simply because it lasted longer in a hostile environment."

    # --- Slide 8: The Saturation Limit (Honest Negative Result) ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "The Saturation Limit (Honest Negative Result)"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "Physical Capacity Boundaries:"
    p = tf.add_paragraph()
    p.text = "- Under heavy congestion, all links reach 100% capacity.\n- DRL performed worse than ECMP (-80.41 vs -73.78).\n- Continued path-shifting under saturation creates counterproductive routing churn.\n- No routing algorithm can create bandwidth when total demand exceeds topology capacity."
    try:
        slide.shapes.add_picture('results/plots/throughput_vs_latency.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Discuss our honest negative result: When every link in the network is completely saturated, DRL cannot route around bottlenecks because no spare capacity exists. Path churning under saturation leads to extra penalties."

    # --- Slide 9: Robustness & Zero-Shot Transfer ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Zero-Shot Generalization & Robustness"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(4.5))
    tf = txBox.text_frame
    tf.text = "Generalization on 5 Unseen Topologies:"
    p = tf.add_paragraph()
    p.text = "- Evaluated on Abilene, Janetbackbone, Bellcanada, Colt, and Renater2001.\n- DQN consistently outperformed ECMP across all 5 held-out topologies under moderate traffic.\n- Single-palette reward matrix shows consistent performance gradients across traffic stress tests."
    try:
        slide.shapes.add_picture('results/plots/reward_heatmap.png', Inches(5.0), Inches(1.5), width=Inches(4.5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Show the reward heatmap across the traffic scenarios. Our zero-shot evaluation on 5 completely unseen topologies confirms that the learned policies successfully transfer to new network topologies."

    # --- Slide 10: Conclusion & Future Work ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Conclusions & Recommendations"
    slide.placeholders[1].text = (
        "- DRL is highly effective for proactive load balancing under Moderate traffic (both DQN and PPO win) and Burst traffic (DQN wins).\n"
        "- PPO demonstrates superior per-step efficiency and prolonged survival.\n"
        "- Zero-shot topological generalization is viable via standardized telemetry zero-padding.\n"
        "- DRL routing cannot solve fundamental network saturation without admission control.\n"
        "- Recommendation: Combine DRL routing with dynamic rate limiting and admission control."
    )
    slide.notes_slide.notes_text_frame.text = "Conclude the presentation. Summarize key takeaways: DRL shines under moderate and burst conditions, per-step metrics provide deeper clarity than raw episode totals, and admission control is essential for saturation. Thank the committee and invite questions."

    prs.save('final_presentation.pptx')
    print("final_presentation.pptx successfully created with 10 slides, presenter notes, and updated visuals.")

if __name__ == '__main__':
    create_presentation()
