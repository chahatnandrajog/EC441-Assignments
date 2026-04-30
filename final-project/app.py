
import math

import networkx as nx
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# ------------------------------------------------------
# Page setup
# ------------------------------------------------------
st.set_page_config(
    page_title="Dijkstra Routing Simulator",
    layout="wide"
)

st.title("Dijkstra Routing Simulator")
st.caption("A visual simulator showing shortest paths, shortest-path trees, forwarding tables, and rerouting after link failures.")


# ------------------------------------------------------
# Network setup
# ------------------------------------------------------
ROUTER_POSITIONS = {
    "A": (0, 2),
    "B": (2, 3),
    "C": (2, 1),
    "D": (4, 3),
    "E": (4, 1),
    "F": (6, 2),
}

NETWORK_LINKS = [
    ("A", "B", 4),
    ("A", "C", 1),
    ("B", "C", 2),
    ("B", "D", 5),
    ("C", "E", 2),
    ("D", "E", 1),
    ("D", "F", 3),
    ("E", "F", 1),
]


# ------------------------------------------------------
# Helper functions
# ------------------------------------------------------
def edge_key(router1, router2):
    return tuple(sorted((router1, router2)))


def format_cost(cost):
    if cost == math.inf:
        return "∞"
    return int(cost)


def build_graph(failed_links):
    graph = nx.Graph()

    for router in ROUTER_POSITIONS:
        graph.add_node(router)

    for router1, router2, cost in NETWORK_LINKS:
        if edge_key(router1, router2) not in failed_links:
            graph.add_edge(router1, router2, weight=cost)

    return graph


def run_dijkstra_with_steps(graph, source):
    """
    Runs Dijkstra's algorithm from scratch and saves each step.

    distances[router] stores the best known cost from the source.
    previous[router] stores the router before it on the best path.
    finalized stores routers whose shortest path is confirmed.
    """
    distances = {router: math.inf for router in graph.nodes}
    previous = {router: None for router in graph.nodes}
    finalized = set()
    steps = []

    distances[source] = 0

    while len(finalized) < len(graph.nodes):
        unfinalized = [router for router in graph.nodes if router not in finalized]

        if not unfinalized:
            break

        current = min(unfinalized, key=lambda router: distances[router])

        if distances[current] == math.inf:
            break

        finalized.add(current)
        updates = []

        for neighbor in graph.neighbors(current):
            if neighbor in finalized:
                continue

            new_cost = distances[current] + graph[current][neighbor]["weight"]

            if new_cost < distances[neighbor]:
                old_cost = distances[neighbor]
                distances[neighbor] = new_cost
                previous[neighbor] = current
                updates.append(
                    f"{neighbor}: {format_cost(old_cost)} to {format_cost(new_cost)} through {current}"
                )

        steps.append(
            {
                "selected": current,
                "finalized": sorted(finalized),
                "distances": distances.copy(),
                "previous": previous.copy(),
                "updates": updates,
            }
        )

    return distances, previous, steps


def rebuild_path(previous, source, destination):
    path = []
    current = destination

    while current is not None:
        path.append(current)

        if current == source:
            return list(reversed(path))

        current = previous[current]

    return []


def path_to_edges(path):
    highlighted_edges = set()

    for i in range(len(path) - 1):
        highlighted_edges.add(edge_key(path[i], path[i + 1]))

    return highlighted_edges


def shortest_path_tree_edges(previous):
    tree_edges = set()

    for router, parent in previous.items():
        if parent is not None:
            tree_edges.add(edge_key(router, parent))

    return tree_edges


def make_forwarding_table(graph, source, distances, previous):
    rows = []

    for destination in sorted(graph.nodes):
        if destination == source:
            continue

        path = rebuild_path(previous, source, destination)

        if path:
            next_hop = path[1] if len(path) > 1 else "-"
            full_path = " → ".join(path)
            cost = format_cost(distances[destination])
        else:
            next_hop = "unreachable"
            full_path = "unreachable"
            cost = "∞"

        rows.append(
            {
                "Destination": destination,
                "Next Hop": next_hop,
                "Cost": cost,
                "Full Path": full_path,
            }
        )

    return pd.DataFrame(rows)


def draw_network(
    graph,
    failed_links,
    highlighted_edges,
    tree_edges,
    finalized_nodes,
    source,
    destination,
):
    fig = go.Figure()

    # Failed links are shown as red dashed lines.
    for router1, router2, cost in NETWORK_LINKS:
        if edge_key(router1, router2) in failed_links:
            x1, y1 = ROUTER_POSITIONS[router1]
            x2, y2 = ROUTER_POSITIONS[router2]

            fig.add_trace(
                go.Scatter(
                    x=[x1, x2],
                    y=[y1, y2],
                    mode="lines",
                    line=dict(color="red", width=4, dash="dash"),
                    hoverinfo="text",
                    text=f"Failed link {router1}-{router2}",
                    showlegend=False,
                )
            )

    # Active links.
    for router1, router2, data in graph.edges(data=True):
        x1, y1 = ROUTER_POSITIONS[router1]
        x2, y2 = ROUTER_POSITIONS[router2]
        current_edge = edge_key(router1, router2)

        line_color = "gray"
        line_width = 3

        if current_edge in tree_edges:
            line_color = "royalblue"
            line_width = 5

        if current_edge in highlighted_edges:
            line_color = "green"
            line_width = 8

        fig.add_trace(
            go.Scatter(
                x=[x1, x2],
                y=[y1, y2],
                mode="lines",
                line=dict(color=line_color, width=line_width),
                hoverinfo="text",
                text=f"{router1}-{router2}, cost {data['weight']}",
                showlegend=False,
            )
        )

        middle_x = (x1 + x2) / 2
        middle_y = (y1 + y2) / 2

        fig.add_trace(
            go.Scatter(
                x=[middle_x],
                y=[middle_y],
                mode="text",
                text=[str(data["weight"])],
                textfont=dict(size=16, color="black"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    # Routers.
    router_x = []
    router_y = []
    router_labels = []
    router_colors = []
    router_sizes = []

    for router, position in ROUTER_POSITIONS.items():
        x, y = position
        router_x.append(x)
        router_y.append(y)
        router_labels.append(router)

        if router == source:
            router_colors.append("royalblue")
            router_sizes.append(44)
        elif router == destination:
            router_colors.append("lightgreen")
            router_sizes.append(44)
        elif router in finalized_nodes:
            router_colors.append("lightblue")
            router_sizes.append(40)
        else:
            router_colors.append("white")
            router_sizes.append(40)

    fig.add_trace(
        go.Scatter(
            x=router_x,
            y=router_y,
            mode="markers+text",
            marker=dict(
                size=router_sizes,
                color=router_colors,
                line=dict(width=3, color="black"),
            ),
            text=router_labels,
            textposition="middle center",
            textfont=dict(size=18, color="black"),
            hoverinfo="text",
            hovertext=[f"Router {router}" for router in router_labels],
            showlegend=False,
        )
    )

    fig.update_layout(
        height=560,
        margin=dict(l=20, r=20, t=20, b=20),
        xaxis=dict(visible=False, range=(-0.7, 6.7)),
        yaxis=dict(visible=False, range=(0.3, 3.7)),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )

    return fig


# ------------------------------------------------------
# Streamlit state
# ------------------------------------------------------
if "failed_links" not in st.session_state:
    st.session_state.failed_links = set()


# ------------------------------------------------------
# Sidebar controls
# ------------------------------------------------------
st.sidebar.header("Controls")

view_mode = st.sidebar.radio(
    "View",
    [
        "Shortest Path",
        "Shortest-Path Tree",
        "Step-by-Step Dijkstra",
    ],
)

source_router = st.sidebar.selectbox(
    "Source router",
    sorted(ROUTER_POSITIONS.keys()),
    index=0
)

destination_choices = [
    router for router in sorted(ROUTER_POSITIONS.keys())
    if router != source_router
]

destination_router = st.sidebar.selectbox(
    "Destination router",
    destination_choices,
    index=destination_choices.index("F") if "F" in destination_choices else 0
)

st.sidebar.divider()

link_names = [f"{router1}-{router2}" for router1, router2, cost in NETWORK_LINKS]
selected_link_name = st.sidebar.selectbox("Choose a link to cut or restore", link_names)

selected_link_parts = selected_link_name.split("-")
selected_link = edge_key(selected_link_parts[0], selected_link_parts[1])

button_col1, button_col2 = st.sidebar.columns(2)

with button_col1:
    if st.button("Cut Link"):
        st.session_state.failed_links.add(selected_link)

with button_col2:
    if st.button("Restore Link"):
        st.session_state.failed_links.discard(selected_link)

if st.sidebar.button("Reset Network"):
    st.session_state.failed_links = set()


# ------------------------------------------------------
# Main simulator
# ------------------------------------------------------
graph = build_graph(st.session_state.failed_links)
distances, previous, steps = run_dijkstra_with_steps(graph, source_router)

shortest_path = rebuild_path(previous, source_router, destination_router)
shortest_path_edges = path_to_edges(shortest_path)
tree_edges = shortest_path_tree_edges(previous)

st.markdown(
    """
    The network is modeled as a weighted graph. Each router is a node, each connection is an edge,
    and each number is the cost of using that link. Dijkstra's algorithm finds the lowest-cost path
    from the selected source router to every other router. If a link fails, the graph changes and the
    route is recomputed, similar to how link-state routing protocols update after LSAs are flooded.
    """
)

left_column, right_column = st.columns([1.4, 1])

with left_column:
    st.subheader("Network Visualization")

    highlighted_edges = set()
    active_tree_edges = set()
    finalized_nodes = set()

    if view_mode == "Shortest Path":
        highlighted_edges = shortest_path_edges

    elif view_mode == "Shortest-Path Tree":
        active_tree_edges = tree_edges

    elif view_mode == "Step-by-Step Dijkstra":
        if steps:
            step_number = st.slider(
                "Dijkstra step",
                min_value=1,
                max_value=len(steps),
                value=1,
            )

            current_step = steps[step_number - 1]
            active_tree_edges = shortest_path_tree_edges(current_step["previous"])
            finalized_nodes = set(current_step["finalized"])

    fig = draw_network(
        graph,
        st.session_state.failed_links,
        highlighted_edges,
        active_tree_edges,
        finalized_nodes,
        source_router,
        destination_router,
    )

    st.plotly_chart(fig, use_container_width=True)

with right_column:
    st.subheader("Current Route")

    if shortest_path:
        st.success(f"Shortest path: {' → '.join(shortest_path)}")
        st.metric("Total cost", format_cost(distances[destination_router]))
    else:
        st.error(f"No route from {source_router} to {destination_router}")

    if view_mode == "Shortest Path":
        st.markdown(
            """
            The green route is the path packets would follow from the source router to the destination.
            Dijkstra chooses the path with the lowest total cost, not necessarily the path with the fewest links.
            """
        )

    elif view_mode == "Shortest-Path Tree":
        st.markdown(
            """
            The blue links show the shortest-path tree rooted at the selected source router.
            From this tree, the router can build a forwarding table by choosing the first hop toward each destination.
            """
        )

    elif view_mode == "Step-by-Step Dijkstra":
        if steps:
            current_step = steps[step_number - 1]

            st.markdown(
                f"""
                This view shows how Dijkstra's algorithm grows outward from the source router.
                The selected router for this step is **{current_step["selected"]}**.
                Light blue routers have already been finalized, meaning their shortest path is known.
                """
            )

            st.markdown("**Distance updates from this step:**")

            if current_step["updates"]:
                for update in current_step["updates"]:
                    st.write(f"- {update}")
            else:
                st.write("No distance updates happened at this step.")

    if st.session_state.failed_links:
        st.warning(
            "A link is currently failed. This simulates a topology change. In link-state routing, "
            "an updated LSA would be flooded, and routers would rerun Dijkstra using the new topology."
        )

    st.subheader("Forwarding Table")
    table = make_forwarding_table(graph, source_router, distances, previous)
    st.dataframe(table, use_container_width=True, hide_index=True)
