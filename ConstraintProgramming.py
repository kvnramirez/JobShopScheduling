# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
# Import Python wrapper for or-tools CP-SAT solver.
import time

from ortools.sat.python import cp_model

# https://developers.google.com/optimization/
# https://developers.google.com/optimization/scheduling/job_shop
from instances import i3, i1, i2, i5


def minimalJobshopSat(jobs_data):
    # Crear el modelo para el solver
    model = cp_model.CpModel()

    machines_count = 1 + max(task[0] for job in jobs_data for task in job)
    all_machines = range(machines_count)
    jobs_count = len(jobs_data)
    all_jobs = range(jobs_count)

    # Calcular la suma de todos los tiempos de procesamiento de cada maquina
    horizon = sum(task[1] for job in jobs_data for task in job)

    task_type = collections.namedtuple('task_type', 'start end interval')
    assigned_task_type = collections.namedtuple('assigned_task_type',
                                                'start job index')

    # Crear todos los trabajos con la matriz de entrada
    all_tasks = {}
    for job in all_jobs:
        for task_id, task in enumerate(jobs_data[job]):
            start_var = model.NewIntVar(0, horizon,
                                        'start_%i_%i' % (job, task_id))
            duration = task[1]
            end_var = model.NewIntVar(0, horizon, 'end_%i_%i' % (job, task_id))
            interval_var = model.NewIntervalVar(
                start_var, duration, end_var, 'interval_%i_%i' % (job, task_id))
            all_tasks[job, task_id] = task_type(
                start=start_var, end=end_var, interval=interval_var)

    # Crear los contraints
    for machine in all_machines:
        intervals = []
        for job in all_jobs:
            for task_id, task in enumerate(jobs_data[job]):
                if task[0] == machine:
                    intervals.append(all_tasks[job, task_id].interval)
        model.AddNoOverlap(intervals)

    # Agregar constraints de precedencia, indican donde puede empezar cada trabajo
    for job in all_jobs:
        for task_id in range(0, len(jobs_data[job]) - 1):
            model.Add(all_tasks[job, task_id + 1].start >= all_tasks[job, task_id].end)

    # Estabelcer objetivo de makespan.
    obj_var = model.NewIntVar(0, horizon, 'makespan')
    model.AddMaxEquality(
        obj_var,
        [all_tasks[(job, len(jobs_data[job]) - 1)].end for job in all_jobs])
    model.Minimize(obj_var)

    # Resolver modelo para obtener solucion
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        # El makespan obtenido es optimo
        print('Makespan optimo: %i' % solver.ObjectiveValue())
        print()

        # Crear una lista te trabajos asignados por maquina
        assigned_jobs = [[] for _ in all_machines]
        for job in all_jobs:
            for task_id, task in enumerate(jobs_data[job]):
                machine = task[0]
                assigned_jobs[machine].append(
                    assigned_task_type(
                        start=solver.Value(all_tasks[job, task_id].start),
                        job=job,
                        index=task_id))

        disp_col_width = 10
        sol_line = ''
        sol_line_tasks = ''

        print('Calendarización optima', '\n')

        for machine in all_machines:
            # Mostrar maquinas por orden de inicio
            assigned_jobs[machine].sort()
            sol_line += 'Maquina ' + str(machine) + ': '
            sol_line_tasks += 'Maquina ' + str(machine) + ': '

            for assigned_task in assigned_jobs[machine]:
                name = 'job_%i_%i' % (assigned_task.job, assigned_task.index)
                # Agregar espacios a la salida para formatear el print en pantalla
                sol_line_tasks += name + ' ' * (disp_col_width - len(name))
                start = assigned_task.start
                duration = jobs_data[assigned_task.job][assigned_task.index][1]

                sol_tmp = '[%i,%i]' % (start, start + duration)
                # Agregar espacios a la salida para formatear el print en pantalla
                sol_line += sol_tmp + ' ' * (disp_col_width - len(sol_tmp))

            sol_line += '\n'
            sol_line_tasks += '\n'

        print(sol_line_tasks)
        print('Intervalos de tiempo para cada trabajo\n')
        print(sol_line)


def main():
    print("Job Shop Scheduling con Constraint Programming")
    t0 = time.clock()
    jobs_data = i3
    minimalJobshopSat(jobs_data)

    t1 = time.clock() - t0
    print("\nTiempo de ejecucion del programa: %s s " % (t1 - t0))  # CPU seconds elapsed (floating point)


if __name__ == "__main__":
    main()
