from typing import AnyStr

def armstrong(x: int) -> bool:
    """
    This function determines whether the number given as input is `Armstrong` or not.
    If a number passes `Armstrong` test this function returns `True` else `False`

    Args: This function takes exactly one argument.

    `x:int` : x should be an integer for calculating the armstrong number.
    """

    m = x
    sum = 0
    temp = x
    count = 0
    while x!=0:
        x//=10
        count = count+1
    for i in range(0, count):
        num =temp%10
        sum = sum + pow(num,count)
        temp//=10
    if sum != m:
        return False
    else:
        return True


def listComparison(x: list) -> None:
    '''
    Gives `Largest` and `Smallest` number from the list specified by user.
    And prints the largest and smallest number from the user-given list.

    Args: This function takes exactly one argument.

    `x: list` : x should be a list to find a largest and smallest number in the list.
    '''
    largest = smallest = x[0]
    for item in x:
        if item>largest:
            largest = item
            return None

        if item<smallest:
            smallest = item
            return None

    print(f"The largest number is: {largest}")
    print(f'The smallest number is: {smallest}')


def palindromeStr(x: str) -> bool:
    """
    Checks whether a `string` is a `Palindrome` or not.
    After checking returns `True` if a `String` is a `Palindrome` else `False`

    Args: This function takes exactly one argument.

    `x:str` : x should be a string data type for the palindrome test
    """
    
    rev = x[::-1]
    if rev.casefold() == x.casefold():
        return True
    else:
        return False
    

def palindromeNum(x: int) -> bool:
    '''
    Checks whether an `integer number` is a `Palindrome` or not.
    After checking returns `True` if an `Integer Number` is a `Palindrome` else `False`.
    
    This function takes exactly one argument.
    
    Args:

    `x: int` : x should be an integer data type for the palindrome test.
    '''
    temp = x
    sum = ''
    while temp !=0:
        sum = sum + str(temp%10)
        temp = temp//10    
    if int(sum) == x:
        return True
    else:
        return False


def fibonacciSeries(x: int)-> None:
    """
    This function prints the fibonacci series upto `x` terms specified by the user.
    
    Args:
    This function takes exactly one argument.


    `x: int` : x should be an integer which specifies the range upto which the fibonacci series will be generated.
    """
    a= 0
    b=1
    list1 = []
    list1.extend([a,b])
    for i in range(0, x-2):
        c = a+b
        a = b
        b = c
        list1.append(c)

    print("The fibonacci series upto {} is:".format(x))
    print(*list1,sep=", ")
    
    return None


def factorial(x: int)-> int:
    """
    This function returns the `Factorial` value of a number which is specified in the function by user.
    
    This function takes exactly one argument.
    Args:
    `x: int` : x should be an `integer number` for calculating the factorial value of x.
    """
    
    fact = 1
    for i in range(1, x+1):
        fact*=i

    return fact


def quadEquationSqrt(a: int=1, b: int=2, c: int=3) -> None:
    """
    This function prints the `roots` of a `Quadratic Equation` whose `Coefficient` is specified by the `User`. Returns `None` if bound to a variable.

    Args: This function takes three arguments in total.

    `a: int` :The literal of this argument should be of integer data

    `b: int` :The literal of this argument should be of integer data

    `c: int` :The literal of this argument should be of integer data
    """
    
    equation = f"{a}x² + {b}x + {c}"
    print(f"User-given equation is:\n{equation}")

    discriminant = pow(b,2) - (4*a*c)

    root1 = (-b - pow(discriminant,0.5))/(2*a)
    root2 = (-b + pow(discriminant,0.5))/(2*a)

    if root1 == -(root2):
        print(f"The roots of '{equation}' is: ±{root2}")
    else:
        print(f"The roots of '{equation}' are: {root1} and {root2}")

    return None
    

def leapYear(year: int = 2020)-> None:
    """
    This function tests and `prints` whether a given year is a `Leap year` or not. Returns `None` if bound to a variable.

    Args: This function takes exactly one argument.

    `year: int` : The literal of this argument should be of `integer (int)` data type.
    """
    
    if year % 4 == 0:
        if year%100 == 0:
            if year %400 == 0:
                print(f"{year} is a leap year")
            else:
                print(f"{year} is not a leap year")
        else:
            print(f"{year} is a leap year")
    else:
        print(f"{year} is not a leap year")

    return None


def triangleDeterminer(m1: float, m2: float, m3: float) -> AnyStr:
    """
    This function returns the name of the triangle using the above arguments given by the user.

    Args: This function takes three arguments. 

    `m1: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.
    
    `m2: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.

    `m3: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.
    """

    name = ""
    if m1 == m2 == m3:
        name = "Equilateral"
    
    if m1 == m2 != m3 or m1 != m2 == m3 or m1 == m3 != m2:
        name = "Isosceles"
    
    if m1 != m2 != m3:
        name = "Scalene"

    return name
    

def threeNumComparison(a: float, b: float, c: float) -> list:
    """
    This function returns the list containing smallest and largest number respectively using the above arguments given by the user.

    Args: This function takes three arguments. 

    `a: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.
    
    `b: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.

    `c: float` : This argument accepts both `int(1 -> 1.0)` and `float(1.2 -> 1.2)` data types.
    """
    smallest = 0
    largest = 0
    if a > b and a > c:
        largest = a
        if b > c:
            smallest = c
        else:
            smallest = b

    elif b > a and b > c:
        largest = b
        if c > a:
            smallest = a
        else:
            smallest = c

    else:
        largest = c

    return list([smallest, largest])


def cryptograph(message: str = ..., mode: str = ['Encrypt', 'Decrypt', None]) -> AnyStr :
    """
    This function `Encrypts` or `Decrypts` a `message` by specifying the `mode` to either decrypt or encrypt a user-given message.

    Args:
    `message: str` : This should contain the `message` given by user.

    `mode: str` : This should contain the `mode` in string(`str`) format. The displayed list is given for the preview of the available mode specification.
    """
    keys = """a@%$bc^de!f*g&(h,i"';:.-\| ~₹jkl/m5n6o1p9q7r2s8t0uvwxy3z+#*)=_`"""
    values = keys[::-1]
    encryptionDict = dict(zip(keys, values))
    decryptionDict = dict(zip(values, keys))

    if mode == "Encrypt":
        modMessage = "".join([encryptionDict[letter] for letter in message.lower()])
        return modMessage
    
    if mode == "Decrypt":
        modMessage = "".join([decryptionDict[letter] for letter in message.lower()])
        return modMessage.capitalize()
