## Network Layer Lab: Addressing and Routing

## 1. IP Address and Subnet

From the ipconfig output, my device has an IPv4 address of 192.168.1.196 with a subnet mask of 255.255.255.0.

The subnet mask corresponds to a /24 prefix, meaning the first 24 bits represent the network and the remaining 8 bits represent the host portion.

Using this:

Network address: 192.168.1.0
Broadcast address: 192.168.1.255
Usable host range: 192.168.1.1 – 192.168.1.254

This shows how IP addresses are divided into network and host portions, which allows routers to group devices into networks instead of tracking individual hosts.

## 2. Routing Table

From the route print output, the key entries are:

Default route:
0.0.0.0 → 192.168.1.1
Local network:
192.168.1.0/24 → On-link

The default route means that any destination outside the local subnet is sent to the gateway 192.168.1.1, which is my router.

The local network entry shows that devices within 192.168.1.0/24 can be reached directly without going through another router.

This routing table acts as a forwarding table, which is used to decide where each packet should be sent.

## 3. Packet Path (Traceroute)

Using tracert google.com, I observed multiple hops between my device and the destination.

    - Hop 1: Local router (192.168.1.1 equivalent, shown via IPv6 gateway)
    - Intermediate hops: ISP routers (Charter/Spectrum network)
    - Final hops: Google network

Some hops show Request timed out, which means those routers do not respond to traceroute requests, but the packet is still being forwarded.

Each hop represents a router forwarding the packet closer to the destination. This demonstrates how packets travel across multiple networks rather than going directly from source to destination.

## 4. Connecting Addressing and Routing

IP addressing and routing are closely connected. The prefix structure of IP addresses allows routers to group large numbers of addresses into networks.

Instead of storing routes for individual hosts, routers store routes for prefixes (like 192.168.1.0/24). When a packet is sent, the router checks its routing table and forwards the packet based on the best matching prefix.

If no specific match is found, the default route is used to send the packet toward the broader internet.

## 5. Example Walkthrough

For example, when sending a packet to Google:

    1. The destination is not part of my local subnet (192.168.1.0/24)
    2. The packet does not match any local route
    3. It matches the default route (0.0.0.0)
    4. The packet is sent to the gateway (192.168.1.1)
    5. The router forwards it through multiple ISP routers (as shown in traceroute)
    6. The packet eventually reaches Google’s network