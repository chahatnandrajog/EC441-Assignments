# Week 11: TCP Lifecycle Visualizer and Congestion Window Graph

## Overview

This artifact models how TCP behaves across the full lifecycle of a connection. Instead of only describing TCP concepts, this project visualizes them step by step, showing how connections are established, how data is transmitted reliably, how packet loss is handled, and how the connection is closed.

The second part of the artifact is a congestion window graph that demonstrates how TCP dynamically adjusts its sending rate over time using slow start, congestion avoidance, and loss recovery mechanisms.

---

## What This Artifact Demonstrates

### 1. Three-Way Handshake
The simulation begins with connection establishment:
- Client sends SYN  
- Server responds with SYN-ACK  
- Client sends ACK  

This ensures both sides are synchronized and ready to communicate.

---

### 2. Reliable Data Transfer
The visualizer shows how:
- TCP uses **byte-based sequence numbers**
- ACKs are **cumulative**
- The receiver always indicates the **next expected byte**

This highlights how TCP ensures ordered and reliable delivery.

---

### 3. Packet Loss and Fast Retransmit
A key part of the artifact is modeling packet loss:
- One segment is intentionally “lost”
- The receiver sends **duplicate ACKs**
- After 3 duplicate ACKs, the sender performs **fast retransmit**

This demonstrates how TCP avoids waiting for a timeout when loss is detected early.

---

### 4. Connection Teardown
The artifact ends with a **graceful close**:
- Client sends FIN  
- Server ACKs  
- Server sends FIN  
- Client sends final ACK  

This also introduces the idea of **TIME_WAIT**, where the connection remains briefly active to handle delayed packets.

---

### 5. Congestion Window Graph

The graph (`cwnd_graph.png`) shows how TCP adjusts its sending rate:

- **Slow Start**: rapid exponential growth at the beginning  
- **Congestion Avoidance**: slower, linear growth  
- **Triple Duplicate ACK**: moderate drop in cwnd  
- **Timeout**: large drop and restart  

This connects the packet-level behavior to overall network performance.

---

## How to Run

Install matplotlib if needed: 

```bash
pip install matplotlib

```
run the visualizer:

python simulator.py

run with graph generation:

python simulator.py --graph

## AI Engagement
AI played a role in helping me design this artifact, but the main goal was to turn lecture concepts into something more interactive and understandable.

I started by thinking about what kind of artifact would actually show how TCP works instead of just explaining it. Since TCP involves a sequence of events like handshakes, acknowledgments, and retransmissions, I decided to build a lifecycle visualizer. AI helped me refine this idea into something structured, where each step clearly represents what is happening between the client and server.

While building the project, I used AI to help organize the code and make sure each part of TCP was represented correctly. This included the handshake process, how sequence numbers increase, how cumulative ACKs work, and how duplicate ACKs trigger fast retransmit. I also used it to verify that the congestion window behavior in the graph matched what we learned in class, including slow start, congestion avoidance, and the effects of packet loss.

One of the most useful aspects of using AI was checking that the artifact stayed aligned with the actual course material rather than becoming too simplified or inaccurate. Instead of just generating answers, it helped me connect the code I was writing back to the underlying networking concepts.

Overall, AI was used as a support tool to guide structure and correctness, but the final artifact reflects my understanding of how TCP behaves across a connection.


