# Notes: How the Packet Journey Simulator Connects to Lecture 17

## IPv4 Header Fields

The simulator represents a simplified IPv4 packet using fields like:

- source IP address
- destination IP address
- source port
- destination port
- protocol
- TTL
- total length
- Don't Fragment flag

This connects to the IPv4 datagram header because routers use the destination address for forwarding, TTL to prevent infinite loops, total length for packet size, and flags/fragment offset when fragmentation is involved.

## TTL and ICMP

Each router in the simulation decrements the packet's TTL by 1. If TTL reaches 0, the router drops the packet and prints that an ICMP Time Exceeded message would be sent.

This is the same basic mechanism used by traceroute. Traceroute sends packets with increasing TTL values so that each router along the path reveals itself when TTL expires.

## NAT / PAT

The first router in the simulation acts as a home NAT router. It changes the private source address and port into a public IP address and new public port.

Example:

```text
192.168.1.25:51515 becomes 203.0.113.10:40001
```

This represents Port Address Translation, where many private devices can share one public IPv4 address.

## Fragmentation

The simulator checks whether the packet's total length is larger than the next link's MTU. If the packet is too large and the DF flag is not set, the simulator splits the packet into fragments.

The fragment offset is measured in 8-byte units, which is why the simulator calculates offsets using payload bytes divided by 8.

## Path MTU Discovery

If the packet is too large and the DF flag is set, the router cannot fragment the packet. The simulator drops it and prints that an ICMP Fragmentation Needed message would be sent.

This models Path MTU Discovery, where the sender learns the smallest MTU along the path and reduces its packet size instead of relying on routers to fragment packets.

## IPv6 Connection

Although the simulator focuses on IPv4, it also helps explain why IPv6 simplified some parts of the header. IPv6 removed router fragmentation from the base header and relies on endpoints to handle packet sizing. This makes forwarding cleaner and avoids some of the problems caused by IPv4 fragmentation.
