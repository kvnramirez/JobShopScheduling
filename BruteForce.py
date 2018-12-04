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

    # Configuracion
    set = m10
    m_size = len(set)
    debug = False

    # Imprimir tabla de trabajos y maquinas
    table = BeautifulTable()
    headers = []
    for x in range(len(set)):
        headers.append(str(x))
    table.column_headers = headers
    for row in set:
        table.append_row(row)
    print(table)

    # Calcular combinaciones
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


if __name__ == "__main__":
    main()
