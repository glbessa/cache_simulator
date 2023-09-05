from cache import Cache
from utils import Utils
from memory_architecture import MemoryArchitecture
from cache_level import CacheLevel
from substitution_algorithm import SubstitutionAlgorithm

import sys
from tqdm import tqdm

class CacheSimulator:
    def __init__(self, architecture: MemoryArchitecture):
        # Tamanho do endereço em Bytes (4 Bytes = 32 bits)
        self.address_length: int = 4
        # Lista de endereços lidos em formato binário
        self.addresses: list = list()

        self.architecture: MemoryArchitecture = architecture

    def simulate(self):
        for addr in tqdm(self.addresses):
            self.architecture(addr)

        # self.print_raw_outputs()
        self.print_bonito()

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

    # Total de acessos, Taxa de hit, Taxa de miss, Taxa de miss compulsório, Taxa de miss de capacidade, Taxa de miss de conflito

    def print_raw_outputs(self):
        print(f"{self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{self.architecture[0].instruction_cache.hits/self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{self.architecture[0].instruction_cache.misses/self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{self.architecture[0].instruction_cache.compulsory_misses/self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{self.architecture[0].instruction_cache.capacity_misses/self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{self.architecture[0].instruction_cache.conflict_misses/self.architecture[0].instruction_cache.accesses}")

    def print_bonito(self):
        print(f"Acessos = {self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de hit = {self.architecture[0].instruction_cache.hits/self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de miss = {self.architecture[0].instruction_cache.misses/self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de miss COMPULSORIO = {self.architecture[0].instruction_cache.compulsory_misses/self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de miss CAPACIDADE = {self.architecture[0].instruction_cache.capacity_misses/self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de miss CONFLITO = {self.architecture[0].instruction_cache.conflict_misses/self.architecture[0].instruction_cache.accesses}")

if __name__ == "__main__":
    num_sets = int(sys.argv[1])
    block_size = int(sys.argv[2])*8
    associativity = int(sys.argv[3])
    subst_algorithm = sys.argv[4]
    output_flag = sys.argv[5]
    input_filename = sys.argv[6]

    arch = MemoryArchitecture([
        CacheLevel([
            Cache(num_sets, block_size, associativity, SubstitutionAlgorithm.FIFO)
        ])
    ])

    cache_simulator = CacheSimulator(arch)
    cache_simulator.read_input_file(input_filename)
    cache_simulator.simulate()