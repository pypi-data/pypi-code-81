try:
    from gask.start.start_prog import first_check
except ImportError:
    from start.start_prog import first_check


def main():
    first_check()


if __name__ == "__main__":
    main()
