import datetime as _datetime

class timestamp:
    """
    horário da execução
    """
    def __init__(self):

        dtt_now = _datetime.datetime.now()
        self.str_yyyymmdd = dtt_now.strftime('%Y%m%d')
        self.str_hhmmss = dtt_now.strftime('%H%M%S')
        self.str_full = dtt_now.strftime('%Y-%m-%d %H:%M:%S')
        self.dtt_timestamp = dtt_now.timestamp()
        self.dtt_now = dtt_now