import collections
import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    
    # Slide 1: Title
    slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Deep Reinforcement Learning for Proactive Network Traffic Congestion Control"
    subtitle.text = "Authors: Peter Borngreat-Mensah, Henry Asante, Blessing Listowell Issaka\nMSc Computer Science, Cohort B, University of Ghana"
    
    # Slide 2: Problem Statement
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "The Problem: Static Routing & Micro-Bursts"
    content = slide.placeholders[1]
    content.text = ("- Wide-area networks experience heavy volatility and micro-bursts.\n"
                    "- Traditional Equal-Cost Multi-Path (ECMP) relies on static hashing.\n"
                    "- ECMP is blind to real-time telemetry.\n"
                    "- Result: 'Elephant flows' collide on the same bottleneck links causing buffer bloat and packet loss.")
                    
    # Slide 3: Research Objectives
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Research Objectives"
    content = slide.placeholders[1]
    content.text = ("1. Evaluate Deep Reinforcement Learning (DQN, PPO) against ECMP.\n"
                    "2. Implement intelligent agents within an SDN framework.\n"
                    "3. Critically test Zero-Shot Generalization on unseen topologies.\n"
                    "4. Discover the limitations of AI routing under heavy network saturation.")

    # Slide 4: Methodology - Environment
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Methodology: Gymnasium Environment"
    content = slide.placeholders[1]
    content.text = ("- Dataset: Internet Topology Zoo (Real ISP graphs).\n"
                    "- Train/Test Split: Trained on 20 topologies, tested on 5 completely unseen topologies.\n"
                    "- Preprocessing: Yen's K-Shortest Paths algorithm to constrain the routing action space.\n"
                    "- Frameworks: Gymnasium & Stable-Baselines3.")
                    
    # Slide 5: Methodology - MDP
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Methodology: MDP Formulation"
    content = slide.placeholders[1]
    content.text = ("- State Space (250 features): Top 100 link utilizations (zero-padded), Top 100 queue depths, 50 flow demands.\n"
                    "- Action Space: PPO uses continuous weights; DQN discretized into 10 bins.\n"
                    "- Reward: R = 1.0 * U_mean - 10.0 * P_congestion - 5.0 * D_packet\n"
                    "- Strongly penalizes congestion and dropped packets.")

    # Slide 6: Key Findings - Burst Traffic
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Key Findings: Burst Traffic Superiority"
    content = slide.placeholders[1]
    content.text = ("- Under unpredictable flash crowds and micro-bursts, DRL dominates.\n"
                    "- ECMP fails because static hashing cannot adapt to sudden asymmetric loads.\n"
                    "- PPO and DQN agents actively monitor queue depths and divert traffic to sub-optimal, empty paths to preserve health.")

    # Slide 7: Key Findings - The Saturation Limit
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Key Findings: The Limits of Routing"
    content = slide.placeholders[1]
    content.text = ("- Under sustained, extreme congestion, DRL fails to outperform ECMP.\n"
                    "- This is an honest, mathematically bounded negative result.\n"
                    "- When total demand exceeds physical link capacity, the network saturates.\n"
                    "- AI cannot magically create bandwidth; admission control is required.")

    # Slide 8: Algorithmic Comparison
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "DQN vs PPO Convergence"
    content = slide.placeholders[1]
    content.text = ("- PPO (Continuous, On-Policy): Exhibited highly stable learning with smooth policy loss decay due to clipped objective gradients.\n"
                    "- DQN (Discrete, Off-Policy): Exhibited higher variance and moving target instability.\n"
                    "- Both fundamentally collapsed under extreme congestion, proving the failure mode is environmental, not algorithmic.")

    # Slide 9: Statistical Variance
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Variance and Predictability"
    content = slide.placeholders[1]
    content.text = ("- ECMP guarantees a tight, highly predictable statistical distribution of performance.\n"
                    "- DRL agents trade this predictability for dynamic reaction capabilities, resulting in a wider variance of congestion penalties.\n"
                    "- Trained across 5 distinct random seeds to ensure statistical rigor.")
                    
    # Slide 10: Conclusion
    slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(slide_layout)
    title = slide.shapes.title
    title.text = "Conclusion & Future Work"
    content = slide.placeholders[1]
    content.text = ("- DRL (specifically PPO) is a highly viable alternative for proactive load balancing during micro-bursts.\n"
                    "- True zero-shot generalization across networks is achievable via topological state vector padding.\n"
                    "- Future Work: Coupling DRL routing with dynamic admission control to prevent catastrophic saturation.")

    prs.save('final_presentation.pptx')
    print("final_presentation.pptx created successfully.")

if __name__ == '__main__':
    create_presentation()
