"""Quick demonstration of the backend."""
import simulation
from deadlock_detection import detect_deadlock, resolve_deadlock


def run_demo():
    simulation.reset_simulation()

    for process in ("P1", "P2"):
        print(simulation.add_process(process))

    for resource in ("R1", "R2"):
        print(simulation.add_resource(resource))

    print(simulation.allocate_resource("P1", "R1"))
    print(simulation.allocate_resource("P2", "R2"))

    print(simulation.request_resource("P1", "R2"))
    print(simulation.request_resource("P2", "R1"))

    state = simulation.get_system_state()
    print("\\nSYSTEM STATE")
    print(state)

    print("\\nDEADLOCK CHECK")
    print(detect_deadlock(state))

    print("\\nRECOVERY: terminate P2")
    print(resolve_deadlock(state, "P2"))


if __name__ == "__main__":
    run_demo()
