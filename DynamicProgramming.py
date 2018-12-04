# -*- coding: utf-8 -*-

# https://www.geeksforgeeks.org/weighted-job-scheduling/

class Job(object):
    def __init__(self, start, finish, profit):
        self.start = start
        self.finish = finish
        self.profit = profit


def jobComparator(s1, s2):
    #  A utility function that is used for sorting events according to finish time
    return s1.finish < s2.finish


def latestNonConflict(job_array, i):
    # Find the latest job (in sorted array) that doesn't conflict with the job[i]
    pass


def findMaxProfit(job_array, n):
    # The main function that returns the maximum possible profit from given array of jobs
    pass


def main():
    dynamicProgramming()


if __name__ == "__main__":
    main()


def dynamicProgramming():
    pass
