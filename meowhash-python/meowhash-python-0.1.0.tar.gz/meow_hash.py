import cpufeature, meow_hash_ext


REQUIRED_SIMD_FEATURES = {
    'AES',
    'SSE',
    'SSE2',
    'SSE3',
    'SSSE3',
    'SSE4.1'
}


class MeowHash:
    """
    128 bit hash
    """
    def __init__(self, bytes_: bytes):
        for feature in REQUIRED_SIMD_FEATURES:
            if not cpufeature.CPUFeature[feature]:
                raise RuntimeError(
                    f'CPU does not support SIMD feature "{feature}"'
                )
        self.hash_result = meow_hash_ext.digest(bytes_)
    
    def __str__(self):
        hash_ = self.hexdigest()
        return f'{hash_[:8]}-{hash_[8:16]}-{hash_[16:24]}-{hash_[24:]}'
    
    def __repr__(self):
        return str(self)
    
    def __format__(self, _):
        return str(self)

    def hexdigest(self):
        return hex(self.hash())[2:].upper()

    def digest(self):
        return self.hash_result

    def hash(self):
        return int.from_bytes(self.hash_result, byteorder='little')

    def __int__(self):
        return self.hash()


def meow_hash(bytes_: bytes) -> MeowHash:
    if isinstance(bytes_, str):
        assert False, 'Unicode-objects must be encoded before hashing'
    assert isinstance(bytes_, bytes), 'Can only hash bytes'
    return MeowHash(bytes_)
