#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from scipy.optimize import linear_sum_assignment
from solution import compute_cost, get_adj_rows_max

def generate_random_array(row_number, column_number, number_of_values_by_row):
    array = np.zeros((row_number, column_number), dtype="int8")  # Initialize array
    idx = np.random.rand(row_number, column_number).argsort(1)[
        :, :number_of_values_by_row
    ]
    array[np.arange(row_number)[:, None], idx] = 1
    return array


def test_random_bench():
    student_number, room_number = 150, 150
    voisins = {n: [n - 1, n + 1] for n in range(room_number)}

    cost = generate_random_array(student_number, room_number, np.random.randint(1, 3))
    # print(cost)
    adj = generate_random_array(student_number, student_number, np.random.randint(4))
    # print(adj)

    adj_argmax, adj_max = get_adj_rows_max(adj)
    # print(adj_argmax, adj_max)
    cost = compute_cost(
        cost, adj_argmax, adj_max, lambda room1, room2: room2 in voisins[room1]
    )
    row_ind, col_ind = linear_sum_assignment(cost, maximize=True)
    result = dict(zip(row_ind, col_ind))