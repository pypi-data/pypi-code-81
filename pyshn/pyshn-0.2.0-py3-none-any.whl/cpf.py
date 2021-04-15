###################################################################################################
# Entry Point
###################################################################################################

def cpf(value: any, generate: bool = False, validate: bool = True):
    if not (isinstance(value, int) or isinstance(value, str)):
        raise _invalid_type(value, expected="number or string")

    cpf_ = __cpf(_parse(value, generate))

    if validate and not cpf_:
        raise _invalid_number(value)
    else:
        return cpf_

###################################################################################################
# Helpers
###################################################################################################

def _calc(digits: str):
    mod = sum(int(x) * y for x, y in zip(digits, range(len(digits) + 1, 1, -1))) % 11
    return 0 if mod < 2 else 11 - mod

def _digits(value: int):
    return ''.join([d for d in value if d.isdigit()])

def _parse(value: any, generate: bool) -> str:
    func = None

    if isinstance(value, int):
        func = _generate_from_number if generate else _parse_from_number
    else:
        func = _generate_from_string if generate else _parse_from_string
    
    return func(value)

def _generate_from_string(value: str) -> str:
    def nine():
        if value.isnumeric():
            return value
        raise _invalid_format(value)

    def eleven():
        if value[3] == '.' and value[7] == '.':
            return _digits(value)
        raise _invalid_format(value)

    try:
        value = { 9: nine, 11: eleven }[len(value)]()
    except KeyError:
        raise _invalid_format(value)

    value += str(_calc(value))
    value += str(_calc(value))

    return value

def _generate_from_number(value: int) -> str:
    if 1 < value > 999_999_999:
        raise _invalid_range(value, end=999_999_999)
    else:
        return _generate_from_string(f"{value:0>9}")

def _parse_from_string(value: str) -> str:
    def eleven():
        if value.isnumeric():
            return value
        raise _invalid_format(value)

    def twelve():
        if value[9] == '/':
            return _digits(value)
        raise _invalid_format(value)

    def fourteen():
        if value[3] == '.' and value[7] == '.' and value[11] == '-':
            return _digits(value)
        raise _invalid_format(value)

    try:
        return { 11: eleven, 12: twelve, 14: fourteen }[len(value)]()
    except KeyError:
        raise _invalid_format(value)

def _parse_from_number(value: int) -> str:
    if 1 < value >  99_999_999_999:
        raise _invalid_range(value, end=99_999_999_999)
    else:
        return f"{value:0>11}"

###################################################################################################
# Errors
###################################################################################################

class CpfError(BaseException):
    pass

def _invalid_type(value: any, expected: str = "any"):
    return TypeError(f"argument must be {expected}, not '{type(value)}'.")

def _invalid_range(value: any, begin: int = 1, end: int = 99_999_999_999):
    return CpfError(f"argument range must be between {begin} and {end}, its {value}.")

def _invalid_format(value: any):
    return CpfError(f"invalid format '{value}'.")

def _invalid_number(value: any):
    return CpfError(f"invalid number '{value}'.")

###################################################################################################
# CPF Class
###################################################################################################

class __cpf(object):
    _number: int

    def __init__(self, number: int):
        self._number = int(number)

    def __bool__(self):
        n = f"{self._number:0>11}"
        return len(set(n)) != 1 and _calc(n[:-2]) == int(n[9]) and _calc(n[:-1]) == int(n[10])

    def __int__(self):
        return self._number

    def __str__(self):
        return format(self)

    def __repr__(self):
        return f"<cpf {self._number:0>11}>"

    def __format__(self, format_spec):
        n = f"{self._number:0>11}"
        if format_spec == '':
            return f"{n[:3]}.{n[3:6]}.{n[6:9]}-{n[9:]}"                
        if format_spec == 'n':
            return n        
        if format_spec == 'N':
            return f"{n[:9]}/{n[9:]}"
        raise ValueError(f"Invalid format specifier")