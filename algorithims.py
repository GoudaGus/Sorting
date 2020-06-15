from random import randint, shuffle


# test = [i for i in range(100)]
# shuffle(test)


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
    
    

    # finished = True
    # start = 0
    # for i in range(len(input_list)):
    #     if i == iteration:
    #         min_num = input_list[i]
    #         start = 1
    #     if min_num > input_list[i] and start == 1:
    #         finished = False
    #         min_num = input_list[i] 
    # input_list[0], input_list[len(input_list) - 1] = min_num, input_list[0]
    # # if finished:
    # #     return False
    # return input_list

def bogo_sort(input_list):
    finished = True
    for i in range(len(input_list) - 1):
        if input_list[i] > input_list[i + 1]:
            shuffle(input_list)
            finished = False
    if finished:
        return False
    return input_list


# list_output = selection_sort(test)
# # list_output.reverse()
# print(list_output)

