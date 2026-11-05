Deadlock Simulator Backend

Requirements: Python 3.8+; no third-party packages.

Run demo:       python main.py
Run tests:      python -m unittest -v

Import in frontend:
  import simulation
  from deadlock_detection import detect_deadlock, resolve_deadlock

Resource Allocation Graph tuple format:
  allocations: (resource_id, process_id)
  requests:    (process_id, resource_id)

This version supports exactly one instance per resource.
