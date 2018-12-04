# -*- coding: utf-8 -*-
import itertools

# PYTHON MAIN
# https://www.guru99.com/learn-python-main-function-with-examples-understand-main.html

# BENCHMARKS
# https://github.com/tamy0612/JSPLIB

# ALGORITHMS
# https://www.geeksforgeeks.org/job-assignment-problem-using-branch-and-bound/

# INDEX IN TUPLE
# https://stackoverflow.com/questions/4021154/finding-the-index-of-a-string-in-a-tuple

#
# https://yurichev.com/blog/job_shop/
# https://stackoverflow.com/questions/32726673/combinations-with-entries-unique-in-row-and-column
# https://www.geeksforgeeks.org/job-assignment-problem-using-branch-and-bound/


# HACER: caso basico, n maquinas, n trabajos, un trabajo por maquina
import numpy as np
from numpy.ma import array


class item():
    myInstances = []

    def __init__(self, val, worker):
        self.val = val
        self.worker = worker
        self.__class__.myInstances.append(self)

    def __repr__(self):
        return "(%d, %s)" % (self.val, self.worker)

    def get_list_by_worker(worker_key):
        temp = []
        for x in item.myInstances:
            if x.worker == worker_key:
                temp.append(x)
        return temp


def main():
    print("Job Shop Scheduling con Fuerza Bruta")

    A = [9, 2, 7, 8]
    B = [6, 4, 3, 7]
    C = [5, 8, 1, 8]
    D = [7, 6, 9, 4]

    for a in A:
        x = item(a, "A")

    for b in B:
        x = item(b, "B")

    for c in C:
        x = item(c, "C")

    for d in D:
        x = item(d, "D")

    # for obj in item.myInstances:
    #     print("val: %d , worker: %s" % (obj.val, obj.worker))
    #
    # print(A)
    #
    # print('get list by worker A: ', item.get_list_by_worker("B"))
    # tdd = []
    # for xx in item.get_list_by_worker("A"):
    #     for xxx in item.get_list_by_worker("B")[1:]:
    #         for xxxx in item.get_list_by_worker("C")[2:]:
    #             for xxxxx in item.get_list_by_worker("D")[3:]:
    #                 tdd.append((xx, xxx, xxxx, xxxxx))
    #                 print(xx, xxx, xxxx, xxxxx)

    # print(tdd)

    # for x in tdd:
    #     sum = 0
    #     print(x)
    #     for y in x:
    #         sum = sum + y.val
    #     print("sum: ", sum)

    B = [[(1, "A"), (2, "A"), (19, "A")],
         [(12, "B"), (5, "B"), (6, "B")],
         [(7, "C"), (8, "C"), (15, "C")]]

    C = [[1, 2, 3],
         [4, 5, 6],
         [7, 8, 9]]

    n = len(B)
    index_list = range(n)
    perms = itertools.permutations(index_list)
    combinations = [[B[i][p[i]] for i in index_list] for p in perms]
    print("combinaciones: ", combinations)

    sum_combinations = []
    for combination in combinations:
        sum = 0
        for element in combination:
            sum = element[0] + sum
        sum_combinations.append(sum)
        print("combinacion: %s, tiempo total: %s" % (combination, sum))

    print("index: ", sum_combinations.index(min(sum_combinations)))
    print("Costo minimo: ", min(sum_combinations))
    combinacion_minima = combinations[sum_combinations.index(min(sum_combinations))]
    print("Combinacion: ", combinacion_minima)
    find_min_value, find_min_indexes = locate_min(sum_combinations)
    print("Min value: ", find_min_value)
    print("Index(es)min value: ", find_min_indexes)

    for min_index in find_min_indexes:
        print("Combinacion: ", combinations[min_index])


def locate_min(sum_list):
    min_indexes = []
    smallest = min(sum_list)
    for index, element in enumerate(sum_list):
        if smallest == element:  # check if this element is the minimum_value
            min_indexes.append(index)  # add the index to the list if it is

    return smallest, min_indexes

    # sum_combinacines = []
    # for x in combinaciones:
    #     sum = 0
    #     print("combinacion: ", x)
    #     for y in x:
    #         sum = y.val + sum
    #     sum_combinacines.append(sum)
    #     print("sum: ", sum)
    #     print("------")
    # print("Suma de combinaciones posibles: ", sum_combinacines)

    # combinaciones1 = list(itertools.product([1], [5, 8]))
    # print("combinaciones1: ", combinaciones1)
    #
    # combinaciones2 = list(itertools.product(combinaciones1, [9]))
    # print("combinaciones2: ", combinaciones2)

    # for row_index, row in enumerate(B):
    #     for col_index, val in enumerate(row):
    #         new = remove_row(B, row_index)
    #         print("removed rows: ", new)
    #         new = remove_columns(new, col_index-1)
    #         print("remove cols: ", new)
    #         new = []


list = []


def tddd(matrix):
    matrix_rows = len(matrix)
    if matrix_rows == 0:
        return matrix
    else:
        print("-Fila seleccionada: ", matrix[0])
        seq = []
        for index, a in enumerate(matrix[0]):
            E = a
            print("--Seleccionado E: ", E)
            seq.append(E)
            new_matrix = remove_row(matrix, 0)
            new_matrix = nremove_column(new_matrix, index)
            print("--- Sig matriz: ", new_matrix)
            print("seq: ", seq)
            tddd(new_matrix)
        print("seq: ", seq)
        list.append(seq)
    print("list: ", list)
    return list


def nremove_column(matrix, index):
    return [(x[0:index] + x[index + 1:]) for x in matrix]


def remove_row(original_matrix, element_row_index):
    """
    Remover fila de matriz
    :param original_matrix:
    :param element_row_index: row to remove
    :return:
    """
    new_matrix = []
    if (len(original_matrix)) >= element_row_index:
        new_matrix = original_matrix[:]  # Hacer una copia de la matriz original
        new_matrix.remove(original_matrix[element_row_index])
        # print("Matriz con filas removidas: ", new_matrix)
    else:
        print("Indice no coincide con tamaño de matriz")
    return new_matrix


def remove_columns(original_matrix, element_column_index):
    new_matrix = original_matrix[:]
    for x in new_matrix:
        print("element_column_index:", element_column_index)
        x.remove(x[element_column_index])
        print("Matriz con columnas removidas: ", new_matrix)
    return new_matrix


def new_matrix(matrix, index):
    newTemp = [x.remove[x.index] for x in matrix]


def remove_column(matrix, column):
    return [r.pop(column) for r in matrix]


def is_squared(matrix):
    # Check that all rows have the correct length, not just the first one
    return all(len(row) == len(matrix) for row in matrix)


# print("--M-- | T1 | T2 | T3 | T4")
# print(" -A- ", A)
# print(" -B- ", B)
# print(" -C- ", C)
# print(" -D- ", D)

# perms = list(itertools.permutations(input))
# num_perms = len(list(itertools.permutations(input)))
# print("permutations: ", perms)
# print("permutations size: ", num_perms)
# sum_perms = []
#
# for x in perms:
#     sum_perms.append(sum(x))
#
# print("sum perms: ", sum_perms)

# product(A, B) returns the same as:  ((x,y) for x in A for y in B).
# combinaciones = list(
#     itertools.product(item.get_list_by_worker("A"), item.get_list_by_worker("B"), item.get_list_by_worker("C"),
#                       item.get_list_by_worker("D")))
# num_combinaciones = len(combinaciones)
# print("Combinaciones: %s" % combinaciones)
# print("Total combinaciones: %d" % num_combinaciones)
#
# # for x in combinaciones:
# #     for y in x:
# #         t = [i for i in t if i.name != "Remove me"]
#
# sum_combinacines = []
# for x in combinaciones:
#     sum = 0
#     print("combinacion: ", x)
#     for y in x:
#         sum = y.val + sum
#     sum_combinacines.append(sum)
#     print("sum: ", sum)
#     print("------")
# print("Suma de combinaciones posibles: ", sum_combinacines)
#
# # index = 0
# # elem = 0
# # i = 0
# #
# # while i < len(sum_combinacines) - 1:
# #     print("i: ", i)
# #     if (sum_combinacines[i] < sum_combinacines[i + 1]):
# #         print("elem: ", elem)
# #         elem = sum_combinacines[i]
# #         index = i
# #     else:
# #         elem = sum_combinacines[i + 1]
# #         index = i + 1
# #     i = i + 1
#
# print("index: ", sum_combinacines.index(min(sum_combinacines)))
# print("Costo minimo: ", min(sum_combinacines))
# combinacion_minima = combinaciones[sum_combinacines.index(min(sum_combinacines))]
# print("Combinacion: ", combinacion_minima)
#
# print("tddd: ", B.index(3))
#
# # TODO cuando hace combinacion, no se puede repetir la misma columna ya que dos maquinas podrian hacer el mismo trabajo
# # https://stackoverflow.com/questions/32726673/combinations-with-entries-unique-in-row-and-column
# print("Maquina %d - Trabajo %d (Duracion: %d)" % (1, A.index(combinacion_minima[0]) + 1, combinacion_minima[0]))
# print("Maquina %d - Trabajo %d (Duracion: %d)" % (2, B.index(combinacion_minima[1]) + 1, combinacion_minima[1]))
# print("Maquina %d - Trabajo %d (Duracion: %d)" % (3, C.index(combinacion_minima[2]) + 1, combinacion_minima[2]))
# print("Maquina %d - Trabajo %d (Duracion: %d)" % (4, D.index(combinacion_minima[3]) + 1, combinacion_minima[3]))
#
# # count = 1;
# # for a in combinacion_minima:
# #     print("Maquina %d - Trabajo %d (Duracion: %d)" % (count, combinacion_minima.index(a) + 1, a))
# #     count = count + 1;
# # #
# # for y in sum_combinacines:
#     print("hola")


# TODO iterar por columnas o por fila
def special_combinations(matrix):
    combs = []
    print("hola")

    for x in matrix:
        for y in x:
            pass


if __name__ == "__main__":
    main()
