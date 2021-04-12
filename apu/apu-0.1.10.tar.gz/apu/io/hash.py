""" create hashcode for files """

from hashlib import md5, sha224, sha256, sha384, sha1, sha512

BUF_SIZE = 65636

# switch for different hashtypes
DIGITS = {
    "md5": lambda file: _calc_(file, md5()),
    "sha224": lambda file: _calc_(file, sha224()),
    "sha1": lambda file: _calc_(file, sha1()),
    "sha256": lambda file: _calc_(file, sha256()),
    "sha384": lambda file: _calc_(file, sha384()),
    "sha512": lambda file: _calc_(file, sha512()),
}

def _calc_(file, hash_func):
    """ calculate the file hash oh a file """
    hash_code = hash_func

    try:
        #open the file
        with open(file, "rb") as file_for_finger_printing:
            # read the file and build hash
            while True:
                data = file_for_finger_printing.read(BUF_SIZE)
                if not data:
                    break
                hash_code.update(data)

        return hash_code
    except Exception as err: # pylint: disable=W0703
        print(str(err))
        return None
