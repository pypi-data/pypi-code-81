def ifstate():
    print("""

 if [condition]:
     statement
 elif [condition]:
     statement
 else:
     statement
     
     """)

def forstate():
    print("""

 for:
 
 iterates over a sequence, executing the code inside every time.

 example:

 words = ['this', 'is', 'a', 'for' 'statement']
 
 for [string] in words:
     print('hello world')
     
 # This program will print hello world 5 times because there are 5 entries in the list.

 You can also use this with range,

 for i in range(5):
        print(i)
 # Output
 0
 1
 2
 3
 4

 """)

def breakstate():
    print("""
    
    break:

    breaks out of the current loop.

    example:

    for letter in 'TESTING':   
        if letter == 'I':
            break
        print(letter)
    
    # output
    T
    E
    S
    T

    """)

def dictstate():
    print("""
    
    dictionary:

    a set of keys and values paired together.

    example:

    dict = {'School starts': 0800, 'School ends': 1500}  
    print(dict['School starts'])

    Output:

    0800

    """)

def liststate():
    print("""
    
    list:

    A variable which can store multiple values. The values are organized positionally, so you can retrieve them with list[index].
    
    example:

    days = ['sunday', 'monday', 'tuesday', 'wendesday', 'thursday', 'friday', 'saturday']
    
    
    """)

def whilestate():
    print("""
    
    while statement:

    the statement inside the loop will continue executing as long as 
    the condition is still valid. You can use while True to make an 
    infinite loop until break is called.
    
    example:

    x = 0

    while x < 10:
        x = x + 1
        print('looped')
    
    output:

    looped
    looped
    looped
    looped
    looped
    looped
    looped
    looped
    looped
    looped

    """)

def tuplestate():
    print("""
    
    tuple:

    tuples are immutable list, meaning that they cannot be changed after you define
    them. This uses less memory and are more useful for data that doesn't need to be
    altered.

    example:

    tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)

    """)

def functionstate():
    print("""
    
    function:

    a function only runs when it is called, and can return a result as an output.

    example:

    def my_function(parameters):
        statement
    
    """)


