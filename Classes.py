# -*- coding: utf-8 -*-

class Solution:
    """ Clase que almacena las soluciones posibles de las maquinas """

    def __init__(self, id, makespan=0):
        self.id = id
        self.machines = []
        self.makespan = makespan

    def __repr__(self):
        return '\n->Sequencia %s , makespan: %s,\n-->maquinas: %s' % (self.id, self.makespan, self.machines)

class Sequence:
    """ Clase que almacena las soluciones posibles de las maquinas """

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
        self.next_start = 0

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
