# -*- coding: utf-8 -*-
import copy
import itertools
import time
from operator import attrgetter

from instances import i1, i2, i3


class Sequence:
    """ Clase que almacena las sequencias posibles de las maquinas """

    def __init__(self, id, makespan=0):
        self.id = id
        self.machines = []
        self.makespan = makespan

    def __repr__(self):
        return '\n->Sequencia %s , makespan: %s,\n-->maquinas: %s' % (self.id, self.makespan, self.machines)


class Machine:
    """ Clase que almacena maquinas y su secuencia """

    def __init__(self, id, total_duration=0):
        self.id = id
        self.jobs = []
        self.total_duration = total_duration

    def __repr__(self):
        return '\n-Maquina %s, duracion secuencia: %s, trabajos: %s' % (self.id, self.total_duration, self.jobs)


class Job:
    """ Clase que almacena trabajos, duracion, maquina"""

    def __init__(self, id, machine_id, duration=0, start_time=0, end_time=0):
        self.id = id
        self.start_time = start_time
        self.end_time = end_time
        self.duration = duration
        self.machine_id = machine_id

    def __repr__(self):
        return '<Trabajo %s, id_maquina: %s, tiempo_inicio: %s, tiempo_fin: %s, duracion: %s>' % (
            self.id, self.machine_id, self.start_time, self.end_time, self.duration)


def create_jobs(input):
    """
    Funcion crear objetos Trabajos en base a matriz
    :param input: matriz mxn
    :return: lista de trabajos
    """
    list = []

    m_counter = 0
    for m in input:
        for j in m:
            list.append(Job(j[0], m_counter, j[1]))
        m_counter = m_counter + 1

    return list


def get_jobs_by_machine(machine_id, jobs_list):
    """
    Obtener lista de trabajos de una maquina determinada
    :param machine_id: id de maquina
    :param jobs_list: lista de trabajos
    :return: lista de trabajos por maquina especificada
    """
    results = []

    for job in jobs_list:
        if job.machine_id == machine_id:
            results.append(job)

    return results


def sum_jobs_and_min_index(machine):
    """
    Actualizar duracion de cada machine para su secuencia de jobs
    :param machine: Machine object
    """
    sum_each = []
    sum = 0
    for x in machine.jobs:
        for elem in x:
            sum = sum + elem.duration
        sum_each.append(sum)
        machine.total_duration = sum


def get_min_duration_machine(machines_list):
    """
    Obtener la maquina con secuencia de ejecucion minima y su indice
    :param machines_list: lista de Maquinas
    :return: Maquina, index de maquina
    """
    return min(machines_list, key=attrgetter('total_duration')), machines_list.index(
        min(machines_list, key=attrgetter('total_duration')))


def get_max_sequences(sequences_list):
    """
    Obtener la maquina con secuencia de ejecucion maxima y su indice
    :param machines_list: lista de Maquinas
    :return: Maquina, index de maquina
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

    # i2, i3, i1
    input_matrix = i3
    machines_number = len(input_matrix)
    jobs_number = len(input_matrix[0])

    # Crear list de jobs
    list_jobs = create_jobs(input_matrix)

    perms_by_machine = []

    print("Generando permutaciones por maquina....")
    for x in range(machines_number):
        perms_by_machine.append(list(itertools.permutations(get_jobs_by_machine(x, list_jobs))))

    print("Permutaciones generadas por maquina:", perms_by_machine)
    print("Maquinas totales: ", len(perms_by_machine))

    print("Generando posibles sequencias...")
    sequence_combinations = list(itertools.product(*perms_by_machine))
    print("Secuencias generadas: ")
    print(sequence_combinations)
    print("Secuencias totales((n!)^m): ", len(sequence_combinations))
    print("Creando objetos necesarios...")

    sequences_list = []
    sequence_count = 1
    for sequence in sequence_combinations:
        # Crear posibles secuencias
        new_sequence = Sequence(sequence_count)
        for m_senquence in sequence:
            # Crear maquinas necesarias para cada secuencia
            new_machine = Machine(m_senquence[0].machine_id)
            # Se usa deepcopy para copiar los objetos y poderlos modificar
            new_machine.jobs.append(copy.deepcopy(m_senquence))
            # Agregar jobs a machine
            new_sequence.machines.append(new_machine)
        sequences_list.append(new_sequence)
        sequence_count = sequence_count + 1

    print(sequences_list)

    print("\nCalendarizando secuencias... ")
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

    # Ajustar tiempos de jobs para cada maquina para cada secuencia posible
    min_machine_index = 0
    for full_sequence in sequences_list:
        # Se modifican los trabajos de la maquina con duracion de secuencia de trabajos minima
        min_machine, min_machine_index = get_min_duration_machine(full_sequence.machines)
        # print("maquina con duracion minima: ", min_machine)

        # Se crea una copia de las maquinas y se elimina de la matriz la minima escogida anteriormente
        temp_machines_list = list(full_sequence.machines)
        del temp_machines_list[min_machine_index]
        # print("temp_machines_list: ", temp_machines_list)

        # Procesar caso minimo
        # print("min machine: ", min_machine)
        # Se compara cada trabajo de la secuencia minima
        for x in min_machine.jobs:
            for ymin in x:
                for machine in temp_machines_list:
                    for x in machine.jobs:
                        for celem in x:
                            # Si se intentan poner trabajos al mismo tiempo en cada maquina se recorre para que se pueda ejecutar
                            if ymin.id == celem.id:
                                # Ajustar tiempo de inicio y fin de trabajo con duracion minima
                                # print("Trabajos similares")
                                # print("y inicio: %s - fin  %s" % (ymin.start_time, ymin.end_time))
                                # print("j inicio: %s - fin %s" % (celem.start_time, celem.end_time))
                                ymin.start_time = celem.end_time
                                ymin.end_time = ymin.start_time + ymin.duration
                                # print("y nuevo inicio: %s, nuevo fin: %s" % (ymin.start_time, ymin.end_time))

        if machines_number == 3:
            # Si se tienen 3 maquinas
            new_min_machine, new_min_machine_index = get_min_duration_machine(temp_machines_list)
            # print("siguiente maquina con duracion minima: ", new_min_machine)

            # Almacenar ultima maquina con duracion minima y crear matriz
            last_min_machine = list(temp_machines_list)
            del last_min_machine[new_min_machine_index]
            last_temp_machines_list = [new_min_machine, min_machine]
            # print("ultima maquina con duracion minima: ", last_min_machine)

            # Se crea una copia de las maquinas y se elimina de la matriz la minima escogida anteriormente
            temp_machines_list_2 = list(full_sequence.machines)
            del temp_machines_list_2[new_min_machine_index]
            # print("temp_machines_list_2: ", temp_machines_list_2)

            # Procesar siguiente caso minimo
            # Se compara cada trabajo de la secuencia minima
            for x in new_min_machine.jobs:
                for ymin in x:
                    for machine in temp_machines_list_2:
                        for x in machine.jobs:
                            for celem in x:
                                if ymin.id == celem.id:
                                    # Ajustar tiempo de inicio y fin de trabajo con duracion minima
                                    # print("Trabajos similares")
                                    # print("y inicio: %s - fin  %s" % (ymin.start_time, ymin.end_time))
                                    # print("j inicio: %s - fin %s" % (celem.start_time, celem.end_time))
                                    ymin.start_time = celem.end_time
                                    ymin.end_time = ymin.start_time + ymin.duration
                                    # print("y nuevo inicio: %s, nuevo fin: %s" % (ymin.start_time, ymin.end_time))

            # Procesar ultimo caso minimo
            # Se compara cada trabajo de la secuencia minima
            for x in last_min_machine[0].jobs:
                for ymin in x:
                    for machine in last_temp_machines_list:
                        for x in machine.jobs:
                            for celem in x:
                                if ymin.id == celem.id:
                                    # Ajustar tiempo de inicio y fin de trabajo con duracion minima
                                    # print("Trabajos similares")
                                    # print("y inicio: %s - fin  %s" % (ymin.start_time, ymin.end_time))
                                    # print("j inicio: %s - fin %s" % (celem.start_time, celem.end_time))
                                    ymin.start_time = celem.end_time
                                    ymin.end_time = ymin.start_time + ymin.duration
                                    # print("y nuevo inicio: %s, nuevo fin: %s" % (ymin.start_time, ymin.end_time))

    # Calcular duracion de trabajos de cada maquina

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Calculando duraciones de cada secuencia de maquinas y de cada trabajo...")
    for sequence in sequences_list:
        durations = []
        for machine in sequence.machines:
            durations.append(machine.total_duration)

            for jobs_sequence in machine.jobs:
                end_times = []
                for job in jobs_sequence:
                    end_times.append(job.end_time)
                print("Maquina %s, %s" % (machine.id, end_times))
                machine.total_duration = max(end_times)
        sequence.makespan = max(durations)

    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Mostrando mejores calendarizaciones...")
    print("Total mejores calendarizaciones: ", len(get_max_sequences(sequences_list)))
    for y in get_max_sequences(sequences_list):
        print(sequences_list[y])

    end = time.time()
    print("\nTiempo de ejecucion del programa: %d ms " % ((end - start) * 1000))
    # print("\nTiempo de ejecucion del programa: %d s " % ((end - start)))


if __name__ == "__main__":
    main()
