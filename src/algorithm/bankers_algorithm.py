import numpy as np


process = [
    "P1",
    "P2",
    "P3",
    "P4",
    "P5",
]
resources = [10, 5, 7]

allocated_matrix = np.array([
    [0, 1, 0],
    [2, 0, 0],
    [3, 0, 2],
    [2, 1, 1],
    [0, 0, 2],
])

max_demand = np.array([
    [7, 5, 3],
    [3, 2, 2],
    [9, 0, 2],
    [2, 2, 2],
    [4, 3, 3],
])

res_table = {
    process[0]: [allocated_matrix[0], max_demand[0]],
    process[1]: [allocated_matrix[1], max_demand[1]],
    process[2]: [allocated_matrix[2], max_demand[2]],
    process[3]: [allocated_matrix[3], max_demand[3]],
    process[4]: [allocated_matrix[4], max_demand[4]],
}

res_require = max_demand - allocated_matrix


def calc_remaining_resource(res, allocated_matrix):
    total_allocated = np.sum(allocated_matrix, axis=0)
    remaining_res = res - total_allocated
    return remaining_res


def banker_algorithm(res_requirement, resources, allocated_matrix, processes):
    n = len(processes)
    available_res = calc_remaining_resource(resources, allocated_matrix)
    finish = [False] * n
    safe_sequence = []
    for j in range(n):
        for i in range(n):
            if not finish[i]:
                if (available_res >= res_requirement[i]).all():
                    finish[i] = True
                    available_res += allocated_matrix[i]
                    safe_sequence.append(processes[i])
    return safe_sequence if all(finish) else None