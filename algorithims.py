"""Hold algorithms for UI.py."""

from random import shuffle


def insertion_sort(input_list, r):
    """Use insertion sort on list."""
    if r:
        for i in range(len(input_list) - 1):
            if input_list[i] < input_list[i + 1]:
                input_list[i], input_list[i + 1] = \
                    input_list[i + 1], input_list[i]
    else:
        for i in range(len(input_list) - 1):
            if input_list[i] > input_list[i + 1]:
                input_list[i], input_list[i + 1] = \
                    input_list[i + 1], input_list[i]
    return input_list


def selection_sort(input_list, iteration, r):
    """Use selection sort on list."""
    if r:
        iteration = len(input_list) - 1 - iteration
        lowest = input_list[iteration]
        lowest_index = iteration
        for i in range(iteration, 0, -1):
            if input_list[i - 1] < lowest:
                lowest = input_list[i - 1]
                lowest_index = i - 1
        input_list[iteration], input_list[lowest_index] = input_list[lowest_index], input_list[iteration]
    else:
        lowest = input_list[iteration]
        lowest_index = iteration
        for i in range(iteration, len(input_list) - 1):
            if input_list[i + 1] < lowest:
                lowest = input_list[i + 1]
                lowest_index = i + 1
        input_list[iteration], input_list[lowest_index] = input_list[lowest_index], input_list[iteration]
    return input_list


def bogo_sort(input_list):
    """Use bogo soort on list."""
    shuffle(input_list)
    return input_list
