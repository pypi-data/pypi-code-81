import functools
import random
import time

PASSWORD_CHARACTER_SET = (
    '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!#$%&()*+,-.:;<=>?@[]^_`{|}~'  # nosec
)


def spinner(cycles: int = 10, *, frames_per_second: int = 10) -> None:
    """Print a spinner."""
    for i in range(0, cycles * 4):
        time.sleep(1 / frames_per_second)
        if i % 4 == 0:
            print('\r|', end='')
        elif i % 4 == 1:
            print('\r/', end='')
        elif i % 4 == 2:
            print('\r-', end='')
        else:
            print('\r\\', end='')
    print('\r|', end='')


def assumption_make():
    options = (
        'we have a can opener',
        'normal distribution',
        'that I exist',
        'air is diatomic',
        'that assumptions are dangerous',
        'coffee',
        'that all assumptions are invalid',
    )

    print('I\'ve assumed {}.'.format(random.choice(options)))  # nosec


def password_create(*, length: int = 15, character_set: str = PASSWORD_CHARACTER_SET) -> str:
    """Create a password of the given length using the given character_set."""
    return ''.join(random.choices(character_set, k=length))


def spin_until_done(func):
    """Show a spinner until the function is done."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import concurrent.futures

        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(spinner)
            function_submission = executor.submit(func, *args, **kwargs)
            # TODO: add some stop here to make sure that the spinner does not just keep running
            while not function_submission.done():
                spinner()
            return function_submission.result()

    return wrapper
