"""
deadlock_detection.py
Deadlock detection for a Resource Allocation Graph with one instance
of each resource.

A directed cycle in this graph means deadlock:
    process -> resource : pending request
    resource -> process : current allocation
"""

import simulation


def _build_graph(system_state):
    graph = {}

    def add_edge(source, target):
        graph.setdefault(source, []).append(target)
        graph.setdefault(target, [])

    for process_id in system_state["processes"]:
        graph.setdefault(f"P:{process_id}", [])
    for resource_id in system_state["resources"]:
        graph.setdefault(f"R:{resource_id}", [])

    for resource_id, process_id in system_state["allocations"]:
        add_edge(f"R:{resource_id}", f"P:{process_id}")

    for process_id, resource_id in system_state["requests"]:
        add_edge(f"P:{process_id}", f"R:{resource_id}")

    return graph


def _strongly_connected_components(graph):
    """Tarjan's algorithm; returns all strongly connected components."""
    index = 0
    stack = []
    on_stack = set()
    indices = {}
    lowlinks = {}
    components = []

    def visit(node):
        nonlocal index
        indices[node] = index
        lowlinks[node] = index
        index += 1
        stack.append(node)
        on_stack.add(node)

        for neighbour in graph.get(node, []):
            if neighbour not in indices:
                visit(neighbour)
                lowlinks[node] = min(lowlinks[node], lowlinks[neighbour])
            elif neighbour in on_stack:
                lowlinks[node] = min(lowlinks[node], indices[neighbour])

        if lowlinks[node] == indices[node]:
            component = []
            while True:
                member = stack.pop()
                on_stack.remove(member)
                component.append(member)
                if member == node:
                    break
            components.append(component)

    for node in graph:
        if node not in indices:
            visit(node)

    return components


def detect_deadlock(system_state):
    """
    Detect cycles in a single-instance Resource Allocation Graph.

    Returns:
        {
            "deadlock": bool,
            "processes": [...],
            "resources": [...],
            "cycles": [[...]],
            "message": str
        }
    """
    required = {"processes", "resources", "allocations", "requests"}
    if not isinstance(system_state, dict) or not required.issubset(system_state):
        return {
            "deadlock": False,
            "processes": [],
            "resources": [],
            "cycles": [],
            "message": "Invalid system state format."
        }

    graph = _build_graph(system_state)
    cyclic_components = []

    for component in _strongly_connected_components(graph):
        # A single node is cyclic only if it has a self-loop.
        if len(component) > 1:
            cyclic_components.append(component)
        elif component and component[0] in graph.get(component[0], []):
            cyclic_components.append(component)

    deadlocked_processes = set()
    deadlocked_resources = set()
    cycles = []

    for component in cyclic_components:
        process_nodes = [n for n in component if n.startswith("P:")]
        resource_nodes = [n for n in component if n.startswith("R:")]
        deadlocked_processes.update(n[2:] for n in process_nodes)
        deadlocked_resources.update(n[2:] for n in resource_nodes)
        cycles.append(component)

    is_deadlocked = bool(cyclic_components)
    return {
        "deadlock": is_deadlocked,
        "processes": sorted(deadlocked_processes),
        "resources": sorted(deadlocked_resources),
        "cycles": cycles,
        "message": (
            "Deadlock detected: circular waiting exists."
            if is_deadlocked else
            "No deadlock detected."
        )
    }


def resolve_deadlock(system_state, process_id):
    """
    Recover by terminating the selected process.
    The process is removed through simulation.remove_process(), which
    releases its allocated resources and removes its pending requests.
    """
    detection = detect_deadlock(system_state)
    if not detection["deadlock"]:
        return {
            "success": False,
            "message": "Cannot perform deadlock recovery: no deadlock is detected.",
            "system_state": simulation.get_system_state()
        }

    if process_id not in detection["processes"]:
        return {
            "success": False,
            "message": f"{process_id} is not part of the detected deadlock.",
            "system_state": simulation.get_system_state()
        }

    result = simulation.remove_process(process_id)
    return {
        "success": result["success"],
        "message": (
            f"Deadlock recovery completed: {process_id} was terminated and its resources were released."
            if result["success"] else result["message"]
        ),
        "terminated_process": process_id if result["success"] else None,
        "system_state": simulation.get_system_state(),
        "deadlock_status": detect_deadlock(simulation.get_system_state())
    }
