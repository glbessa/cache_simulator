class Utils:
    @staticmethod
    def big_endian2little_endian(word: bytes) -> bytes:
        return bytes(bytearray(word)[::-1])