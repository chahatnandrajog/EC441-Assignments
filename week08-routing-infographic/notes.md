## Key Takeaways from Week 8: Routing Algorithms
1. Two fundamentally different approaches

Link-State and Distance Vector solve the same shortest path problem but differ in how information is shared:

Link-State distributes local link information globally
Distance Vector distributes global distance estimates locally

This difference explains why their behavior and performance vary significantly.

2. Why Dijkstra’s Algorithm works

Dijkstra’s algorithm uses a greedy approach by always selecting the node with the smallest known distance. Because all edge weights are non-negative, once a node is finalized, its shortest path cannot be improved later. This guarantees correctness.

3. Why Distance Vector converges slowly

Distance Vector relies on iterative updates between neighbors. While this allows for distributed computation, it also causes delays in propagating changes. When a link fails, routers may continue using outdated information, leading to slow convergence.

4. Count-to-Infinity problem

One major limitation of Distance Vector is the count-to-infinity problem. When a path becomes invalid, routers may repeatedly increase their distance estimates based on incorrect neighbor information, creating routing loops and delayed convergence.

5. Real-world implications
Link-State (OSPF) is used in larger networks because of faster convergence and accuracy
Distance Vector (RIP) is simpler but less scalable due to slower convergence and limitations
6. Key Insight

Both algorithms ultimately aim to compute the shortest path, but:

Link-State prioritizes accuracy and speed
Distance Vector prioritizes simplicity and distributed operation