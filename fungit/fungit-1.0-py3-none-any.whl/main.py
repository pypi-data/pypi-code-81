from .term import Term
from .gui.box_option import initial_git_box
from .event.key import Key
from .event.process import process_key


def main():
    Term.init()
    initial_git_box()
    Key.start()

    def run():
        while not False:
            # Term.refresh()
            # Timer.stamp()

            # while Timer.not_zero():
            #     if Key.input_wait(Timer.left()):
            #         process_key()
            process_key()

    run()
    # try:
    # except Exception as e:
    #     # clean_quit(1)
    #     print(e)
    #     exit(1)


if __name__ == '__main__':
    main()
