
import networkx as nx


def create_graph(system_state):
    """
    Creates a Resource Allocation Graph.

    system_state format:
    {
        "processes": ["P1", "P2"],
        "resources": ["R1", "R2"],
        "allocations": [("R1", "P1"), ("R2", "P2")],
        "requests": [("P1", "R2"), ("P2", "R1")]
    }
    """

    graph = nx.DiGraph()

    processes = system_state.get("processes", [])
    resources = system_state.get("resources", [])
    allocations = system_state.get("allocations", [])
    requests = system_state.get("requests", [])

    # Add process nodes
    for process in processes:
        graph.add_node(
            process,
            node_type="process",
            shape="dot",
            color="#3498db"
        )

    # Add resource nodes
    for resource in resources:
        graph.add_node(
            resource,
            node_type="resource",
            shape="square",
            color="#f1c40f"
        )

    # Allocation: Resource -> Process
    for resource, process in allocations:
        graph.add_edge(
            resource,
            process,
            edge_type="allocation",
            color="#27ae60",
            label="Allocated"
        )

    # Request: Process -> Resource
    for process, resource in requests:
        graph.add_edge(
            process,
            resource,
            edge_type="request",
            color="#3498db",
            label="Requested"
        )

    return graph


def find_deadlock_cycles(graph):
    """Finds circular waiting cycles in the graph."""
    cycles = list(nx.simple_cycles(graph))

    return [
        cycle for cycle in cycles
        if len(cycle) > 1
    ]


def get_deadlocked_processes(graph):
    """Returns processes involved in deadlock cycles."""
    cycles = find_deadlock_cycles(graph)

    deadlocked = set()

    for cycle in cycles:
        for node in cycle:
            if graph.nodes[node].get("node_type") == "process":
                deadlocked.add(node)

    return deadlocked


def highlight_deadlock(graph, deadlocked_processes):
    """Highlights deadlocked processes and related resources."""

    deadlocked_resources = set()

    for process in deadlocked_processes:
        if process not in graph:
            continue

        graph.nodes[process]["color"] = "#e74c3c"
        graph.nodes[process]["borderWidth"] = 4

    for cycle in find_deadlock_cycles(graph):
        if any(node in deadlocked_processes for node in cycle):
            for node in cycle:
                if graph.nodes[node].get("node_type") == "resource":
                    deadlocked_resources.add(node)

                graph.nodes[node]["color"] = "#e74c3c"
                graph.nodes[node]["borderWidth"] = 4

            for i in range(len(cycle)):
                source = cycle[i]
                target = cycle[(i + 1) % len(cycle)]

                if graph.has_edge(source, target):
                    graph.edges[source, target]["color"] = "#e74c3c"
                    graph.edges[source, target]["width"] = 4

    return graph


def update_graph(system_state):
    """Creates an updated graph from current system state."""
    return create_graph(system_state)
