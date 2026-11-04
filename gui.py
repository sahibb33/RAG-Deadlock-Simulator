
import streamlit as st


def render_dashboard():

    # ---------- SESSION DATA ----------
    if "processes" not in st.session_state:
        st.session_state.processes = []

    if "resources" not in st.session_state:
        st.session_state.resources = []

    if "activity" not in st.session_state:
        st.session_state.activity = []

    # ---------- PAGE DESIGN ----------
    st.markdown("""
    <style>
    .stApp {
        background-color: #0b1120;
        color: white;
    }

    section[data-testid="stSidebar"] {
        background-color: #111827;
    }

    .main-title {
        font-size: 34px;
        font-weight: 800;
        color: #facc15;
    }

    .subtitle {
        color: #9ca3af;
        font-size: 15px;
    }

    .stat-card {
        background: #172033;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #273449;
        text-align: center;
    }

    .stat-number {
        font-size: 28px;
        font-weight: bold;
        color: #facc15;
    }

    .stat-label {
        color: #cbd5e1;
        font-size: 14px;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------- SIDEBAR ----------
    st.sidebar.title("🔄 RAG Simulator")
    st.sidebar.caption("Resource Allocation & Deadlock Analysis")

    page = st.sidebar.radio(
        "NAVIGATION",
        ["Dashboard", "Processes", "Resources", "Simulation", "About"]
    )

    st.sidebar.markdown("---")
    st.sidebar.info(
        "Graphical Simulator for Resource Allocation Graphs"
    )

    # ---------- DASHBOARD ----------
    if page == "Dashboard":

        st.markdown(
            '<div class="main-title">Resource Allocation Graph Simulator</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '<div class="subtitle">Visualize resource allocation and understand deadlocks interactively.</div>',
            unsafe_allow_html=True
        )

        st.write("")

        # Statistics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.processes)}</div>
                <div class="stat-label">Total Processes</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="stat-number">{len(st.session_state.resources)}</div>
                <div class="stat-label">Total Resources</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="stat-card">
                <div class="stat-number">SAFE</div>
                <div class="stat-label">System Status</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("### Simulation Controls")

        col1, col2 = st.columns(2)

        # Add Process
        with col1:
            st.markdown("#### Add Process")

            process_id = st.text_input(
                "Process ID",
                placeholder="Example: P1",
                key="dashboard_process"
            )

            if st.button("Add Process", key="add_process_dashboard",
                         use_container_width=True):

                process_id = process_id.strip().upper()

                if not process_id:
                    st.warning("Please enter a process ID.")

                elif process_id in st.session_state.processes:
                    st.warning("This process already exists.")

                else:
                    st.session_state.processes.append(process_id)
                    st.session_state.activity.append(
                        f"Process {process_id} was added."
                    )
                    st.success(f"{process_id} added successfully!")
                    st.rerun()

        # Add Resource
        with col2:
            st.markdown("#### Add Resource")

            resource_id = st.text_input(
                "Resource ID",
                placeholder="Example: R1",
                key="dashboard_resource"
            )

            if st.button("Add Resource", key="add_resource_dashboard",
                         use_container_width=True):

                resource_id = resource_id.strip().upper()

                if not resource_id:
                    st.warning("Please enter a resource ID.")

                elif resource_id in st.session_state.resources:
                    st.warning("This resource already exists.")

                else:
                    st.session_state.resources.append(resource_id)
                    st.session_state.activity.append(
                        f"Resource {resource_id} was added."
                    )
                    st.success(f"{resource_id} added successfully!")
                    st.rerun()

        st.markdown("---")

        # Current graph placeholder
        st.markdown("### Resource Allocation Graph")

        if st.session_state.processes or st.session_state.resources:
            st.info(
                "Processes and resources have been added. "
                "The graphical connections will appear after graph integration."
            )
        else:
            st.info("Add processes and resources to begin your simulation.")

        # Activity
        st.markdown("### Recent Activity")

        if st.session_state.activity:
            for item in reversed(st.session_state.activity[-5:]):
                st.write("•", item)
        else:
            st.caption("No activity yet.")

    # ---------- PROCESS MANAGEMENT ----------
    elif page == "Processes":

        st.title("Process Management")
        st.write("Add and manage system processes.")

        new_process = st.text_input(
            "Enter Process ID",
            placeholder="Example: P1",
            key="process_page_input"
        )

        if st.button("Add Process", key="process_page_add"):

            new_process = new_process.strip().upper()

            if not new_process:
                st.warning("Enter a process ID.")

            elif new_process in st.session_state.processes:
                st.warning("Process already exists.")

            else:
                st.session_state.processes.append(new_process)
                st.session_state.activity.append(
                    f"Process {new_process} was added."
                )
                st.success(f"{new_process} added successfully!")
                st.rerun()

        st.markdown("### Existing Processes")

        if st.session_state.processes:

            for process in st.session_state.processes:
                col1, col2 = st.columns([4, 1])

                col1.write(f"🔵 **{process}**")

                if col2.button("Remove", key=f"remove_{process}"):
                    st.session_state.processes.remove(process)
                    st.session_state.activity.append(
                        f"Process {process} was removed."
                    )
                    st.rerun()

        else:
            st.info("No processes added yet.")

    # ---------- RESOURCE MANAGEMENT ----------
    elif page == "Resources":

        st.title("Resource Management")
        st.write("Add and manage system resources.")

        new_resource = st.text_input(
            "Enter Resource ID",
            placeholder="Example: R1",
            key="resource_page_input"
        )

        if st.button("Add Resource", key="resource_page_add"):

            new_resource = new_resource.strip().upper()

            if not new_resource:
                st.warning("Enter a resource ID.")

            elif new_resource in st.session_state.resources:
                st.warning("Resource already exists.")

            else:
                st.session_state.resources.append(new_resource)
                st.session_state.activity.append(
                    f"Resource {new_resource} was added."
                )
                st.success(f"{new_resource} added successfully!")
                st.rerun()

        st.markdown("### Existing Resources")

        if st.session_state.resources:

            for resource in st.session_state.resources:
                col1, col2 = st.columns([4, 1])

                col1.write(f"🟨 **{resource}**")

                if col2.button("Remove", key=f"remove_{resource}"):
                    st.session_state.resources.remove(resource)
                    st.session_state.activity.append(
                        f"Resource {resource} was removed."
                    )
                    st.rerun()

        else:
            st.info("No resources added yet.")

    # ---------- SIMULATION ----------
    
    # ---------- SIMULATION ----------
    elif page == "Simulation":

        st.title("Resource Allocation & Deadlock Simulation")
        st.write("Allocate, request and release resources between processes.")

        if "allocations" not in st.session_state:
            st.session_state.allocations = []

        if "requests" not in st.session_state:
            st.session_state.requests = []

        processes = st.session_state.processes
        resources = st.session_state.resources

        if not processes or not resources:
            st.warning("Please add at least one process and one resource first.")

        else:
            st.markdown("### Resource Operations")

            operation = st.selectbox(
                "Select Operation",
                ["Allocate Resource", "Request Resource", "Release Resource"]
            )

            process = st.selectbox("Select Process", processes)
            resource = st.selectbox("Select Resource", resources)

            if st.button("Execute Operation", use_container_width=True):

                allocation = (resource, process)
                request = (process, resource)

                if operation == "Allocate Resource":

                    if allocation in st.session_state.allocations:
                        st.warning("This resource is already allocated to this process.")

                    elif any(r == resource for r, p in st.session_state.allocations):
                        st.error("This resource is already allocated. Request it instead.")

                    else:
                        st.session_state.allocations.append(allocation)
                        st.session_state.requests = [
                            item for item in st.session_state.requests
                            if item != request
                        ]
                        st.session_state.activity.append(
                            f"{resource} allocated to {process}."
                        )
                        st.success(f"{resource} allocated to {process}!")
                        st.rerun()

                elif operation == "Request Resource":

                    if allocation in st.session_state.allocations:
                        st.warning("This process already holds this resource.")

                    elif request in st.session_state.requests:
                        st.warning("This request already exists.")

                    else:
                        st.session_state.requests.append(request)
                        st.session_state.activity.append(
                            f"{process} requested {resource}."
                        )
                        st.success(f"{process} is now requesting {resource}.")
                        st.rerun()

                elif operation == "Release Resource":

                    if allocation not in st.session_state.allocations:
                        st.warning("This process does not hold this resource.")

                    else:
                        st.session_state.allocations.remove(allocation)
                        st.session_state.activity.append(
                            f"{process} released {resource}."
                        )
                        st.success(f"{process} released {resource}!")
                        st.rerun()

            st.markdown("---")
            st.markdown("### Current Allocations")

            if st.session_state.allocations:
                for resource, process in st.session_state.allocations:
                    st.write(f"🟨 {resource} → 🔵 {process}")
            else:
                st.info("No resources allocated yet.")

            st.markdown("### Pending Requests")

            if st.session_state.requests:
                for process, resource in st.session_state.requests:
                    st.write(f"🔵 {process} → 🟨 {resource}")
            else:
                st.info("No pending requests.")

            st.caption(
                "Note: This is a basic single-instance resource demo. "
                "Full deadlock detection will be connected to the backend module."
            )


    # ---------- ABOUT ----------
    elif page == "About":

        st.title("About This Project")

        st.write("""
        **Graphical Simulator for Resource Allocation Graphs**

        This project demonstrates how operating systems manage
        processes and resources and how deadlocks can occur.

        **Main Modules**

        - Frontend: Python and Streamlit
        - Backend: Python
        - Graph Visualization: NetworkX and PyVis

        **Main Objective**

        To understand resource allocation and identify deadlock
        situations through an interactive graphical simulator.
        """)

