my_global_var = "This is a global variable"

class MyGlobalClass:
    def __init__(self):
        print("Hello World")
        print(f"my_global_var = {my_global_var}")

if __name__ == "__main__":
    MyGlobalClass()