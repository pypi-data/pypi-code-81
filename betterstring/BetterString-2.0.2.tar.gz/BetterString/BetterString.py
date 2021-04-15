from .Exceptions import *
from .Color import *
import re


FULL_SIZE = "fs"
BLUE = "blue"
CYAN = "cyan"
GREEN = "green"
ORANGE = "orange"
RED = "red"


class BetterString(str):
    __doc__ = """
    This returns a string with more functionality!

    BetterString has the same functions as str with a few extras and changes
    """.replace("    ", "")[1:]

    def __init__(self, inp, **kwargs):
        super().__init__()

        self.string = str(inp)
        self.kwargs = kwargs

    def count_pattern(self, pattern: str) -> int:
        """
        This counts how many time the pattern appears
        in the string.
        The pattern has to be a str if it is not it
        will be automatically converted

        **You can use regex**

        :param pattern: regex pattern or normal string
        """
        return len(re.findall(str(pattern), self.string))

    def lower(self, size: int or str = FULL_SIZE) -> str:
        """
        Better Upper function. You can
        choose how many characters will
        be upper size

        Usage:
        BetterString.upper({size (optional)})
        Example:
        Input:
        x = BetterString("Test String")
        x = x.upper(size=3)
        print(x)
        Output:
        TESt String

        :param size: amount of characters that will be replaced with the upper sized version of that char
        """
        lower_string = ""
        if size == "fs":
            size = len(self.string) - 1
        elif isinstance(size, str):
            raise TypeError("Size has to be of type Integer")

        if size > len(self.string) - 1:
            raise ValueError(f"Size of {size} is to big!")

        i = 0
        for i in range(0, size):
            if i <= size:
                lower_string += self.string[i].lower()

        lower_string += self.string[i + 1:]

        return lower_string

    def upper(self, size: int or str = FULL_SIZE) -> str:
        """
        Better Upper function. You can
        choose how many characters will
        be upper size

        Usage:
        BetterString.upper({size (optional)})
        Example:
        Input:
        x = BetterString("Test String")
        x = x.upper(size=3)
        print(x)
        Output:
        TESt String

        :param size: amount of characters that will be replaced with the upper sized version of that char
        """
        upper_string = ""
        if size == "fs":
            size = len(self.string)-1
        elif isinstance(size, str):
            raise TypeError("Size has to be of type Integer")

        if size > len(self.string)-1:
            raise ValueError(f"Size of {size} is to big!")

        i = 0
        for i in range(0, size):
            if i <= size:
                upper_string += self.string[i].upper()

        upper_string += self.string[i+1:]

        return upper_string

    ########## Replace
    def to_literal(self, convert_type):
        """
        Converts BetterString type to {type}
        You cant types that dont exist

        Usage:
        BetterString.convert_to({type})
        Example:
        Input:
        x = BetterString("123")
        x = x.convert_to("int")
        print(x, type(x))
        Output:
        123 <class "int">

        :param convert_type: str
        """
        try:
            ret = eval("{}({})".format(convert_type, self.string))
        except TypeError:
            raise StringCannotBeConverted(self.string, convert_type) from None

        return ret

    def execute(self, globals_: dict = None, locals_: dict = None) -> str or None:
        """
        Execute your string.
        If your code has an return statement please
        name the return value "ret_val"! otherwise we cant
        guarantee that you get that return

        :param globals_: globals
        :param locals_: locals
        :return:
        """
        if locals_ is None:
            locals_ = {}
        if globals_ is None:
            globals_ = globals()

        try:
            ret = eval(self.string)  # , globals_, locals_)
        except SyntaxError:
            try:
                exec(self.string, globals_, locals_)
                try:
                    ret = locals_["return_val"]
                except KeyError:
                    ret = None
            except SyntaxError:
                raise StringCannotBeExecuted

        return ret

    def colorize(self, color: str, bold: bool = False, underline: bool = False) -> str:
        """
        Colorizes the string with the given color

        Available colors:
        "blue",
        "cyan",
        "green",
        "orange",
        "red"

        :param color: Color which the text should have
        :param bold: If the text should be bold
        :param underline: If the text should be underlined
        :return: The colorized text
        """
        return colorize(self.string, color, bold, underline)

    # Maybe i will use this code again idk
    """
    def __getitem__(self, item: int or slice) -> str or list:
        ret = None

        if isinstance(item, int):
            ret = self.string[int(item)]

        elif isinstance(item, slice):
            slice_size = item.start
            str_len = len(self.string)

            if slice_size < str_len:
                ret = self.string[item]
            else:
                raise IndexStartOutOfBoundError

        elif isinstance(item, str):
            raise TypeError("String indices must be integers!")

        return ret
    """

    def __call__(self) -> Exception:
        raise StringNotCallable()

    def __repr__(self) -> str:
        ret = f"BetterStrings(inp='{self.string}'"

        for item in self.kwargs:
            if isinstance(self.kwargs[item], str):
                ret += f", {item}='{self.kwargs[item]}'"
            else:
                ret += f", {item}={self.kwargs[item]}"

        ret += ")"

        return ret
