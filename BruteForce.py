# -*- coding: utf-8 -*-
import itertools


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


# HACER: caso basico, n maquinas, n trabajos, un trabajo por maquina


class item():
    myInstances = []

    def __init__(self, val, worker):
        self.val = val
        self.worker = worker
        self.__class__.myInstances.append(self)

    def __repr__(self):
        return "(%d, %s)" % (self.val, self.worker)

    def get_list_by_worker(worker_key):
        temp = []
        for x in item.myInstances:
            if x.worker == worker_key:
                temp.append(x)
        return temp


def main():
    print("Job Shop Scheduling con Fuerza Bruta")

    A = [9, 2, 7, 8]
    B = [6, 4, 3, 7]
    C = [5, 8, 1, 8]
    D = [7, 6, 9, 4]

    for a in A:
        x = item(a, "A")

    for b in B:
        x = item(b, "B")

    for c in C:
        x = item(c, "C")

    for d in D:
        x = item(d, "D")

    for obj in item.myInstances:
        print("val: %d , worker: %s" % (obj.val, obj.worker))

    print(A)

    print('get list by worker A: ', item.get_list_by_worker("B"))
    tdd = []
    for xx in item.get_list_by_worker("A"):
        for xxx in item.get_list_by_worker("B")[1:]:
            for xxxx in item.get_list_by_worker("C")[2:]:
                for xxxxx in item.get_list_by_worker("D")[3:]:
                    tdd.append((xx, xxx, xxxx, xxxxx))
                    print(xx, xxx, xxxx, xxxxx)

    print(tdd)

    for x in tdd:
        sum = 0
        print(x)
        for y in x:
            sum = sum + y.val
        print("sum: ", sum)

    input = [A, B, C, D]

    print("--M-- | T1 | T2 | T3 | T4")
    print(" -A- ", A)
    print(" -B- ", B)
    print(" -C- ", C)
    print(" -D- ", D)

    # perms = list(itertools.permutations(input))
    # num_perms = len(list(itertools.permutations(input)))
    # print("permutations: ", perms)
    # print("permutations size: ", num_perms)
    # sum_perms = []
    #
    # for x in perms:
    #     sum_perms.append(sum(x))
    #
    # print("sum perms: ", sum_perms)

    # product(A, B) returns the same as:  ((x,y) for x in A for y in B).
    combinaciones = list(
        itertools.product(item.get_list_by_worker("A"), item.get_list_by_worker("B"), item.get_list_by_worker("C"),
                          item.get_list_by_worker("D")))
    num_combinaciones = len(combinaciones)
    print("Combinaciones: %s" % combinaciones)
    print("Total combinaciones: %d" % num_combinaciones)


    # for x in combinaciones:
    #     for y in x:
    #         t = [i for i in t if i.name != "Remove me"]


    sum_combinacines = []
    for x in combinaciones:
        sum = 0
        print("combinacion: ", x)
        for y in x:
            sum = y.val + sum
        sum_combinacines.append(sum)
        print("sum: ", sum)
        print("------")
    print("Suma de combinaciones posibles: ", sum_combinacines)

    # index = 0
    # elem = 0
    # i = 0
    #
    # while i < len(sum_combinacines) - 1:
    #     print("i: ", i)
    #     if (sum_combinacines[i] < sum_combinacines[i + 1]):
    #         print("elem: ", elem)
    #         elem = sum_combinacines[i]
    #         index = i
    #     else:
    #         elem = sum_combinacines[i + 1]
    #         index = i + 1
    #     i = i + 1

    print("index: ", sum_combinacines.index(min(sum_combinacines)))
    print("Costo minimo: ", min(sum_combinacines))
    combinacion_minima = combinaciones[sum_combinacines.index(min(sum_combinacines))]
    print("Combinacion: ", combinacion_minima)

    print("tddd: ", B.index(3))

    # TODO cuando hace combinacion, no se puede repetir la misma columna ya que dos maquinas podrian hacer el mismo trabajo
    # https://stackoverflow.com/questions/32726673/combinations-with-entries-unique-in-row-and-column
    print("Maquina %d - Trabajo %d (Duracion: %d)" % (1, A.index(combinacion_minima[0]) + 1, combinacion_minima[0]))
    print("Maquina %d - Trabajo %d (Duracion: %d)" % (2, B.index(combinacion_minima[1]) + 1, combinacion_minima[1]))
    print("Maquina %d - Trabajo %d (Duracion: %d)" % (3, C.index(combinacion_minima[2]) + 1, combinacion_minima[2]))
    print("Maquina %d - Trabajo %d (Duracion: %d)" % (4, D.index(combinacion_minima[3]) + 1, combinacion_minima[3]))

    # count = 1;
    # for a in combinacion_minima:
    #     print("Maquina %d - Trabajo %d (Duracion: %d)" % (count, combinacion_minima.index(a) + 1, a))
    #     count = count + 1;
    # #
    # for y in sum_combinacines:
    #     print("hola")


# TODO iterar por columnas o por fila
def special_combinations(matrix):
    combs = []
    print("hola")

    for x in matrix:
        for y in x:
            pass


if __name__ == "__main__":
    main()
