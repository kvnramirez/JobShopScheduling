# -*- coding: utf-8 -*-

def locate_min(sum_list):
    min_indexes = []
    smallest = min(sum_list)
    for index, element in enumerate(sum_list):
        if smallest == element:  # check if this element is the minimum_value
            min_indexes.append(index)  # add the index to the list if it is

    return smallest, min_indexes
