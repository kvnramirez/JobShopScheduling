# -*- coding: utf-8 -*-
import itertools
import time

from beautifultable import BeautifulTable

from instances import m3, m4, m5, m6, m7, m8, m9, m10

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

# pip install beautifultable

# HACER: caso basico, n maquinas, n trabajos, un trabajo por maquina
from utils import locate_min


def main():
    start = time.time()
    print(">>> Job Shop Scheduling con Fuerza Bruta <<<")

    set = m10
    m_size = len(set)

    table = BeautifulTable()

    headers = []
    for x in range(len(set)):
        headers.append(str(x))

    table.column_headers = headers

    for row in set:
        table.append_row(row)

    print(table)

    debug = False

    n = len(set)
    index_list = range(n)
    perms = itertools.permutations(index_list)
    combinations = [[set[i][p[i]] for i in index_list] for p in perms]
    print("Combinaciones posibles: ", len(combinations))

    print("----- Lista de combinaciones posibles -----")
    sum_combinations = []
    for combination in combinations:
        sum = 0
        for element in combination:
            sum = element[0] + sum
        sum_combinations.append(sum)
        if debug:
            print("Combinacion: %s, tiempo total de secuencia: %s" % (combination, sum))

    print("----- Mejor(es) resultados: -----")

    find_min_value, find_min_indexes = locate_min(sum_combinations)
    print("Tiempo minimo posible: ", find_min_value)
    print("Posiciones combinaciones tiempo minimo: ", find_min_indexes)

    sum_total_perms = 0
    for min_index in find_min_indexes:
        print("Combinación: ", )

        table_seq = BeautifulTable()
        seq_headers = []
        for x in range(len(combinations[min_index])):
            seq_headers.append("Secuencia " + str(x + 1))
        table_seq.column_headers = seq_headers
        table_seq.append_row(combinations[min_index])
        print(table_seq)

        # Obtener permutaciones de las combinaciones con menor tiempo
        permutations = list(itertools.permutations(combinations[min_index]))

        print("Permutaciones: ")
        # print(permutations)
        for t in permutations:

            if m_size <= 4:
                table_seq = BeautifulTable()
                seq_headers = []
                for x in range(len(t)):
                    seq_headers.append("Secuencia " + str(x + 1))
                table_seq.column_headers = seq_headers
                table_seq.append_row(t)
                print(table_seq)

        print("------")
        sum_total_perms = sum_total_perms + len(permutations)

    print("Posibles secuencias de la combinacion(permutaciones): ", sum_total_perms)

    end = time.time()
    print("Tiempo de ejecucion del programa: %d ms " % ((end - start) * 1000))


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


if __name__ == "__main__":
    main()
