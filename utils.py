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
