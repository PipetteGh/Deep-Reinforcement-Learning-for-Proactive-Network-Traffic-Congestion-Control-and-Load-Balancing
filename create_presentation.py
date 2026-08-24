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
    slide.notes_slide.notes_text_frame.text = "Welcome the audience. Introduce yourselves and state that this research tackles one of the most pressing issues in modern ISP networks: transient traffic micro-bursts and the limitations of static routing."
    
    # --- Slide 2: Problem Statement ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "The Problem: Static Routing & Micro-Bursts"
    slide.placeholders[1].text = (
        "- Wide-area networks experience heavy volatility.\n"
        "- Equal-Cost Multi-Path (ECMP) relies on static hashing.\n"
        "- ECMP is blind to real-time telemetry.\n"
        "- 'Elephant flows' collide on bottleneck links."
    )
    slide.notes_slide.notes_text_frame.text = "Explain that traditional ECMP doesn't look at how full a link is; it just blindly hashes packets. When a massive data flow (elephant flow) hits, ECMP can accidentally send it down an already congested path, causing dropped packets."

    # --- Slide 3: Research Objectives ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Research Objectives"
    slide.placeholders[1].text = (
        "1. Evaluate Deep Reinforcement Learning (DQN, PPO).\n"
        "2. Implement intelligent agents within an SDN framework.\n"
        "3. Critically test Zero-Shot Generalization on unseen topologies.\n"
        "4. Discover limitations under heavy network saturation."
    )
    slide.notes_slide.notes_text_frame.text = "Our goal wasn't just to see if AI works, but to push it to its breaking point. We specifically wanted to see if an agent trained on one network could magically route traffic on a completely different, unseen network (zero-shot generalization)."

    # --- Slide 4: Methodology - State Space & Features ---
    slide = prs.slides.add_slide(prs.slide_layouts[5]) # Title only
    slide.shapes.title.text = "Methodology: State Space & PCA Features"
    # Add text
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
    tf = txBox.text_frame
    tf.text = "- 250-dimensional continuous vector.\n- Top 100 links (utilization).\n- Top 100 queues.\n- 50 Flow Demands.\n- Topologies < 100 links are zero-padded."
    # Add Image
    try:
        slide.shapes.add_picture('results/plots/feature_importance.png', Inches(4.5), Inches(2.0), width=Inches(5))
    except Exception as e:
        print(f"Skipped image: {e}")
    slide.notes_slide.notes_text_frame.text = "Point to the graph. Explain that the neural network learns to prioritize Queue Occupancy and Link Utilization over raw flow demands. The zero-padding allows the same 250-feature neural network to accept any topology size."

    # --- Slide 5: Methodology - Action Space ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Methodology: Continuous vs Discrete Actions"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
    tf = txBox.text_frame
    tf.text = "- PPO: Continuous probability spectrum.\n- DQN: Rigid 10-bin discrete choices.\n- Reward penalizes congestion and drops."
    try:
        slide.shapes.add_picture('results/plots/action_space_dist.png', Inches(4.5), Inches(2.0), width=Inches(5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Show how DQN's actions (in red) are locked into 10 rigid bars, whereas PPO (in blue) can output any fine-tuned routing weight, allowing for much smoother traffic engineering."

    # --- Slide 6: Key Findings - Burst Traffic Superiority ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Key Findings: Burst Traffic"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(2))
    tf = txBox.text_frame
    tf.text = "- Under sudden micro-bursts, DRL dominates.\n- ECMP fails to adapt dynamically."
    # --- Slide 5: Performance Under Moderate Traffic ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Superior Performance under Moderate Traffic"
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5))
    tf = txBox.text_frame
    tf.text = "Optimal Operating Window:"
    p = tf.add_paragraph()
    p.text = "- Under moderate traffic conditions, both DQN and PPO consistently outperformed traditional ECMP."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "- Achieved lower congestion penalties and higher overall throughput."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "- The models learned to proactively divert traffic to sub-optimal but empty paths."
    p.level = 1

    slide.shapes.add_picture("results/plots/burst_performance_bar.png", Inches(5), Inches(1.5), width=Inches(4.5))

    notes = slide.notes_slide.notes_text_frame
    notes.text = "In this slide, we focus on our primary success: moderate traffic. This is the optimal operating window for our models where they both clearly beat ECMP. As you can see from the plot, the agents learn to route around early congestion."

    # Slide 6: Burst Limitations
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Burst Traffic Limitations"
    
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4.5), Inches(5))
    tf = txBox.text_frame
    tf.text = "DQN vs PPO under Burst:"
    p = tf.add_paragraph()
    p.text = "- DQN successfully beat ECMP, finding stable routes around bottlenecks."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "- PPO failed to outperform ECMP."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "- While PPO survived longer in episodes, its reward per step was worse."
    p.level = 1

    slide.shapes.add_picture("results/plots/episode_length.png", Inches(5), Inches(1.5), width=Inches(4.5))

    notes = slide.notes_slide.notes_text_frame
    notes.text = "Under extreme burst traffic, DQN handled the volatility well, but PPO did not. Even though PPO survives for more timesteps before failing, its overall efficiency per step drops below the ECMP baseline."

    # --- Slide 7: Key Findings - The Saturation Limit ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "The Saturation Limit (Honest Negative Result)"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
    tf = txBox.text_frame
    tf.text = "- Extreme congestion mathematically saturates the network.\n- No routing policy can create bandwidth.\n- DRL performs identically/worse than ECMP here."
    try:
        slide.shapes.add_picture('results/plots/throughput_vs_latency.png', Inches(4.5), Inches(2.0), width=Inches(5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "This is our most critical academic finding. Look at the square markers on the scatter plot. Under extreme congestion, DRL fails to beat ECMP. Why? Because the network is physically full. Constantly shifting traffic just causes packet reordering overhead. This proves we need admission control."

    # --- Slide 8: Zero-Shot Generalization ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Zero-Shot Generalization vs Network Size"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
    tf = txBox.text_frame
    tf.text = "- Agents tested on 5 UNSEEN Topologies.\n- Performance decays naturally as nodes increase.\n- PPO maintains superior trajectory over DQN."
    try:
        slide.shapes.add_picture('results/plots/topology_scaling.png', Inches(4.5), Inches(2.0), width=Inches(5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "We threw the agents into completely unseen networks ranging up to 100 nodes. As expected, bigger networks are harder to route, so reward drops. But notice how PPO (the blue line) consistently stays above DQN (the red line), proving robust zero-shot transfer."

    # --- Slide 9: Statistical Variance ---
    slide = prs.slides.add_slide(prs.slide_layouts[5])
    slide.shapes.title.text = "Variance and Predictability"
    txBox = slide.shapes.add_textbox(Inches(0.5), Inches(1.5), Inches(4), Inches(4))
    tf = txBox.text_frame
    tf.text = "- ECMP provides narrow, predictable variance.\n- DRL trades predictability for aggressive reaction to bursts."
    try:
        slide.shapes.add_picture('results/plots/congestion_violin.png', Inches(4.5), Inches(2.0), width=Inches(5))
    except Exception as e:
        pass
    slide.notes_slide.notes_text_frame.text = "Look at the violin plots. ECMP is tight and narrow (predictable but mediocre). The DRL agents have wider bodies and long tails—they are aggressively hunting for better paths, which creates higher variance but much better burst mitigation."
    
    # --- Slide 10: Conclusion & Future Work ---
    slide = prs.slides.add_slide(prs.slide_layouts[1])
    slide.shapes.title.text = "Conclusion & Future Work"
    slide.placeholders[1].text = (
        "- DRL (specifically PPO) is highly viable for proactive micro-burst load balancing.\n"
        "- Zero-shot generalization is achievable via topological state vector zero-padding.\n"
        "- DRL cannot solve absolute network saturation.\n"
        "- Future Work: Coupling DRL routing with dynamic admission control."
    )
    slide.notes_slide.notes_text_frame.text = "Wrap up the presentation. Conclude that AI is amazing for transient bursts, but it cannot bend the laws of physics when a network is 100% full. Thank the audience and ask for questions."

    prs.save('final_presentation.pptx')
    print("final_presentation.pptx with images and notes created successfully.")

if __name__ == '__main__':
    create_presentation()
