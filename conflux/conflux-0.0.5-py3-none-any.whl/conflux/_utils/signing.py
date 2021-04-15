from cytoolz import (
    pipe,
)
from eth_utils import (
    to_bytes,
    to_int,
)
from .transactions import (
    encode_transaction,
    serializable_unsigned_transaction_from_dict,
)
CHAIN_ID_OFFSET = 35
V_OFFSET = 27

# signature versions
PERSONAL_SIGN_VERSION = b'E'  # Hex value 0x45
INTENDED_VALIDATOR_SIGN_VERSION = b'\x00'  # Hex value 0x00
STRUCTURED_DATA_SIGN_VERSION = b'\x01'  # Hex value 0x01

def sign_transaction_dict(eth_key, transaction_dict):
    # generate RLP-serializable transaction, with defaults filled
    unsigned_transaction = serializable_unsigned_transaction_from_dict(transaction_dict)

    transaction_hash = unsigned_transaction.hash()

    # sign with private key
    (v, r, s) = sign_transaction_hash(eth_key, transaction_hash)

    # serialize transaction with rlp
    encoded_transaction = encode_transaction(unsigned_transaction, vrs=(v, r, s))

    return (v, r, s, encoded_transaction)

def extract_chain_id(raw_v):
    """
    Extracts chain ID, according to EIP-155
    @return (chain_id, v)
    """
    above_id_offset = raw_v - CHAIN_ID_OFFSET
    if above_id_offset < 0:
        if raw_v in {0, 1}:
            return (None, raw_v + V_OFFSET)
        elif raw_v in {27, 28}:
            return (None, raw_v)
        else:
            raise ValueError("v %r is invalid, must be one of: 0, 1, 27, 28, 35+")
    else:
        (chain_id, v_bit) = divmod(above_id_offset, 2)
        return (chain_id, v_bit + V_OFFSET)

def sign_transaction_hash(key, transaction_hash):
    signature = key.sign_msg_hash(transaction_hash)
    return signature.vrs

def _pad_to_eth_word(bytes_val):
    return bytes_val.rjust(32, b'\0')

def to_bytes32(val):
    return pipe(
        val,
        to_bytes,
        _pad_to_eth_word,
    )

def to_standard_v(enhanced_v):
    (_chain, chain_naive_v) = extract_chain_id(enhanced_v)
    v_standard = chain_naive_v - V_OFFSET
    assert v_standard in {0, 1}
    return v_standard

def to_standard_signature_bytes(ethereum_signature_bytes):
    rs = ethereum_signature_bytes[:-1]
    v = to_int(ethereum_signature_bytes[-1])
    standard_v = to_standard_v(v)
    return rs + to_bytes(standard_v)

def sign_message_hash(key, msg_hash):
    signature = key.sign_msg_hash(msg_hash)
    (v, r, s) = signature.vrs
    eth_signature_bytes = to_bytes32(r) + to_bytes32(s) + to_bytes(v)
    return (v, r, s, eth_signature_bytes)
