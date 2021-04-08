from .bcrypt import BCryptScheme
from AuthEncoding import registerScheme


registerScheme('BCRYPT', BCryptScheme())
