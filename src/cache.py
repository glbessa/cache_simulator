from substitution_algorithm import SubstitutionAlgorithm
from cache_type import CacheType
from addressed_type import AddressedType

import logging
import math
import random

class Cache:
    def __init__(self, num_sets: int, block_size: int, associativity: int, subst_algorithm: SubstitutionAlgorithm, name: str = "Cache", upper_level = None):
        self.name = name
        # Nível da cache (L1 / L2)
        self._cache_level: int = 1
        # Tipo da Cache (unificada)
        self._cache_type: CacheType = CacheType.UNIFIED
        # Tamanho do endereco em bits
        self._address_length: int = 32
        # Tipo de enderecamento
        self._adressed_by: AddressedType = AddressedType.BYTE
        # Tamanho da palavra em bits
        self._word_length: int = 32
        # Upper level
        self._upper_level = upper_level


        # Numero de conjuntos da cache
        self._num_sets: int = num_sets
        # Tamanho do bloco (em bits)
        self._block_size: int = block_size
        # Grau de associatividade
        self._associativity: int = associativity
        # Algoritmo de substituição escolhido
        self._substitution_algorithm: SubstitutionAlgorithm = subst_algorithm
        # Tamanho total da cache (nsets * block_size * aasoc )
        self._cache_size = self._num_sets * self._block_size * self._associativity
        
        if self._adressed_by == AddressedType.WORD:
            self._offset: int = int(math.log2(self._block_size / self._word_length))
        else:
            self._offset: int = int(math.log2(self._block_size / 8))

        # Tamanho da tag (em Bits)
        self._index_length: int = int(math.log2(self._num_sets))
        # Tamanho da tag (em Bits)
        self._tag_length: int = int(self._address_length - self._offset - self._index_length)

        self._tables: list(dict[list[bytes], list[bool], list[bytes]]) = []
        for _ in range(self._associativity):
            self._tables.append({"TAG": [bytes(0) for _ in range(self._num_sets)], "VAL_BIT": [False for _ in range(self._num_sets)], "DATA": [bytes(0) for _ in range(self._num_sets)]})
        
        self._accessed_addreses: list = list()
        
        self._hits: int = 0
        self._accesses: int = 0
        self._compulsory_misses: int = 0
        self._capacity_misses: int = 0
        self._conflict_misses: int = 0

    def __call__(self, address: bytes):
        return self.get(address)

    def set_upper_level(self, upper_level):
        self.upper_level = upper_level

    def get(self, address: bytes):
        """
        """
        logging.info(f"Requested address {address}")

        tag = bytes(int.from_bytes(address, byteorder='little') >> (self._index_length + self._offset))
        index = int.from_bytes(address, byteorder='little') << self._tag_length
        index = index >> (self._tag_length + self._offset)
        index = index % (2 ** self._index_length)

        compulsory_flag = True
        capacity_flag = True
        hit_flag = False
        # [
        #     {
        #         valbit : [indice] -> 0 ou 1 
        #     },
        #     {

        #     },
        #     {

        #     },
        # ]
        self._accesses += 1
        self._accessed_addreses.append(address)

        for tab in self.tables:
            if tab["VAL_BIT"][index] == True:
                compulsory_flag = False
                if tab["TAG"][index] == tag:
                    self._hits += 1
                    hit_flag = True
                    break
            else:
                capacity_flag = False

        if hit_flag == False:
            if compulsory_flag == True:
                self._compulsory_misses += 1
            elif capacity_flag == True:
                self._capacity_misses += 1
            else:
                self._conflict_misses += 1
            
            self.__handle_miss(address)

    def __handle_miss(self, address: bytes):
        tag = bytes(int.from_bytes(address, byteorder='little') >> (self._index_length + self._offset))
        index = int.from_bytes(address, byteorder='little') << self._tag_length
        index = index >> (self._tag_length + self._offset)
        index = index % (2 ** self._index_length)

        data = self.upper_level(address)

        if self._substitution_algorithm == SubstitutionAlgorithm.RANDOM:
            num = random.randrange(0, self._associativity)
            self._tables[num]["TAG"][index] = bytes(tag)
            self._tables[num]["VAL_BIT"][index] = True
            self._tables[num]["DATA"] = data

        elif self._substitution_algorithm == SubstitutionAlgorithm.FIFO:
            return

        else:
            return

    def reset(self):
        """
        Resetando as variáveis para valor inicial
        """
        
        self._table = {"TAG": list(), "VAL_BIT": list(), "DATA": list()}
        self._hits: int = 0
        self._accesses: int = 0
        self._compulsory_misses: int = 0
        self._capacity_misses: int = 0
        self._conflict_misses: int = 0
    
    @property
    def tables(self) -> list:
        return self._tables

    @property
    def misses(self) -> int:
        return self.compulsory_misses + self.capacity_misses + self.conflict_misses

    @property
    def hits(self) -> int:
        return self._hits

    @property
    def accesses(self) -> int:
        return self.misses + self.hits

    @property
    def compulsory_misses(self) -> int:
        return self._compulsory_misses
        
    @property
    def capacity_misses(self) -> int:
        return self._capacity_misses
        
    @property
    def conflict_misses(self) -> int:
        return self._conflict_misses