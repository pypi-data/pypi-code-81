import base64

def e_url(s):
    ssb = s.encode("ascii") 
    base64_bytes = base64.b64encode(ssb) 
    base64_string = base64_bytes.decode("ascii") 
    strstr = base64_string.translate(str.maketrans('+/', '-_'))
    return strstr.rstrip('=') 

def d_url(s):
    strstr = s.translate(str.maketrans('+/', '-_'))
    le = len(s) + 10
    pad_right = strstr.ljust(le, '=')
    ret = base64.b64decode(pad_right).decode('utf-8')
    return ret