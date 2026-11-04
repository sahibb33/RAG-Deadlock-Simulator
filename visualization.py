
import os
import webbrowser
from pyvis.network import Network

from graph_utils import (
    create_graph,
    find_deadlock_cycles,
    get_deadlocked_processes,
    highlight_deadlock as mark_deadlock
)


def create_visual_graph(system_state):
    """Create graph and highlight deadlock if present."""

    graph = create_graph(system_state)

    deadlocked_processes = get_deadlocked_processes(graph)

    if deadlocked_processes:
        mark_deadlock(graph, deadlocked_processes)

    return graph


def display_graph(graph):
    """Display interactive Resource Allocation Graph."""

    net = Network(
        height="650px",
        width="100%",
        directed=True,
        bgcolor="#111827",
        font_color="white",
        cdn_resources="in_line"
    )

    net.from_nx(graph)

    # Add arrows to edges
    for edge in net.edges:
        edge["arrows"] = "to"

    # Set graph heading
    if find_deadlock_cycles(graph):
        net.heading = "DEADLOCK DETECTED"
    else:
        net.heading = "RESOURCE ALLOCATION GRAPH"

    # Save HTML file using UTF-8 encoding
    filename = "rag_graph.html"

    html = net.generate_html()

    with open(filename, "w", encoding="utf-8") as file:
        file.write(html)

    # Open graph in browser
    file_path = os.path.abspath(filename)
    webbrowser.open("file://" + file_path)

    return filename


def highlight_deadlock(graph, deadlocked_processes):
    """Highlight deadlocked processes and resources."""

    return mark_deadlock(graph, deadlocked_processes)


def update_graph(system_state):
    """Update graph whenever system state changes."""

    graph = create_visual_graph(system_state)

    display_graph(graph)

    return graph


# Test example
if __name__ == "__main__":

    system_state = {

        "processes": ["P1", "P2"],

        "resources": ["R1", "R2"],

        "allocations": [
            ("R1", "P1"),
            ("R2", "P2")
        ],

        "requests": [
            ("P1", "R2"),
            ("P2", "R1")
        ]
    }

    graph = update_graph(system_state)

    if find_deadlock_cycles(graph):

        print("DEADLOCK DETECTED!")

        print(
            "Deadlocked processes:",
            get_deadlocked_processes(graph)
        )

    else:

        print("No deadlock detected.")
