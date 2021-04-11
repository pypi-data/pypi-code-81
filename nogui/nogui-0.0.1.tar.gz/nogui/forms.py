def ask_for(message, default, ask_type=int):
    while True:
        try:
            x = input(message + f" [default = {default}] ")
            x = default if x == "" else x
            x = ask_type(x)
            break
        except ValueError:
            print(f"'{x}' ain't '{ask_type.__name__}'. Provide correct value.")
    return x


def ask_if(message, false="n"):
    while True:
        x = input(message + f" [default = Y] ")
        if x in ("Y","n",""):
            break
        else:
            print("wrong answer: let us try again:")
    return x != "n"
