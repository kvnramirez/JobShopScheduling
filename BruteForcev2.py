# -*- coding: utf-8 -*-
import copy
import itertools
import time
from operator import attrgetter

from instances import i1, i2, i3


class Sequence:
    # https://stackoverflow.com/questions/14178203/python-object-containing-an-array-of-objects-being-weird
    def __init__(self, id, makespan=0):
        self.id = id
        self.machines = []
        self.makespan = makespan

    def __repr__(self):
        return '\n->Sequence %s , makespan: %s,\n-->machines: %s' % (self.id, self.makespan, self.machines)


class Machine:
    def __init__(self, id, total_duration=0):
        self.id = id
        self.jobs = []
        self.total_duration = total_duration

    def __repr__(self):
        return '\n-Machine %s, duration: %s, jobs: %s' % (self.id, self.total_duration, self.jobs)


class Job:
    def __init__(self, id, machine_id, duration=0, start_time=0, end_time=0):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.machine_id = machine_id

    def __repr__(self):
        return '<Job %s, machine_id: %s, start_time: %s, end_time: %s, duration: %s>' % (
            self.id, self.machine_id, self.start_time, self.end_time, self.duration)


def create_jobs(input):
    list = []

    m_counter = 0
    for m in input:
        for j in m:
            list.append(Job(j[0], m_counter, j[1]))
        m_counter = m_counter + 1

    return list


def get_jobs_by_machine(machine_id, jobs_list):
    results = []

    for job in jobs_list:
        if job.machine_id == machine_id:
            results.append(job)

    return results


def get_base_solution(jobs_list, machines_number):
    sum_each = []
    for x in range(machines_number):
        sum = 0
        for j in get_jobs_by_machine(x, jobs_list):
            sum = sum + j.duration
        sum_each.append(sum)
    print(sum_each)
    return get_jobs_by_machine(sum_each.index(min(sum_each)), jobs_list), sum_each.index(min(sum_each))


def sum_jobs_and_min_index(machine):
    """
    Actualizar duracion de cada machine para su secuencia de jobs
    :param machine: Machine object
    """
    sum_each = []
    sum = 0
    for x in machine.jobs:
        for elem in x:
            # print("elem: ", elem)
            sum = sum + elem.duration
        sum_each.append(sum)
        machine.total_duration = sum
    # print("aqui", sum_each)


def get_min_duration_machine(machines_list):
    """
    Obtener la maquina con secuencia de ejecucion minima y su indice
    :param machines_list:
    :return: Machine, machine index in list
    """
    print("spm: ", min(machines_list, key=attrgetter('total_duration')))
    return min(machines_list, key=attrgetter('total_duration')), machines_list.index(
        min(machines_list, key=attrgetter('total_duration')))


def get_max_sequences(sequences_list):
    """
    Obtener la maquina con secuencia de ejecucion minima y su indice
    :param machines_list:
    :return: Machine, machine index in list
    """
    max_indexes = []
    max_value = max(x.makespan for x in sequences_list)

    for index, element in enumerate(sequences_list):

        if max_value == element.makespan:  # check if this element is the minimum_value
            max_indexes.append(index)  # add the index to the list if it is

    return max_indexes


def main():
    start = time.time()
    print("Job Shop Scheduling con Fuerza Bruta")

    input_matrix = i2
    machines_number = len(input_matrix)
    jobs_number = len(input_matrix[0])

    # Crear list de jobs
    list_jobs = create_jobs(input_matrix)
    # print(list_jobs)

    # Test
    # print(get_jobs_by_machine(0, list_jobs))
    # print(list(itertools.permutations(get_jobs_by_machine(0, list_jobs))))
    # print(len(list(itertools.permutations(get_jobs_by_machine(0, list_jobs)))))

    # Obtener solucion base con menor duracion en secuencia y calcular sus permutaciones
    # base_solution, base_solution_machine_id = get_base_solution(list_jobs, machines_number)
    # base_solution_perms = list(itertools.permutations(base_solution))
    # print("base solution perms: ", base_solution_perms)
    # print("base solution index: ", base_solution_machine_id)

    perms_by_machine = []
    # perms_by_machine.append(base_solution_perms)

    print("Perms by machine generating....")
    for x in range(machines_number):
        perms_by_machine.append(list(itertools.permutations(get_jobs_by_machine(x, list_jobs))))

    print("Perms by machine generated:", perms_by_machine)
    print("Machine count: ", len(perms_by_machine))

    print("Generating possible sequences:")
    sequence_combinations = list(itertools.product(*perms_by_machine))
    print("Sequences generated: ")
    print(sequence_combinations)
    print("Total sequences: ", len(sequence_combinations))
    print("------------")
    print("Creating neccesary objects: ")

    sequences_list = []
    sequence_count = 1
    for sequence in sequence_combinations:
        new_sequence = Sequence(sequence_count)

        for m_senquence in sequence:
            # Crear machine
            # print("mid: ", m_senquence[0].machine_id)
            new_machine = Machine(m_senquence[0].machine_id)
            # Se usa deepcopy para copiar los objetos y poderlos modificar
            new_machine.jobs.append(copy.deepcopy(m_senquence))

            # Agregar jobs a machine
            new_sequence.machines.append(new_machine)

        sequences_list.append(new_sequence)

        sequence_count = sequence_count + 1

    print(sequences_list)

    print("\nScheduling each sequence... ")
    # Almacenar suma de jobs de cada secuencia de cada maquina
    # ->Sequence 1 , makespan: 0,
    # -->machines: [
    # -Machine 0, duration: 7, jobs: [(<Job 1, machine_id: 0, start_time: 0, end_time: 0, duration: 3>, <Job 2, machine_id: 0, start_time: 0, end_time: 0, duration: 4>)]>,
    # -Machine 1, duration: 5, jobs: [(<Job 1, machine_id: 1, start_time: 0, end_time: 0, duration: 3>, <Job 2, machine_id: 1, start_time: 0, end_time: 0, duration: 2>)]>]>
    for full_sequence in sequences_list:
        for machine in full_sequence.machines:
            sum_jobs_and_min_index(machine)
            for jobs_sequence in machine.jobs:
                start = 0
                for job in jobs_sequence:
                    job.start_time = start
                    job.end_time = job.duration + start
                    start = start + job.duration
        # print(full_sequence)

    # print(sequences_list)

    # Ajustar tiempos de jobs para cada maquina
    min_machine_index = 0
    for full_sequence in sequences_list:
        min_machine, min_machine_index = get_min_duration_machine(full_sequence.machines)
        print("which min machine: ", min_machine)

        temp_machines_list = list(full_sequence.machines)
        del temp_machines_list[min_machine_index]
        print("temp_machines_list: ", temp_machines_list)

        # Procesar caso base
        print(".........")
        print("min machine: ", min_machine)
        for x in min_machine.jobs:
            for ymin in x:
                for machine in temp_machines_list:
                    for x in machine.jobs:
                        for celem in x:
                            if ymin.id == celem.id:
                                print("job id iguales")
                                print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                                print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                                ymin.start_time = celem.end_time
                                ymin.end_time = ymin.start_time + ymin.duration
                                print("y iguales new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                            # else:
                            #     print("job id diferentes")
                            #     if (ymin.start_time - celem.end_time) >= 0 or (ymin.end_time - celem.start_time) >= 0:
                            #         print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                            #         print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                            #         ymin.start_time = celem.end_time + (celem.end_time - ymin.start_time)
                            #         ymin.end_time = ymin.start_time + ymin.duration
                            #     print("y diferentes new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                            else:
                                print("P: no")

                                print("y id: %s, start: %s - end %s" % (ymin.id, ymin.start_time, ymin.end_time))
                                print("j id %s, start: %s - end %s" % (celem.id, celem.start_time, celem.end_time))

        if machines_number == 3:
            # Para 3
            new_min_machine, new_min_machine_index = get_min_duration_machine(temp_machines_list)
            print("which min machine_2: ", new_min_machine)

            last_min_machine = list(temp_machines_list)
            del last_min_machine[new_min_machine_index]
            last_temp_machines_list = [new_min_machine, min_machine]
            print("last min machine: ", last_min_machine)

            temp_machines_list_2 = list(full_sequence.machines)
            del temp_machines_list_2[new_min_machine_index]
            print("temp_machines_list_2: ", temp_machines_list_2)

            for x in new_min_machine.jobs:
                for ymin in x:
                    for machine in temp_machines_list_2:
                        for x in machine.jobs:
                            for celem in x:
                                if ymin.id == celem.id:
                                    print("job id iguales")
                                    print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                                    print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                                    ymin.start_time = celem.end_time
                                    ymin.end_time = ymin.start_time + ymin.duration
                                    print("y iguales new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                                # else:
                                #     print("job id diferentes")
                                #     if (ymin.start_time - celem.end_time) >= 0 or (ymin.end_time - celem.start_time) >= 0:
                                #         print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                                #         print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                                #         ymin.start_time = celem.end_time + (celem.end_time - ymin.start_time)
                                #         ymin.end_time = ymin.start_time + ymin.duration
                                #     print("y diferentes new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                                else:
                                    print("P: no")

                                    print("y id: %s, start: %s - end %s" % (ymin.id, ymin.start_time, ymin.end_time))
                                    print("j id %s, start: %s - end %s" % (celem.id, celem.start_time, celem.end_time))

            for x in last_min_machine[0].jobs:
                for ymin in x:
                    for machine in last_temp_machines_list:
                        for x in machine.jobs:
                            for celem in x:
                                if ymin.id == celem.id:
                                    print("job id iguales")
                                    print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                                    print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                                    ymin.start_time = celem.end_time
                                    ymin.end_time = ymin.start_time + ymin.duration
                                    print("y iguales new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                                # else:
                                #     print("job id diferentes")
                                #     if (ymin.start_time - celem.end_time) >= 0 or (ymin.end_time - celem.start_time) >= 0:
                                #         print("y start: %s - end %s" % (ymin.start_time, ymin.end_time))
                                #         print("j start: %s - end %s" % (celem.start_time, celem.end_time))
                                #         ymin.start_time = celem.end_time + (celem.end_time - ymin.start_time)
                                #         ymin.end_time = ymin.start_time + ymin.duration
                                #     print("y diferentes new start: %s, new end: %s" % (ymin.start_time, ymin.end_time))
                                else:
                                    print("P: no")

                                    print("y id: %s, start: %s - end %s" % (ymin.id, ymin.start_time, ymin.end_time))
                                    print("j id %s, start: %s - end %s" % (celem.id, celem.start_time, celem.end_time))

    print("qpd: ", min_machine)

    # for full_sequence in sequences_list:
    #     for job_sequence in full_sequence.machines[min_machine_index].jobs:
    #         for job in job_sequence:
    #             print("job: ", job)

    # machines_matrix = list()
    # remove_in_matrix = [x for x in lst if x != 'A']
    #
    # for compare_job in

    print("99999999999999")
    print(sequences_list)

    # Calcular makespan

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Calculating spans each machine...")
    for sequence in sequences_list:
        for machine in sequence.machines:
            for jobs_sequence in machine.jobs:
                end_times = []
                for job in jobs_sequence:
                    end_times.append(job.end_time)
                print("machine %s, %s" % (machine.id, end_times))
                machine.total_duration = max(end_times)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Setting makespan each sequence...")
    for sequence in sequences_list:
        durations = []
        for machine in sequence.machines:
            durations.append(machine.total_duration)
        sequence.makespan = max(durations)

    print(sequences_list)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Displaying better sequences...")
    print("Total sequences: ", len(get_max_sequences(sequences_list)))
    for y in get_max_sequences(sequences_list):
        print(sequences_list[y])

    # for machine in temp_machines_list:
    #     print("machine tu: ", machine)
    #     for job in machine.jobs:
    #         print("job: ", job)
    #         for jjj in job:
    #             print("hhhh: ", jjj)

    # c_range = [i for i in range(0, machines_number) if i != min_machine_index]
    # print("c_range: ", c_range)

    end = time.time()
    print("\nTiempo de ejecucion del programa: %d ms " % ((end - start) * 1000))
    # print("\nTiempo de ejecucion del programa: %d s " % ((end - start)))

    # sequences_list = []
    # sequence_count = 1
    # for base_perm in base_solution_perms:
    #     # Base solution sequence append
    #     used_machines = []
    #     used_machines.append(base_solution_machine_id)
    #     seq = Sequence(sequence_count)
    #     seq.machines.append(base_perm)
    #
    #     new_range = [i for i in range(0, machines_number) if i != base_solution_machine_id]
    #
    #     print(new_range)
    #
    #     sequence_count = sequence_count + 1
    #     sequences_list.append(seq)
    #
    # print(sequences_list)


if __name__ == "__main__":
    main()
