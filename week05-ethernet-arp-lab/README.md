# Week 05 — Ethernet and ARP Analysis (Wireshark Lab)



## Overview



In this lab, I captured live network traffic using Wireshark in order to analyze:



1. An ARP request (broadcast)

2. An ARP reply (unicast)

3. The relationship between ARP size and Ethernet’s minimum frame size requirement



This lab connects Ethernet frame structure, MAC addressing, and ARP behavior as discussed in Lecture 8.



---



## Environment



- OS: Windows

- Connection: Wi-Fi

- Tool: Wireshark

- Traffic generated using: `ping` and ARP cache clearing



---



# Part 1 — ARP Request (Broadcast)



![ARP Request](screenshots/arp\_request.png)



In the ARP request packet:



- **Destination MAC:** `ff:ff:ff:ff:ff:ff`

- **Opcode:** request (1)

- The sender includes its IP and MAC address

- The request asks: “Who has <target IP>?”



The destination MAC address being all `ff` indicates a **broadcast**.  

This means the frame is delivered to every device on the local LAN.



This matches the expected ARP behavior: when a host knows the target IP address but does not know the target MAC address, it broadcasts an ARP request to the entire subnet.



---



# Part 2 — ARP Reply (Unicast)



![ARP Reply](screenshots/arp\_reply.png)



In the ARP reply packet:



- **Destination MAC:** a specific device MAC address (not broadcast)

- **Opcode:** reply (2)

- The responding host provides its MAC address



Unlike the request, the reply is **unicast**, meaning it is sent only to the requesting host.



This reduces unnecessary traffic since only the requester needs the mapping.



This demonstrates the asymmetry of ARP:

- Request → broadcast

- Reply → unicast



---



# Part 3 — ARP Structure and Minimum Frame Size



![ARP Structure](screenshots/arp\_structure.png)



From the ARP header:



- **Hardware size:** 6 bytes (MAC address length)

- **Protocol size:** 4 bytes (IPv4 address length)



An ARP message contains:

- Sender MAC (6 bytes)

- Sender IP (4 bytes)

- Target MAC (6 bytes)

- Target IP (4 bytes)

- Additional ARP header fields



Total ARP payload size: **28 bytes**



However, Ethernet requires:

- Minimum payload: **46 bytes**

- Minimum frame size: **64 bytes total** (including FCS)



Since 28 bytes is smaller than the required 46-byte minimum payload, Ethernet pads the frame with additional bytes to meet the minimum size requirement.



Even though Wireshark on Wi-Fi does not explicitly show Ethernet padding (due to 802.11 framing abstraction), padding is required by the Ethernet standard to maintain compatibility and support legacy collision detection constraints.



---



# Conceptual Connections



This lab demonstrates several important networking concepts:



- Ethernet frame structure (Destination MAC, Source MAC, EtherType, Payload)

- MAC addressing and broadcast behavior

- ARP as the bridge between IP addressing (network layer) and MAC addressing (link layer)

- Ethernet minimum frame size constraints

- How link-layer requirements influence higher-layer protocol behavior



---



# Reflection



Before performing this lab, ARP seemed like a simple lookup protocol. However, observing the actual broadcast and reply behavior made clear how tightly Ethernet and ARP are coupled within a subnet.



The minimum frame size requirement was especially interesting. Even though modern networks use full-duplex switched Ethernet (where collisions no longer occur), the 64-byte minimum is still enforced for backward compatibility. This shows how historical design constraints continue to influence modern protocol behavior.



Capturing real traffic reinforced the distinction between:

- End-to-end IP addressing

- One-hop Ethernet delivery



ARP exists precisely because these layers operate independently.



---



# Files Included



- `capture.pcapng` — Full Wireshark capture

- `/screenshots/` — Evidence screenshots used in this analysis



