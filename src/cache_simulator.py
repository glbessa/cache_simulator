from cache import Cache
from cache_level import CacheLevel
from memory_architecture import MemoryArchitecture
from substitution_algorithm import SubstitutionAlgorithm

import sys

try:
    from tqdm import tqdm
except ModuleNotFoundError as ex:
    print(ex)

class CacheSimulator:
    def __init__(self, architecture: MemoryArchitecture):

        # Tamanho do endereço em Bytes (4 Bytes = 32 bits)
        self.address_length: int = 4
        # Lista de endereços lidos em formato binário
        self.addresses: list = list()

        self.architecture: MemoryArchitecture = architecture

    def simulate(self):
        try:
            for addr in tqdm(self.addresses):
                self.architecture(addr)
        except:
            for addr in tqdm(self.addresses):
                self.architecture(addr)

    def read_input_file(self, filename):
        """
        Método irá receber arquivo binário contendo os endereços
        requisitos a cache, cada endereço com 32 bits em formato big endian
        """

        with open(filename, 'rb') as reader:
            chunk = reader.read(self.address_length)

            while chunk:
                self.addresses.append(int.from_bytes(chunk, 'big'))
                chunk = reader.read(self.address_length)

    def print_raw_outputs(self):
        print(f"{self.architecture[0].instruction_cache.accesses}", end=" ")
        print(f"{round(self.architecture[0].instruction_cache.hits/self.architecture[0].instruction_cache.accesses, 4)}", end=" ")
        print(f"{round(self.architecture[0].instruction_cache.misses/self.architecture[0].instruction_cache.accesses, 4)}", end=" ")
        print(f"{round(self.architecture[0].instruction_cache.compulsory_misses/self.architecture[0].instruction_cache.misses, 4)}", end=" ")
        print(f"{round(self.architecture[0].instruction_cache.capacity_misses/self.architecture[0].instruction_cache.misses, 4)}", end=" ")
        print(f"{round(self.architecture[0].instruction_cache.conflict_misses/self.architecture[0].instruction_cache.misses, 4)}")

    def print_styled_outputs(self):
        print(f"Acessos                  = {self.architecture[0].instruction_cache.accesses}")
        print(f"Taxa de hit              = {self.architecture[0].instruction_cache.hits/self.architecture[0].instruction_cache.accesses}%")
        print(f"Taxa de miss             = {self.architecture[0].instruction_cache.misses/self.architecture[0].instruction_cache.accesses}%")
        print(f"Taxa de miss COMPULSORIO = {self.architecture[0].instruction_cache.compulsory_misses/self.architecture[0].instruction_cache.accesses}%")
        print(f"Taxa de miss CAPACIDADE  = {self.architecture[0].instruction_cache.capacity_misses/self.architecture[0].instruction_cache.accesses}%")
        print(f"Taxa de miss CONFLITO    = {self.architecture[0].instruction_cache.conflict_misses/self.architecture[0].instruction_cache.accesses}%")




def print_help():
    print("usage: python cache_simulator.py <num_sets> <block_size> <associativy> <subst_algorithm> <output_flag> <input_filename>")
    print("\targ[1]: num_sets (Número de Conjuntos)")
    print("\targ[2]: block_size (Tamanho do bloco em bytes)")
    print("\targ[3]: associativity (Grau de associatividade)")
    print("\targ[4]: subst_algorithm (Algoritmo de Substituição: L - LRU, R - RANDOM, F - FIFO)")
    print("\targ[5]: output_flag (Modo de saída: 0 - Output com informações, 1 - Raw output)")
    print("\targ[6]: input_filename (Path do arquivo de input)")

def main():
    try:
        num_sets = int(sys.argv[1])
        block_size = int(sys.argv[2])
        associativity = int(sys.argv[3])
        subst_algorithm = sys.argv[4]
        output_flag = int(sys.argv[5])
        input_filename = sys.argv[6]
    except ValueError as ex:
        print_help()
        return

    subst = None

    if subst_algorithm.upper() == "F":
        subst = SubstitutionAlgorithm.FIFO
    elif subst_algorithm.upper() == "L":
        subst = SubstitutionAlgorithm.LRU
    elif subst_algorithm.upper() == "R":
        subst = SubstitutionAlgorithm.RANDOM
    else:
        print_help()
        return
        

    arch = MemoryArchitecture([
        CacheLevel([
            Cache(num_sets, block_size, associativity, subst)
        ])
    ])

    cache_simulator = CacheSimulator(arch)
    cache_simulator.read_input_file(input_filename)
    cache_simulator.simulate()

    if output_flag == 1:
        cache_simulator.print_raw_outputs()
    else:
        cache_simulator.print_styled_outputs()
    

if __name__ == "__main__":
    main()
