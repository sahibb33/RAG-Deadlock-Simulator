"""
simulation.py
Core state and operations for a single-instance Resource Allocation Graph simulator.

Resource Allocation Graph edge conventions:
    (resource_id, process_id) in allocations: resource is assigned to process
    (process_id, resource_id) in requests: process is waiting for resource
"""

from copy import deepcopy

_processes = []
_resources = []
_allocations = []  # list of (resource_id, process_id)
_requests = []     # list of (process_id, resource_id)


def _result(success, message, **extra):
    return {"success": success, "message": message, **extra}


def reset_simulation():
    """Clear all processes, resources, allocations, and pending requests."""
    _processes.clear()
    _resources.clear()
    _allocations.clear()
    _requests.clear()
    return get_system_state()


def add_process(process_id):
    """Add a process such as P1."""
    process_id = str(process_id).strip()
    if not process_id:
        return _result(False, "Process ID cannot be empty.")
    if process_id in _processes:
        return _result(False, f"Process {process_id} already exists.")
    _processes.append(process_id)
    return _result(True, f"Process {process_id} added.")


def remove_process(process_id):
    """Remove a process and release every resource it holds."""
    process_id = str(process_id).strip()
    if process_id not in _processes:
        return _result(False, f"Process {process_id} does not exist.")
    _processes.remove(process_id)
    _allocations[:] = [(r, p) for r, p in _allocations if p != process_id]
    _requests[:] = [(p, r) for p, r in _requests if p != process_id]
    return _result(True, f"Process {process_id} removed; its resources were released.")


def add_resource(resource_id):
    """Add a resource such as R1. Each resource has exactly one instance."""
    resource_id = str(resource_id).strip()
    if not resource_id:
        return _result(False, "Resource ID cannot be empty.")
    if resource_id in _resources:
        return _result(False, f"Resource {resource_id} already exists.")
    _resources.append(resource_id)
    return _result(True, f"Resource {resource_id} added.")


def remove_resource(resource_id):
    """Remove a resource if it is not currently allocated or requested."""
    resource_id = str(resource_id).strip()
    if resource_id not in _resources:
        return _result(False, f"Resource {resource_id} does not exist.")
    if any(r == resource_id for r, _ in _allocations):
        return _result(False, f"Cannot remove {resource_id}: it is currently allocated.")
    if any(r == resource_id for _, r in _requests):
        return _result(False, f"Cannot remove {resource_id}: a process is requesting it.")
    _resources.remove(resource_id)
    return _result(True, f"Resource {resource_id} removed.")


def allocate_resource(process_id, resource_id):
    """Immediately allocate a free resource to a process."""
    process_id = str(process_id).strip()
    resource_id = str(resource_id).strip()

    if process_id not in _processes:
        return _result(False, f"Process {process_id} does not exist.")
    if resource_id not in _resources:
        return _result(False, f"Resource {resource_id} does not exist.")

    current_owner = next((p for r, p in _allocations if r == resource_id), None)
    if current_owner is not None:
        if current_owner == process_id:
            return _result(False, f"{process_id} already holds {resource_id}.")
        return _result(False, f"{resource_id} is already allocated to {current_owner}.")

    if (process_id, resource_id) in _requests:
        _requests.remove((process_id, resource_id))

    _allocations.append((resource_id, process_id))
    return _result(True, f"{resource_id} allocated to {process_id}.")


def request_resource(process_id, resource_id):
    """
    Request a resource.
    If free, grant it immediately. If held by another process, record a
    pending request edge. Duplicate requests are rejected.
    """
    process_id = str(process_id).strip()
    resource_id = str(resource_id).strip()

    if process_id not in _processes:
        return _result(False, f"Process {process_id} does not exist.")
    if resource_id not in _resources:
        return _result(False, f"Resource {resource_id} does not exist.")

    owner = next((p for r, p in _allocations if r == resource_id), None)
    if owner == process_id:
        return _result(False, f"{process_id} already holds {resource_id}.")
    if (process_id, resource_id) in _requests:
        return _result(False, f"{process_id} is already waiting for {resource_id}.")

    if owner is None:
        _allocations.append((resource_id, process_id))
        return _result(True, f"{resource_id} was free and has been allocated to {process_id}.",
                       granted=True)

    _requests.append((process_id, resource_id))
    return _result(True, f"{process_id} is now waiting for {resource_id}, held by {owner}.",
                   granted=False, waiting_for=owner)


def release_resource(process_id, resource_id):
    """Release a resource held by the specified process."""
    process_id = str(process_id).strip()
    resource_id = str(resource_id).strip()

    if process_id not in _processes:
        return _result(False, f"Process {process_id} does not exist.")
    if resource_id not in _resources:
        return _result(False, f"Resource {resource_id} does not exist.")
    if (resource_id, process_id) not in _allocations:
        return _result(False, f"{process_id} does not hold {resource_id}.")

    _allocations.remove((resource_id, process_id))

    # Grant the released resource to the first process waiting for it, if any.
    waiting_process = next((p for p, r in _requests if r == resource_id), None)
    if waiting_process is not None:
        _requests.remove((waiting_process, resource_id))
        _allocations.append((resource_id, waiting_process))
        return _result(True, f"{process_id} released {resource_id}; it was granted to {waiting_process}.",
                       granted_to=waiting_process)

    return _result(True, f"{process_id} released {resource_id}.")


def get_system_state():
    """Return a copy of the agreed shared data structure."""
    return {
        "processes": list(_processes),
        "resources": list(_resources),
        "allocations": list(_allocations),
        "requests": list(_requests),
    }


def load_system_state(state):
    """
    Replace internal state from a compatible state dictionary.
    Primarily useful for importing a saved state or tests.
    """
    required = {"processes", "resources", "allocations", "requests"}
    if not isinstance(state, dict) or not required.issubset(state):
        return _result(False, "Invalid state: expected processes, resources, allocations, requests.")

    processes = list(state["processes"])
    resources = list(state["resources"])
    allocations = [tuple(x) for x in state["allocations"]]
    requests = [tuple(x) for x in state["requests"]]

    if len(processes) != len(set(processes)) or len(resources) != len(set(resources)):
        return _result(False, "State contains duplicate process or resource IDs.")
    if any(r not in resources or p not in processes for r, p in allocations):
        return _result(False, "Allocation contains an unknown process or resource.")
    if any(p not in processes or r not in resources for p, r in requests):
        return _result(False, "Request contains an unknown process or resource.")
    allocated_resources = [r for r, _ in allocations]
    if len(allocated_resources) != len(set(allocated_resources)):
        return _result(False, "Single-instance rule violated: a resource has multiple owners.")

    _processes[:] = processes
    _resources[:] = resources
    _allocations[:] = allocations
    _requests[:] = requests
    return _result(True, "System state loaded.")
