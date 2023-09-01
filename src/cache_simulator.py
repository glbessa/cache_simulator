from cache import Cache
from utils import Utils
from memory_architecture import MemoryArchitecture
from cache_level import CacheLevel
from substitution_algorithm import SubstitutionAlgorithm

import sys

class CacheSimulator:
    def __init__(self, architecture: MemoryArchitecture):
        # Tamanho do endereço em Bytes (4 Bytes = 32 bits)
        self.address_length: int = 4
        # Lista de endereços lidos em formato binário
        self.addresses: list = list()

        self.architecture: MemoryArchitecture = architecture

    def simulate(self):
        for addr in self.addresses:
            self.architecture(addr)

        print(self.architecture[0].instruction_cache._hits / self.architecture[0].instruction_cache._accesses)

    def read_input_file(self, filename):
        """
        Método irá receber arquivo binário contendo os endereços
        requisitos a cache, cada endereço com 32 bits em formato big endian
        """

        with open(filename, 'rb') as reader:
            chunk = reader.read(self.address_length)

            while chunk:
                self.addresses.append(Utils.big_endian2little_endian(chunk))
                chunk = reader.read(self.address_length)


if __name__ == "__main__":
    num_sets = int(sys.argv[1])
    block_size = int(sys.argv[2])
    associativity = int(sys.argv[3])
    subst_algorithm = sys.argv[4]
    output_flag = sys.argv[5]
    input_filename = sys.argv[6]

    arch = MemoryArchitecture([
        CacheLevel([
            Cache(num_sets, block_size, associativity, SubstitutionAlgorithm.RANDOM)
        ])
    ])

    cache_simulator = CacheSimulator(arch)
    cache_simulator.read_input_file(input_filename)
    cache_simulator.simulate()