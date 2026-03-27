## Artifact: Shortest Path Routing Infographic

This week’s artifact is a visual infographic comparing two core routing algorithms: Link-State (Dijkstra) and Distance Vector (Bellman-Ford). The goal of the infographic is to represent how routers compute shortest paths in a network using both approaches, while keeping the explanation intuitive and visually structured.

The infographic highlights:

- how each algorithm works step-by-step
- the type of information each router has (global vs local)
- how shortest paths are computed and used to build forwarding tables
- key differences in convergence speed, communication, and scalability
- real-world protocol implementations such as OSPF and RIP

It also includes insight sections explaining why each algorithm works, along with a visualization of the count-to-infinity problem to demonstrate limitations of distance-vector routing.

## AI Usage and Engagement

I used ChatGPT (GPT-5.3) to help generate and refine this infographic, focusing on both structure and clarity.

My process involved multiple stages of prompting and refinement:

- I first prompted for a comparison of Dijkstra vs Distance Vector algorithms to understand how to structure the content.
- I then asked for a mindmap-style infographic layout instead of a report, since I wanted a more visual artifact.
- After generating an initial version, I refined my prompts to:
    - simplify explanations into concise, visual-friendly steps
    - include deeper conceptual insights (such as why the algorithms work)
    - add limitations like the count-to-infinity problem
    - ensure the content aligned with lecture material from Week 8

Rather than directly using the first output, I iterated on prompts to improve:

- clarity (removing unnecessary text)
- depth (adding reasoning and behavior over time)
- structure (organizing content into sections like comparison, insights, and examples)

I reviewed the final output against lecture notes to ensure accuracy and made adjustments to keep the explanations precise and aligned with course concepts.

## Reflection

This process helped me better understand the core difference between link-state and distance-vector routing beyond just memorizing steps. In particular, visualizing how information spreads through the network made concepts like convergence and routing loops easier to grasp.