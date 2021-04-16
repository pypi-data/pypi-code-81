import hashlib
import base64

def sha256(value):
    """Hashes the string and returns that hash value

    Arguments:
    value -- value to be hashed
    """
    
    if not value or value == '':
        raise ValueError({ "Error": "Value does not exist or does not contain any character!" })
    
    try:
        return base64.b64encode(hashlib.sha256(value.encode('utf-8')).digest()).decode('utf-8')
    except Exception as e:
        raise ValueError({ "Error": "Some error occured during hashing process!" })