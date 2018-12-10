# -*- coding: utf-8 -*-
import copy
import itertools
import time
from operator import attrgetter

from Classes import Machine, Solution
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


def get_job_by_machine_and_job_id(jobs_list, job_id, machine_id):
    filter_1 = [x for x in jobs_list if x.id == job_id]
    return [x for x in filter_1 if x.machine_id == machine_id]


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

    solutions = []
    solution_counter = 0
    for range_permutation in range_permutations:

        new_solution = Solution(solution_counter)
        solution_counter = solution_counter + 1

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
        job_sequence = left + right

        # start = 0
        # next_start_per_machine = [0 for m in m_range]
        # print("next_start_per_machine", next_start_per_machine)

        machines_list = []
        # for machine in m_range:
        #     machines_list.append(Machine())

        for machine in m_range:
            new_machine = Machine(machine)
            for job in job_sequence:
                temp_job = get_job_by_machine_and_job_id(list_jobs, job, machine)
                new_machine.jobs.append(copy.deepcopy(temp_job))
            print("new_machine: ", new_machine)
            new_solution.machines.append(new_machine)

        # Establecer tiempos de cada trabajo de primer maquina
        x_counter = 0
        for machine in new_solution.machines:

            if x_counter == 0:
                # El primer trabajo siempre se ejecuta en secuencia definida, se establecen tiempos de inicio y fin de cada trabajo
                start = 0
                for job in machine.jobs:
                    job[0].start_time = start
                    job[0].end_time = job[0].start_time + job[0].duration
                    print("mx job: ", job[0])
                    start = job[0].end_time
            x_counter = x_counter + 1
            print("mx: ", machine)

        # Establecer tiempos de cada trabajo para las demas maquinas
        c_counter = 1
        d_counter = 1

        for i in range(len(new_solution.machines) - 1):
            j_counter = 0
            c1 = new_solution.machines[d_counter - 1].jobs
            c2 = new_solution.machines[d_counter].jobs

            d_counter = d_counter + 1
            s = 0
            p_end = 0
            for i in range(len(c1)):
                if j_counter == 0:
                    # primer trabajo de cada maquina
                    c2[i][0].start_time = c1[i][0].end_time
                    c2[i][0].end_time = c2[i][0].start_time + c2[i][0].duration
                    j_counter = j_counter + 1
                    s = c2[i][0].end_time
                else:
                    print("-------------")
                    print("empezar job que no es el primero en : ", s)
                    print("c1[i][0].id : ", c1[i][0].id)
                    print("c1[i][0].start_time : ", c1[i][0].start_time)
                    print("c1[i][0].end_time : ", c1[i][0].end_time)
                    print("c2[i][0].id : ", c2[i][0].id)
                    print("c2[i][0].start_time : ", c2[i][0].start_time)
                    print("c2[i][0].end_time : ", c2[i][0].end_time)
                    print("c1[i][0].end_time - s: ",c1[i][0].end_time - s)
                    if c1[i][0].end_time - s > 0:
                        c2[i][0].start_time = c1[i][0].end_time
                        c2[i][0].end_time = c2[i][0].start_time + c2[i][0].duration
                        j_counter = j_counter + 1
                        s = c2[i][0].end_time
                        pass
                    else:
                        c2[i][0].start_time = s
                        c2[i][0].end_time = c2[i][0].start_time + c2[i][0].duration
                        j_counter = j_counter + 1
                        s = c2[i][0].end_time
                        pass
                    print("-----------------")
                print("c1: ", c1[i][0])
                print("c2: ", c2[i][0])

        # for i in range(len(new_solution.machines)):
        #     print("www: ", new_solution.machines[c_counter - 1])
        #     for x_job in new_solution.machines[c_counter - 1].jobs:
        #         start = 0
        #         elem_count = 0
        #         for y_job in new_solution.machines[c_counter].jobs:
        #             if x_job[0].id == y_job[0].id:
        #                 if elem_count == 0:
        #                     y_job[0].start_time = x_job[0].end_time
        #                     y_job[0].end_time = y_job[0].start_time + y_job[0].duration
        #                     start = y_job[0].end_time
        #                     print("start: ", start)
        #                 else:
        #                     print("elem_count: ", elem_count)
        #                     print("x start: ", start)
        #             elem_count = elem_count + 1

        # for job in job_sequence:
        #     end = 0
        #     iteration_counter = 0
        #     for machine in m_range:
        #         temp_job = get_job_by_machine_and_job_id(list_jobs, job, machine)
        #         if temp_job:
        #
        #             temp_job[0].start_time = next_start_per_machine[machine]
        #             temp_job[0].end_time = next_start_per_machine[machine] + temp_job[0].duration
        #             next_start_per_machine[machine] = temp_job[0].end_time + next_start_per_machine[machine]
        #             next_start_per_machine = [temp_job[0].end_time for m in m_range]
        #             iteration_counter = iteration_counter + 1
        #         print("temp job: ", temp_job[0])
        #         print("next_start_per_machine", next_start_per_machine)

        # start = next_start

        # Agregar solucion a la lista
        solutions.append(new_solution)

    print("soluciones: ", solutions)

    end = time.time()
    print("\nTiempo de ejecucion del programa: %d ms " % ((end - start) * 1000))
    # print("\nTiempo de ejecucion del programa: %d s " % ((end - start)))


if __name__ == "__main__":
    main()
