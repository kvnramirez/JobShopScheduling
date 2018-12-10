# -*- coding: utf-8 -*-
import copy
import itertools
import time
from operator import attrgetter

from instances import i3
from utils import create_jobs, get_jobs_by_machine


def get_min_job(jobs_list):
    """
        Obtener la maquina con secuencia de ejecucion minima y su indice
        :param machines_list: lista de Maquinas
        :return: Maquina, index de maquina
        """
    return min(jobs_list, key=attrgetter('duration')), jobs_list.index(
        min(jobs_list, key=attrgetter('duration')))


def main():
    start = time.time()
    print("Job Shop Scheduling con Algoritmo de Johnson")

    # i2, i3, i1
    input_matrix = i3
    machines_number = len(input_matrix)
    jobs_number = len(input_matrix[0])

    # Crear list de jobs
    list_jobs = create_jobs(input_matrix)

    # print(list_jobs)

    m_range = [i for i in range(machines_number)]
    # print("m range: ", m_range)
    range_permutations = list(itertools.permutations(m_range))
    print("range permutations: ", range_permutations)

    for range_permutation in range_permutations:
        temp_matrix = []
        for i in m_range:
            temp_matrix.append(copy.deepcopy(get_jobs_by_machine(i, list_jobs)))

        print("temp matrix: ", temp_matrix)

        left = []
        right = []
        print("range permutation: ", range_permutation)
        counter = 0
        for i in range_permutation:
            print("machine for min job: ", i)
            print("new temp matrix: ", temp_matrix)
            min_job, min_job_index = get_min_job(temp_matrix[i])
            if (counter % 2) == 0:
                print("{0} is Even, right set".format(i))
                print(temp_matrix[i])
                left.append(min_job.id)
                print("updated left: ", left)
            else:
                print("{0} is Odd, left set".format(i))
                print(temp_matrix[i])
                right.append(min_job.id)
                print("updated right: ", right)
            counter = counter + 1
            del temp_matrix[i][min_job_index]
            print("-------------")

        # Ordenar de manera descendente
        # left.sort(reverse=True)
        # right.sort(reverse=True)

        print("left: ", left)
        print("right: ", right)

        print("secuencia: ", left + right)

        # Calcular solucion

    end = time.time()
    print("\nTiempo de ejecucion del programa: %d ms " % ((end - start) * 1000))
    # print("\nTiempo de ejecucion del programa: %d s " % ((end - start)))


if __name__ == "__main__":
    main()
