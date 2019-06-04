def bytes_to_bit_rep(string: bytes) -> str:
    """Converts a bytes object into the concatenation of its bit values.

    This method iterates over all the bytes contained in the input object and
    extracts their binary representation, 0-padded to 8 bits. The bits are then
    concatenated into a single string.

    :param string: The bytes object to convert.
    :return: A single string that is the concatenation of the bits from the
    bytes in the input object.

    >>> bytes_to_bit_rep(bytes("a", "UTF-8"))
    '01100001'
    >>> bytes_to_bit_rep(bytes("foo", "UTF-8"))
    '011001100110111101101111'
    """
    return ''.join([f"{ch:08b}" for ch in string])


def bit_rep_to_bytes(bit_rep: str) -> bytes:
    """Converts a concatenation of bits into the corresponding bytes object.

    This method receives a string consisting in binary values and divides it in
    order to obtain the corresponding bytes object. The string is sliced into
    groups of 8 bits, converted to individual bytes and then aggregated in a
    bytes object.

    :param bit_rep: The bit concatenation to convert, stored in a string.
    :return: The bytes object that results from dividing the binary
    representation string into chunks of 8 bits.

    >>> bit_rep_to_bytes('01100001')
    b'a'
    >>> bit_rep_to_bytes('011001100110111101101111')
    b'foo'
    """
    string = bytes("", "UTF-8")
    # Split input string into 8-bit chunks
    byte_array = [bit_rep[i:i+8] for i in range(0, len(bit_rep), 8)]
    for byte in byte_array:
        # Convert to characters and add to existing bytes object
        string += bytes(f"{chr(int(byte, 2))}", "UTF-8")
    return string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
