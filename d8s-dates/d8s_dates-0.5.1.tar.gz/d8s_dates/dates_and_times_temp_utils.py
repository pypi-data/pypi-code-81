"""Utility functions temporarily provided until the rest of the democritus functions get uploaded."""


def number_zero_pad(num: int, length: int) -> str:
    """."""
    if length < len(str(num)):
        message = (
            'The length you provided is shorter than the number. '
            + 'Please provide a length that is at least as long as the given number.'
        )
        raise ValueError(message)

    zero_padded_number = f'{num}'

    while len(zero_padded_number) < length:
        zero_padded_number = f'0{zero_padded_number}'

    return zero_padded_number


def string_remove_from_end(input_string, string_to_remove):
    """Remove the string_to_remove from the end of the input_string."""
    if input_string.endswith(string_to_remove):
        desired_string_final_index = len(input_string) - len(string_to_remove)
        updated_string = input_string[:desired_string_final_index]
        return updated_string
    else:
        return input_string
