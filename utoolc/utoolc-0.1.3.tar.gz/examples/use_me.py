import utoolc

if __name__ == '__main__':
    utoolc.do.utils.print_a_line()
    utoolc.utils.print_a_line()
    print(utoolc.__author__)
    print(utoolc.get_random.get_random_str_with_counts(10))
    utoolc.easy_say.say_hello_world('LC')
    # 使用 utoolc.do 统一使用入口 当然其他入口也开放 自由发挥
    print(utoolc.do.get_num_cpu())
    print(utoolc.do.get_random.get_random_str_with_counts(3))
    utoolc.do.utils.print_a_line()
    utoolc.utils.print_a_line()
