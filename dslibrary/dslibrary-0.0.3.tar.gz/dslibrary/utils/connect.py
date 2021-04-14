

def connect_to_database(path: str, library: str=None, for_write: bool=False, **kwargs):
    """
    Try, by various means, to connect to a database.

    :param path:        URI of database.
    :param library:     A specific library to use, if available
    :param for_write:   Whether to enable write operations.
    """
    # determine flavor of connection and work out which libraries to try
    libraries = []
    if library:
        libraries.append(library)
    path_parts = path.split(":")
    if path_parts[0] == "jdbc":
        path_parts = path_parts[1:]
    if path_parts[0] in ("postgres", "postgresql"):
        libraries.append("psycopg2")
    if path_parts[0] == "mysql":
        libraries.append("pymysql")
    libraries.append("JayDeBeApi")
    for lib in libraries:
        method = f"_connect_{lib}"
        if method in locals():
            conn = locals()[method](path=path, **kwargs)
            if conn:
                return conn


def _connect_psycopg2(path, **kwargs):
    try:
        import psycopg2
    except ImportError:
        return
    dsn = ""
    # TODO split up path to get host, port, database, also need username, password
    return psycopg2.connect(dsn)


# TODO pymysql
# TODO JayDeBeApi
# TODO sqlite3, but we have to resolve the file's location
