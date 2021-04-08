class _BaseClient:
    def __init__(self, public_key):
        self.public_key = public_key

    @property
    def signature_header(self):
        return self.public_key
