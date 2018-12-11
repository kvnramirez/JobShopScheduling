# -*- coding: utf-8 -*-
import copy
import itertools
import time
from operator import attrgetter

from Classes import Machine, Solution
from instances import i3, i2, i1, i4, i10, i5
from utils import create_jobs, get_jobs_by_machine, get_min_sequences


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
    t0 = time.clock()
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
            print("new temp matrix count: ", len(temp_matrix))
            min_job, min_job_index = get_min_job(temp_matrix[i])
            if (counter % 2) == 0:
                print("{0} is Even, right set".format(i))
                print("xx: ", temp_matrix[i])
                left.append(min_job.id)
                print("updated left: ", left)
            else:
                print("{0} is Odd, left set".format(i))
                print("yy: ", temp_matrix[i])
                right.append(min_job.id)
                print("updated right: ", right)
            counter = counter + 1
            for ii in range_permutation:
                print("ii: ", ii)
                del temp_matrix[ii][min_job_index]

            print("min_job_index: ", min_job_index)
            print("-------------")

        # Ordenar de manera descendente, se reduce a una sola solucion
        # left.sort(reverse=True)
        # right.sort(reverse=True)

        print("left: ", left)
        print("right: ", right)

        print("secuencia: ", left + right)
        job_sequence = left + right

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
                    print("c1[i][0].end_time - s: ", c1[i][0].end_time - s)
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

        # Agregar solucion a la lista
        solutions.append(new_solution)

    # Calcular duracion de trabajos de cada maquina

    print(solutions)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Calculando duraciones de cada secuencia de maquinas y de cada trabajo...")
    for solution in solutions:
        durations = []
        for machine in solution.machines:
            print("machine.total_duration: ", machine.total_duration)

            for jobs_sequence in machine.jobs:
                end_times = []
                for job in jobs_sequence:
                    end_times.append(job.end_time)
                print("Maquina %s, %s" % (machine.id, end_times))
                machine.total_duration = max(end_times)
                print("machine.total_duration: ", machine.total_duration)
            durations.append(machine.total_duration)
        print("durations: ", durations)
        solution.makespan = max(durations)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Mostrando mejores calendarizaciones...")
    print("Total mejores calendarizaciones: ", len(get_min_sequences(solutions)))

    if len(get_min_sequences(solutions)) > 0:
        print("Mostrando primer solucion: ")
        print(solutions[get_min_sequences(solutions)[0]])
    else:
        print("No hay solucion")

    # for y in get_min_sequences(solutions):
    #     print(solutions[y])

    t1 = time.clock() - t0
    print("\nTiempo de ejecucion del programa: %s ms " % (t1 - t0))  # CPU seconds elapsed (floating point)
    # print("\nTiempo de ejecucion del programa: %d s " % ((end - start)))


if __name__ == "__main__":
    main()
