"""
TCP Lifecycle Visualizer
EC 441 Weekly Artifact

This script creates a readable, step-by-step visualization of:
1. TCP three-way handshake
2. Data transfer with sequence numbers and ACKs
3. Packet loss with duplicate ACKs and fast retransmit
4. TCP graceful teardown
5. Congestion window behavior over RTTs

Run:
    python simulator.py

Optional:
    python simulator.py --graph
"""

from dataclasses import dataclass
from typing import List
import argparse
import matplotlib.pyplot as plt


@dataclass
class TCPEvent:
    step: int
    sender: str
    receiver: str
    flag: str
    seq: str
    ack: str
    description: str


def print_section(title: str) -> None:
    print("\n" + "=" * 78)
    print(title)
    print("=" * 78)


def print_event(event: TCPEvent) -> None:
    arrow = f"{event.sender:>8}  --->  {event.receiver:<8}"
    details = f"Flag={event.flag:<8} Seq={event.seq:<8} Ack={event.ack:<8}"
    print(f"{event.step:02}. {arrow} | {details} | {event.description}")


def build_tcp_lifecycle_events() -> List[TCPEvent]:
    events = []

    # Initial sequence numbers are intentionally not zero to show ISN randomization.
    client_isn = 1200
    server_isn = 7600

    events.extend([
        TCPEvent(1, "Client", "Server", "SYN", str(client_isn), "-", 
                 "Client requests a connection and sends its initial sequence number."),
        TCPEvent(2, "Server", "Client", "SYN-ACK", str(server_isn), str(client_isn + 1),
                 "Server acknowledges the client's SYN and sends its own initial sequence number."),
        TCPEvent(3, "Client", "Server", "ACK", str(client_isn + 1), str(server_isn + 1),
                 "Client acknowledges the server's SYN. The connection is now established."),
    ])

    # Data transfer example. Each segment represents 500 bytes for clarity.
    seq1 = client_isn + 1
    segment_size = 500

    events.extend([
        TCPEvent(4, "Client", "Server", "PSH-ACK", str(seq1), str(server_isn + 1),
                 "Client sends bytes 1201 through 1700."),
        TCPEvent(5, "Server", "Client", "ACK", str(server_isn + 1), str(seq1 + segment_size),
                 "Server cumulatively ACKs the next expected byte."),
        TCPEvent(6, "Client", "Server", "PSH-ACK", str(seq1 + segment_size), str(server_isn + 1),
                 "Client sends bytes 1701 through 2200."),
        TCPEvent(7, "Server", "Client", "ACK", str(server_isn + 1), str(seq1 + 2 * segment_size),
                 "Server confirms that all bytes through 2200 arrived in order."),
    ])

    # Packet loss and fast retransmit example.
    missing_seq = seq1 + 2 * segment_size
    events.extend([
        TCPEvent(8, "Client", "Server", "PSH-ACK", str(missing_seq), str(server_isn + 1),
                 "Segment carrying bytes 2201 through 2700 is sent but LOST in the network."),
        TCPEvent(9, "Client", "Server", "PSH-ACK", str(missing_seq + segment_size), str(server_isn + 1),
                 "Later segment arrives out of order, so the receiver still expects byte 2201."),
        TCPEvent(10, "Server", "Client", "Dup ACK", str(server_isn + 1), str(missing_seq),
                 "Duplicate ACK 1 says: I am still missing byte 2201."),
        TCPEvent(11, "Client", "Server", "PSH-ACK", str(missing_seq + 2 * segment_size), str(server_isn + 1),
                 "Another later segment arrives out of order."),
        TCPEvent(12, "Server", "Client", "Dup ACK", str(server_isn + 1), str(missing_seq),
                 "Duplicate ACK 2 repeats the same missing byte."),
        TCPEvent(13, "Client", "Server", "PSH-ACK", str(missing_seq + 3 * segment_size), str(server_isn + 1),
                 "A third later segment arrives out of order."),
        TCPEvent(14, "Server", "Client", "Dup ACK", str(server_isn + 1), str(missing_seq),
                 "Duplicate ACK 3 triggers fast retransmit at the sender."),
        TCPEvent(15, "Client", "Server", "RETX", str(missing_seq), str(server_isn + 1),
                 "Client retransmits the missing segment without waiting for the timeout."),
        TCPEvent(16, "Server", "Client", "ACK", str(server_isn + 1), str(missing_seq + 4 * segment_size),
                 "Receiver can now cumulatively ACK all buffered data through byte 4200."),
    ])

    # Teardown example.
    final_client_seq = missing_seq + 4 * segment_size
    final_server_seq = server_isn + 1

    events.extend([
        TCPEvent(17, "Client", "Server", "FIN-ACK", str(final_client_seq), str(final_server_seq),
                 "Client has no more data to send and begins graceful close."),
        TCPEvent(18, "Server", "Client", "ACK", str(final_server_seq), str(final_client_seq + 1),
                 "Server acknowledges the client's FIN. Client-to-server direction is closed."),
        TCPEvent(19, "Server", "Client", "FIN-ACK", str(final_server_seq), str(final_client_seq + 1),
                 "Server is also done and sends its own FIN."),
        TCPEvent(20, "Client", "Server", "ACK", str(final_client_seq + 1), str(final_server_seq + 1),
                 "Client sends final ACK and enters TIME_WAIT."),
    ])

    return events


def print_lifecycle() -> None:
    events = build_tcp_lifecycle_events()

    print_section("TCP Lifecycle Visualizer")

    for event in events:
        if event.step == 1:
            print_section("1. Three-Way Handshake")
        elif event.step == 4:
            print_section("2. Reliable Byte-Stream Data Transfer")
        elif event.step == 8:
            print_section("3. Packet Loss, Duplicate ACKs, and Fast Retransmit")
        elif event.step == 17:
            print_section("4. Graceful Connection Teardown")

        print_event(event)

    print_section("Key Takeaways")
    print("- TCP sequence numbers count bytes, not packets.")
    print("- ACK numbers are cumulative and name the next byte expected.")
    print("- Three duplicate ACKs are treated as strong evidence of packet loss.")
    print("- FIN closes one direction at a time, so graceful teardown may use four messages.")
    print("- TIME_WAIT helps handle lost final ACKs and stale packets from older connections.")


def generate_cwnd_trace():
    """Create a simple cwnd trace based on slow start, congestion avoidance, and loss."""
    rtts = list(range(0, 18))
    cwnd = []
    ssthresh = []

    current_cwnd = 1
    current_ssthresh = 8

    for rtt in rtts:
        cwnd.append(current_cwnd)
        ssthresh.append(current_ssthresh)

        if rtt in [0, 1, 2]:
            # Slow start: double per RTT until threshold.
            current_cwnd *= 2
        elif rtt in [3, 4]:
            # Congestion avoidance: linear increase.
            current_cwnd += 1
        elif rtt == 5:
            # Triple duplicate ACK: mild loss signal.
            current_ssthresh = current_cwnd // 2
            current_cwnd = current_ssthresh
        elif rtt in [6, 7, 8]:
            current_cwnd += 1
        elif rtt == 9:
            # Timeout: severe loss signal.
            current_ssthresh = current_cwnd // 2
            current_cwnd = 1
        elif rtt in [10, 11]:
            current_cwnd *= 2
        else:
            current_cwnd += 1

    return rtts, cwnd, ssthresh


def save_cwnd_graph(output_path: str = "cwnd_graph.png") -> None:
    rtts, cwnd, ssthresh = generate_cwnd_trace()

    plt.figure(figsize=(10, 6))
    plt.plot(rtts, cwnd, marker="o", label="cwnd")
    plt.plot(rtts, ssthresh, linestyle="--", label="ssthresh")
    plt.title("TCP Congestion Window Behavior Over Time")
    plt.xlabel("Round Trip Time (RTT)")
    plt.ylabel("Window Size (MSS)")
    plt.xticks(rtts)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path, dpi=200)
    print(f"Saved congestion-window graph to {output_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="TCP Lifecycle Visualizer")
    parser.add_argument("--graph", action="store_true", help="Generate cwnd_graph.png")
    args = parser.parse_args()

    print_lifecycle()

    if args.graph:
        save_cwnd_graph()


if __name__ == "__main__":
    main()
