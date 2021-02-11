import numpy as np
import scipy.sparse

student_number = 40
room_number = 40

# la matrice des coûts doit être modifiée si l'on souhaite utiliser un sparse array
# voir l'erreur retournée s'il n'est pas possible d'allouer une chambre à chaque étudiant:
# (lorsque tous les étudiants demandent les mêmes chambres par exemple)
# https://docs.scipy.org/doc/scipy/reference/generated/scipy.sparse.csgraph.min_weight_full_bipartite_matching.html#scipy.sparse.csgraph.min_weight_full_bipartite_matching
# ce problème n'apparaît pas avec une matrice dense car les poids nuls sont pris en compte
row = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3])
col = np.array([0, 1, 2, 3, 4, 5, 0, 6, 7, 1, 2, 3])
cost = scipy.sparse.coo_matrix(
    (np.ones(12), (row, col)), shape=(student_number, room_number), dtype="f"
).astype("int8")
cost = cost.tolil()
print(cost.data, cost.rows)
cost = scipy.sparse.random(
    room_number, room_number, density=0.5, format="lil", data_rvs=np.ones, dtype="f"
).astype("int8")

row = np.array([0, 0, 1, 2, 3, 3])
col = np.array([1, 2, 0, 3, 0, 2])
adj = scipy.sparse.coo_matrix(
    (np.ones(6), (row, col)), shape=(student_number, student_number), dtype="f"
).astype("int8")
adj = scipy.sparse.random(
    student_number, student_number, data_rvs=np.ones, dtype="f"
).astype("int8")
print(adj.toarray())

# row_ind, col_ind = scipy.sparse.csgraph.min_weight_full_bipartite_matching(cost, maximize=True)
