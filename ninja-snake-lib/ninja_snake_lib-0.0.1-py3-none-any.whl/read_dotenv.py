import os


class ReadDotenv:

    @staticmethod
    def read_dotenv(base_dir=None):
        fname = ".env"
        if base_dir:
            fname = os.path.join(base_dir, ".env")

        try:

            if os.path.exists(fname):
                with open(fname, "r") as file:
                    for line in file:
                        if not line or len(line) < 2 or line.find("=") == -1 or \
                                line.startswith("#"):
                            continue
                        property, value = line.strip().split("=", 1)
                        os.environ.setdefault(property, value)
        except Exception as ex:
            pass
