"""
EC 441 Weekly Artifact
Packet Journey Simulator: IPv4, ICMP, NAT, TTL, and Fragmentation

This script simulates a packet traveling from a private client to a public server.
It shows how key network-layer ideas work together:
- IPv4 header fields
- TTL decrementing at each router
- ICMP Time Exceeded messages
- NAT / Port Address Translation
- MTU checks and fragmentation behavior
- The difference between normal forwarding and Path MTU Discovery behavior

Run:
    python packet_journey_simulator.py
"""

from dataclasses import dataclass
from typing import Dict, Tuple, Optional, List


@dataclass
class Packet:
    source_ip: str
    destination_ip: str
    source_port: int
    destination_port: int
    protocol: str
    ttl: int
    total_length: int
    dont_fragment: bool
    identification: int = 1001

    def summary(self) -> str:
        df_status = "DF set" if self.dont_fragment else "DF not set"
        return (
            f"{self.protocol} packet | "
            f"{self.source_ip}:{self.source_port} -> "
            f"{self.destination_ip}:{self.destination_port} | "
            f"TTL={self.ttl} | Length={self.total_length} bytes | {df_status}"
        )


@dataclass
class Router:
    name: str
    mtu: int
    is_nat: bool = False
    public_ip: Optional[str] = None


class NATTable:
    def __init__(self):
        self.table: Dict[int, Tuple[str, int]] = {}
        self.next_public_port = 40001

    def translate_outbound(self, packet: Packet, public_ip: str) -> None:
        private_mapping = (packet.source_ip, packet.source_port)
        public_port = self.next_public_port
        self.next_public_port += 1

        self.table[public_port] = private_mapping

        print(f"    NAT translation created:")
        print(f"      LAN side: {packet.source_ip}:{packet.source_port}")
        print(f"      WAN side: {public_ip}:{public_port}")

        packet.source_ip = public_ip
        packet.source_port = public_port

    def print_table(self) -> None:
        print("\nFinal NAT Translation Table")
        print("---------------------------")
        print("WAN Side              LAN Side")
        for public_port, (private_ip, private_port) in self.table.items():
            print(f"203.0.113.10:{public_port:<7} {private_ip}:{private_port}")


def fragment_packet(packet: Packet, mtu: int) -> List[Tuple[int, int, int, int]]:
    """
    Returns a list of fragments:
    (fragment_number, total_length, more_fragments_flag, fragment_offset)

    IPv4 fragment offsets are measured in 8-byte units.
    We assume a 20-byte IPv4 header.
    """
    header_size = 20
    payload_size = packet.total_length - header_size
    max_payload_per_fragment = mtu - header_size

    # Fragment payload size, except the last one, must be a multiple of 8 bytes.
    usable_payload = (max_payload_per_fragment // 8) * 8

    fragments = []
    bytes_sent = 0
    fragment_number = 1

    while bytes_sent < payload_size:
        remaining = payload_size - bytes_sent
        this_payload = min(usable_payload, remaining)
        more_fragments = 1 if bytes_sent + this_payload < payload_size else 0
        fragment_offset = bytes_sent // 8
        total_length = this_payload + header_size

        fragments.append(
            (fragment_number, total_length, more_fragments, fragment_offset)
        )

        bytes_sent += this_payload
        fragment_number += 1

    return fragments


def send_packet(packet: Packet, path: List[Router]) -> None:
    nat_table = NATTable()

    print("Starting Packet")
    print("---------------")
    print(packet.summary())

    for hop_number, router in enumerate(path, start=1):
        print(f"\nHop {hop_number}: {router.name}")
        print("-" * (len(router.name) + 7))

        packet.ttl -= 1
        print(f"  Router decrements TTL. New TTL = {packet.ttl}")

        if packet.ttl <= 0:
            print("  TTL reached 0.")
            print("  Router drops the packet.")
            print("  ICMP Time Exceeded message would be sent back to the source.")
            print("  This is the mechanism traceroute uses to discover routers.")
            return

        if router.is_nat and router.public_ip:
            print("  This router performs NAT/PAT.")
            nat_table.translate_outbound(packet, router.public_ip)
            print("  Packet after NAT:")
            print(f"    {packet.summary()}")

        if packet.total_length > router.mtu:
            print(f"  Packet length ({packet.total_length}) exceeds this link MTU ({router.mtu}).")

            if packet.dont_fragment:
                print("  DF flag is set, so the router cannot fragment it.")
                print("  Router drops the packet.")
                print("  ICMP Destination Unreachable: Fragmentation Needed would be sent.")
                print("  This is the core idea behind Path MTU Discovery.")
                return

            print("  DF flag is not set, so IPv4 fragmentation occurs.")
            fragments = fragment_packet(packet, router.mtu)

            print("  Generated fragments:")
            print("    Fragment | Total Length | MF Flag | Fragment Offset")
            for frag_num, total_length, mf, offset in fragments:
                print(f"    {frag_num:<8} | {total_length:<12} | {mf:<7} | {offset}")

            print("  Reassembly would happen only at the destination, not at this router.")

        else:
            print(f"  Packet fits within this link MTU ({router.mtu}). No fragmentation needed.")

        print("  Packet forwarded to next hop.")

    print("\nDestination Reached")
    print("-------------------")
    print("The packet reached the destination server.")
    print("If this were ping, the destination would send an ICMP Echo Reply.")
    print("If this were TCP/UDP, the destination host would use the protocol and port fields to deliver the data.")

    nat_table.print_table()


def scenario_normal_journey() -> None:
    print("\n===================================================")
    print("Scenario 1: Normal journey with NAT and no drops")
    print("===================================================")

    packet = Packet(
        source_ip="192.168.1.25",
        destination_ip="93.184.216.34",
        source_port=51515,
        destination_port=443,
        protocol="TCP",
        ttl=64,
        total_length=1200,
        dont_fragment=True,
    )

    path = [
        Router("Home Router", mtu=1500, is_nat=True, public_ip="203.0.113.10"),
        Router("ISP Router", mtu=1500),
        Router("Backbone Router", mtu=1500),
        Router("Destination Edge Router", mtu=1500),
    ]

    send_packet(packet, path)


def scenario_traceroute_like() -> None:
    print("\n===================================================")
    print("Scenario 2: TTL expires like traceroute")
    print("===================================================")

    packet = Packet(
        source_ip="192.168.1.25",
        destination_ip="93.184.216.34",
        source_port=33434,
        destination_port=33434,
        protocol="UDP",
        ttl=2,
        total_length=100,
        dont_fragment=True,
    )

    path = [
        Router("Home Router", mtu=1500, is_nat=True, public_ip="203.0.113.10"),
        Router("ISP Router", mtu=1500),
        Router("Backbone Router", mtu=1500),
    ]

    send_packet(packet, path)


def scenario_fragmentation() -> None:
    print("\n===================================================")
    print("Scenario 3: IPv4 fragmentation when DF is not set")
    print("===================================================")

    packet = Packet(
        source_ip="192.168.1.25",
        destination_ip="93.184.216.34",
        source_port=5001,
        destination_port=5002,
        protocol="UDP",
        ttl=64,
        total_length=4000,
        dont_fragment=False,
    )

    path = [
        Router("Home Router", mtu=1500, is_nat=True, public_ip="203.0.113.10"),
        Router("Smaller MTU Router", mtu=1500),
    ]

    send_packet(packet, path)


def scenario_path_mtu_discovery() -> None:
    print("\n===================================================")
    print("Scenario 4: Path MTU Discovery behavior")
    print("===================================================")

    packet = Packet(
        source_ip="192.168.1.25",
        destination_ip="93.184.216.34",
        source_port=5001,
        destination_port=5002,
        protocol="UDP",
        ttl=64,
        total_length=4000,
        dont_fragment=True,
    )

    path = [
        Router("Home Router", mtu=1500, is_nat=True, public_ip="203.0.113.10"),
        Router("Smaller MTU Router", mtu=1500),
    ]

    send_packet(packet, path)


def main() -> None:
    scenario_normal_journey()
    scenario_traceroute_like()
    scenario_fragmentation()
    scenario_path_mtu_discovery()


if __name__ == "__main__":
    main()
