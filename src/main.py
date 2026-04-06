import sys
import os

sys.path.append(os.path.dirname(__file__))

import streamlit as st
import numpy as np
import pandas as pd

from algorithm.bankers_algorithm import banker_algorithm, calc_remaining_resource
from visualization.rag_draw import draw_rag

st.set_page_config(
    page_title="RAG Visualizer",
    layout="wide",
)

st.title("Resource Allocation Graph Visualizer")

with st.sidebar:
    st.header("Configuration")
    n_proc = st.slider("Number of Processes", 2, 8, 5)
    n_res = st.slider("Number of Resources Types", 1, 5, 3)

    st.subheader("Process Names")
    processes = []
    for i in range(n_proc):
        name = st.text_input(
            f"Process {i+1}",
            value=f"P{i+1}",
            key=f"proc_name_{i}",
        )
        processes.append(name)

    st.subheader("Total Resources")
    cols = st.columns(n_res)
    total_resources = []
    for j, col in enumerate(cols):
        val = col.number_input(
            f"R{j+1}",
            min_value=1,
            max_value=50,
            value=[10, 5, 7][j] if j < 3 else 5,
        )
        total_resources.append(val)
    total_resources = np.array(total_resources)

res_cols = [f"R{j+1}" for j in range(n_res)]

if n_proc == 5 and n_res == 3:
    default_alloc = np.array([
        [0, 1, 0],
        [2, 0, 0],
        [3, 0, 2],
        [2, 1, 1],
        [0, 0, 2],
    ])
    default_max = np.array([
        [7, 5, 3],
        [3, 2, 2],
        [9, 0, 2],
        [2, 2, 2],
        [4, 3, 3],
    ])
else:
    default_alloc = np.zeros((n_proc, n_res), dtype=int)
    default_max = np.ones((n_proc, n_res), dtype=int)
    for i in range(n_proc):
        for j in range(n_res):
            default_alloc[i][j] = max(1, (i + j + 1) % 4)
            default_max[i][j] = default_alloc[i][j] + max(1, (i + 1) % 3 + 1)
    total_alloc_check = np.sum(default_alloc, axis=0)
    for j in range(n_res):
        if total_alloc_check[j] > total_resources[j]:
            if total_alloc_check[j] > 0:
                scale = max(0.1, (total_resources[j] - 1) / total_alloc_check[j])
                default_alloc[:, j] = np.maximum(
                    (default_alloc[:, j] * scale).astype(int), 0
                )
                found_nonzero = False
                for i in range(n_proc):
                    if default_alloc[i][j] > 0:
                        found_nonzero = True
                        break
                if not found_nonzero:
                    default_alloc[0][j] = 1
            default_max[:, j] = np.maximum(
                default_max[:, j], default_alloc[:, j] + 1
            )

col1, col2 = st.columns(2)

with col1:
    st.subheader("Allocation Matrix")
    alloc_df = st.data_editor(
        pd.DataFrame(default_alloc, index=processes, columns=res_cols),
        use_container_width=True,
        key="alloc",
    )
with col2:
    st.subheader("Max Demand Matrix")
    max_df = st.data_editor(
        pd.DataFrame(default_max, index=processes, columns=res_cols),
        use_container_width=True,
        key="max",
    )

allocated = alloc_df.to_numpy(dtype=int)
max_demand = max_df.to_numpy(dtype=int)
need = max_demand - allocated
available = calc_remaining_resource(total_resources, allocated)

has_error = False

if len(processes) != len(set(processes)):
    st.error("Process names must be unique.")
    has_error = True

if (need < 0).any():
    st.error("Allocation exceeds Max demand for some process. Fix the matrices.")
    has_error = True

if (available < 0).any():
    st.error("Total allocation exceeds available resources. Fix the matrices.")
    has_error = True

st.divider()
info1, info2, info3 = st.columns(3)

info1.metric("Total Resources", str(total_resources.tolist()))
info2.metric("Available Resources", str(available.tolist()))

with info3:
    with st.expander("Need Matrix"):
        st.dataframe(
            pd.DataFrame(need, index=processes, columns=res_cols),
            use_container_width=True,
        )

st.divider()

if st.button(
    "Run Bankers Algorithm",
    type="primary",
    use_container_width=True,
    disabled=has_error,
):
    safe_seq = banker_algorithm(need, total_resources, allocated, processes)

    if safe_seq:
        st.success("Safe State Detected")
        st.markdown(
            "**Safe Sequence:** "
            + "  →  ".join([f"`{p}`" for p in safe_seq])
        )
    else:
        st.error("Deadlock Detected")

st.divider()
st.subheader("Resource Allocation Graph")

if not has_error:
    fig = draw_rag(processes, allocated, need, total_resources)
    st.pyplot(fig, use_container_width=True)
else:
    st.warning("Fix the errors above before the graph is drawn.")