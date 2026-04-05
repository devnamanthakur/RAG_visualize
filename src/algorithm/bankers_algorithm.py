import numpy as np
import streamlit as st

process=[
    "P1",
    "P2",
    "P3",
    "P4",
    "P5"
]

allocated_matrix= np.array([
    [0,1,0],
    [2,0,0],
    [3,0,2],
    [2,1,1],
    [0,0,2]
])

max_demand=np.array([
    [7,5,3],
    [3,2,2],
    [9,0,2],
    [2,2,2],
    [4,3,3]
])

resource_table={
    process[0]:[allocated_matrix[0],max_demand[0]],
    process[1]:[allocated_matrix[1],max_demand[1]],
    process[2]:[allocated_matrix[2],max_demand[2]],
    process[3]:[allocated_matrix[3],max_demand[3]],
    process[4]:[allocated_matrix[4],max_demand[4]]
}
