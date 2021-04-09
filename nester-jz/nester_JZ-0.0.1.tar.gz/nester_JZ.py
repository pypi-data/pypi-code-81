'''
This is a "print_list" module for multilevel list printing.
Provide a function named "print_list()" for printing a nested list
Among the list maybe include nested list or doesn't  
'''


def print_list(one_list):
    '''
    This function will take a position parameter,named as "one_list".
    This could be any list of python
    Each data item (recursive) in the specified list is output to the screen,
    with each data item taking up a row
    '''
    for each in one_list:
        if isinstance(each,list):
            print_list(each)
        else:
            print(each)
