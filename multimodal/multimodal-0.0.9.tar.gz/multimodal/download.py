import argparse


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--dir-data", requried=True)

    args = parser.parse_args()
    