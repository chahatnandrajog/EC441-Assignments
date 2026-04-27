# Week 09: Packet Journey Simulator

## Topic

IPv4, ICMP, NAT, fragmentation, Path MTU Discovery, and IPv6 comparison.

## Artifact Type

Lab: code-based exploration

## What this project does

This Python simulator models the journey of an IP packet as it moves across a small network path. Instead of only defining terms, the simulation shows how several network-layer concepts interact during forwarding.

The simulator demonstrates:

1. IPv4 packet fields such as source IP, destination IP, protocol, TTL, and total length
2. TTL decrementing at each router
3. ICMP Time Exceeded messages when TTL reaches 0
4. NAT/PAT changing the private source IP and port into a public IP and port
5. MTU checks at each link
6. IPv4 fragmentation when the packet is too large and the Don't Fragment flag is not set
7. Path MTU Discovery behavior when the Don't Fragment flag is set and a packet is too large

## Why I chose this artifact

This lecture felt more theoretical than some previous topics because it focused on packet structure and protocol behavior rather than a single tool or command. To make the material more concrete, I created a simulator that follows a packet hop by hop. This helped me connect the IPv4 header, ICMP, NAT, fragmentation, and Path MTU Discovery into one complete story.

## Files

| File | Purpose |
|---|---|
| `packet_journey_simulator.py` | Main Python simulation |
| `sample_output.txt` | Example output from running the simulator |
| `notes.md` | Concept explanation and reflection |
| `README.md` | Overview and AI usage |

## How to run it

From inside this folder, run:

```bash
python packet_journey_simulator.py
```

If `python` does not work on Windows, try:

```bash
py packet_journey_simulator.py
```

You should see four scenarios printed:

1. Normal packet journey with NAT
2. TTL expiration like traceroute
3. IPv4 fragmentation when DF is not set
4. Path MTU Discovery when DF is set

## Example command

```bash
cd week17-packet-journey-simulator
python packet_journey_simulator.py
```

## What I learned

The most important thing I learned is that forwarding is not just a router looking at the destination address. Each router may also decrement TTL, check MTU, generate ICMP errors, and possibly interact with NAT depending on where it sits in the network. I also better understand why fragmentation is discouraged: if one fragment is lost, the entire original datagram cannot be reassembled. Path MTU Discovery avoids this by using the DF flag and ICMP Fragmentation Needed messages.

## Generative AI Usage

I used ChatGPT to help design the artifact idea and structure the simulator. I asked it to help turn the lecture concepts into a small Python model with multiple scenarios. I then reviewed the output to make sure it matched the course concepts, especially TTL expiration, NAT translation, fragmentation offsets, and Path MTU Discovery.

The AI was useful for organizing the simulation into readable scenarios, but I still had to connect the code behavior back to the networking concepts from lecture. This artifact is not meant to be a production networking tool. It is a learning model that makes the lecture concepts easier to trace step by step.
