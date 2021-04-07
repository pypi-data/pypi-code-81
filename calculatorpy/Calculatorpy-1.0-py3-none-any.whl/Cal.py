A = int(input("Enter First NUmber:"))
B  = int(input("Enter First NUmber:"))
print("For Addition press 1")
print("For Subtraction press 2")
print("For Multiplycation press 3")
print("For Division press 4")
query = str(input())

# Funtion
def ADD():
    print(A+B)
def SUB():
    print(A-B)
def MULTI():
    print(A*B)
def DIV():
    print(A/B)

# Conditions
if "1" in query:
    ADD()
if "2" in query:
    SUB()
if "3" in query:
    MULTI()
if "4" in query:
    DIV()