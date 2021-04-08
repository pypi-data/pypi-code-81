import argparse
from requests import get
import random as ro

__version__ = "1.0.0"


def checkip():
    url = 'https://checkip.amazonaws.com/'
    response = get(url).text
    print(f'Public IP Address: {response}')


def cow_bull(n_sample, n_digits):
    guess_n = input("enter a number you guess: ").zfill(n_digits)
    if 'answer' in guess_n:
        # print(" answer is ", ''.join(n_sample))
        pass
    guess_n_list = list(str(guess_n))
    if len(guess_n_list) != len(set(guess_n_list)):
        print("Duplicates are not allowed!")
        return -1
    if len(guess_n) != n_digits:
        print(f"Only {n_digits} digits are allowed!")
        return -1
    cow = 0
    bull = 0
    for i in guess_n_list:
        if int(i) in n_sample:
            cow += 1

    for i in range(n_digits):
        if n_sample[i] == int(guess_n_list[i]):
            bull += 1
            cow -= 1

    print("Cow : {0},Bull : {1}".format(cow, bull))
    return int(guess_n)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-V", "--version", help="show program version", action="store_true")
    parser.add_argument("-n", "--name", help="output Hello Name! or Hello World!", nargs='*',
                        type=str, )
    parser.add_argument("-ip", "--checkip", help="This will check public IP address of system", action="store_true")
    parser.add_argument("-g", "--playgame", help="You can play Bulls and Cows game", action="store_true")

    # Read arguments from the command line
    args = parser.parse_args()

    if args.name:
        print(f'Hello {str(" ".join(args.name)).title()}!')
    else:
        print("Hello World Py!")

    # Check for --version or -V
    if args.version:
        print(f"Version-{__version__}")
    if args.checkip:
        checkip()
    if args.playgame:
        print(r"""
        ##############--->>> Rules: <<---################
        #   Note:                                       #
        #       Bulls = correct code, correct position. #
        #       Cows = correct code, wrong position.    #
        #################################################
        """)

        try:
            n_digits = int(input("how many digits number you need? "))
            if n_digits == 1:
                raise Exception("At least you have to 2-digits number!")
            if not type(n_digits) is int:
                raise TypeError("Only integers are allowed")
            if n_digits < 0:
                raise Exception("Sorry, no numbers below zero")
            # n_sample = ro.sample(range(10), n_digits)
            n_sample = ro.choices(range(10), k=n_digits)
            ans_list = map(str, n_sample)
            answer = ''.join(ans_list)
            ans = cow_bull(n_sample, n_digits)
            count = 1
            while ans != int(answer):
                ans = cow_bull(n_sample, n_digits)
                count += 1
            # print("answer", answer)
            # print("YOU WON!")
            print(r"""
                    |-------------------------------|
                                YOU WON!                 
                      * Answer is "{}"
                      * Number of attempts are {}       
                    |-------------------------------|   
                    """.format(answer, count))
        except Exception as e:
            print("Error : ", e)
    # Do argument parsing here (eg. with argparse) and anything else
    # you want your project to do. Return values are exit codes.


if __name__ == "__main__":
    main()
