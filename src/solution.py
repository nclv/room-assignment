#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Adjacency matrix for room neighbour
See https://stackoverflow.com/a/64034128

---

Assignment of n students to m rooms.
We use a cost matrix.

<student>: <room numbers>
A: 1, 2, 3
B: 4, 5, 6
C: 7, 8, 1
D: 2, 3, 4

    1   2   3   4   5   6   7   8
A   1   1   1   0   0   0   0   0   
B   0   0   0   1   1   1   0   0
C   1   0   0   0   0   0   1   1
D   0   1   1   1   0   0   0   0

"""

import itertools
import logging
import sys

import fire
import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment

logging.basicConfig(filename='debug.log', filemode='w', level=logging.DEBUG)

test_cost1 = np.array(
    [
        [1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 0, 0],
        [1, 0, 0, 0, 0, 0, 1, 1],
        [0, 1, 1, 1, 0, 0, 0, 0],
    ]
)

test_cost2 = np.array(
    [
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0, 0, 0],
    ]
)

test_adj = np.array([[0, 1, 1, 0], [1, 0, 0, 0], [0, 0, 0, 1], [1, 0, 1, 0]])


def load_data(filename):
    """
    Args:
        filename (str): nom du fichier CSV contenant les données
    """
    colonnes_voeux = ["Nom", "Voeu 1", "Voeu 2", "Voeu 3"]
    colonnes_voisins = ["Nom", "Voisin 1", "Voisin 2", "Voisin 3", "Voisin 4"]

    try:
        data = pd.read_csv(filename, sep=",")
    except FileNotFoundError as err:
        print(f"FileNotFoundError: {err}")
        sys.exit(1)

    logging.info(f"\nDonnées CSV: \n {data}")
    names = data["Nom"]
    logging.debug(f"\nNoms: \n {names}")

    cost = data[colonnes_voeux]
    cost = (
        cost.melt("Nom", value_name="Room")
        .drop("variable", 1)
        .dropna()
        .astype({"Room": int})
    )
    cost = pd.crosstab(cost["Nom"], cost["Room"]).reindex(names, fill_value=0)
    logging.debug(f"\nMatrice des coûts (<student>: <wanted room numbers>): \n {cost}")

    adj = data[colonnes_voisins]
    adj = adj.melt("Nom", value_name="Voisin").drop("variable", 1).dropna()
    adj = pd.crosstab(adj["Nom"], adj["Voisin"]).reindex(
        index=names, columns=names, fill_value=0
    )
    logging.debug(f"\nMatrice d'adjacence (<student>: <wanted neighbours>): \n {adj}")

    return data, cost, adj


def get_adj_rows_max(adj):
    adj += np.transpose(adj)
    adj = np.triu(adj)
    # print(adj)

    adj_argmax = np.unravel_index(np.argmax(adj, axis=1), adj.shape)
    adj_max = adj[adj_argmax]

    return adj_argmax, adj_max


def compute_cost(cost, adj_argmax, adj_max, are_neighbour):
    """
    Add costs of the adjacency matrix to cost matrix if:
        value in the cost matrix not null (the student wants this room)
        the rooms wanted by the students are next to each other
    """
    for student1, student2, adj_cost in zip(*adj_argmax, adj_max):
        if adj_cost == 0:
            continue

        student1_cost_row = cost[student1]
        student2_cost_row = cost[student2]

        for index_cost1, index_cost2 in itertools.product(
            np.nonzero(student1_cost_row)[0], np.nonzero(student2_cost_row)[0]
        ):
            if are_neighbour(index_cost1, index_cost2):
                student1_cost_row[index_cost1] += adj_cost
                student2_cost_row[index_cost2] += adj_cost

    return cost


def check_has_wanted_room(cost, row_ind, col_ind):
    for student, room in zip(row_ind, col_ind):
        # print(np.argwhere(cost[student] != 0))
        if room not in np.argwhere(cost[student] != 0):
            logging.info(f"{student} n'a pas la chambre voulue.")


def assign(in_filename="data.csv", out_filename="result.csv"):
    # Récupération de contenu du fichier CSV
    data, cost_dataframe, adj_dataframe = load_data(in_filename)
    _, room_number = cost_dataframe.shape

    cost = cost_dataframe.to_numpy()
    adj = adj_dataframe.to_numpy()

    # Génération du dictionnaire des chambres voisines
    voisins = {n: [n - 1, n + 1] for n in range(room_number)}

    # Récupération des maximums et de leurs indices pour chaque ligne de la matrice d'adjacence
    adj_argmax, adj_max = get_adj_rows_max(adj)
    # print(adj_argmax, adj_max)
    cost = compute_cost(
        cost, adj_argmax, adj_max, lambda room1, room2: room2 in voisins[room1]
    )
    logging.debug(f"\nMatrice des coûts (<student>: <wanted room numbers>): \n {cost}")

    # Résolution du problème d'assignation
    row_ind, col_ind = linear_sum_assignment(cost, maximize=True)
    result = pd.Series(cost_dataframe.columns[col_ind], index=cost_dataframe.index[row_ind])
    logging.debug(f"\nRésultat de l'affectation: \n {result}")

    data["Rooms"] = result.values
    logging.debug(f"\nDonnées CSV: \n {data}")
    # Sauvegarde des affectations au format CSV
    data.to_csv(out_filename, index=False)


def main():
    fire.Fire(assign)

if __name__ == "__main__":
    main()
