def JoinLists(*args: [list]):

    new_list = []

    for arg_list in args:

        if type(arg_list) in [list, tuple, str]:

            for item in arg_list:

                new_list.append(item)

        else:

            raise TypeError(f'{arg_list} is not of type list but is of type \'{type(arg_list)}\'')

    return new_list

