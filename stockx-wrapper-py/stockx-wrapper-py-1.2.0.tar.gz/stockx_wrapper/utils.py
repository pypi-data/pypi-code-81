import math


def split_number_into_chunks(number_to_split, chunk_length):

    _div = math.ceil(number_to_split / chunk_length)

    chunks = [min(chunk_length, number_to_split-(i*chunk_length)) for i in range(_div)]

    return chunks
