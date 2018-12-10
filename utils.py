# -*- coding: utf-8 -*-
from Classes import Job


def locate_min(sum_list):
    min_indexes = []
    smallest = min(sum_list)
    for index, element in enumerate(sum_list):
        if smallest == element:  # check if this element is the minimum_value
            min_indexes.append(index)  # add the index to the list if it is

    return smallest, min_indexes


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


def get_min_sequences(sequences_list):
    """
    Obtener la maquina con secuencia de ejecucion maxima y su indice
    :param machines_list: lista de Maquinas
    :return: Maquina, index de maquina
    """
    min_indexes = []
    min_value = min(x.makespan for x in sequences_list)
    for index, element in enumerate(sequences_list):
        if min_value == element.makespan:  # check if this element is the minimum_value
            min_indexes.append(index)  # add the index to the list if it is

    return min_indexes
