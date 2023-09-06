from utils.substitution_algorithm import SubstitutionAlgorithm
from utils.cache_type import CacheType
from utils.addressed_type import AddressedType

import logging
import math
import random
import array 

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
        self._block_size: int = block_size * 8
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
 
        # Tamanho do indice (em Bits)
        self._index_length: int = int(math.log2(self._num_sets))
        # Tamanho da tag (em Bits)
        self._tag_length: int = int(self._address_length - self._offset - self._index_length)

        self._aux1 = self._index_length + self._offset
        self._aux2 = self._tag_length + self._offset
        self._aux3 = 2 ** self._index_length

        self._tables: list(dict[list[int], list[bool], list[int]]) = []
        for _ in range(self._associativity):
            self._tables.append({"TAG": [0 for _ in range(self._num_sets)], "VAL_BIT": [False for _ in range(self._num_sets)], "DATA": [0 for _ in range(self._num_sets)]})
        
        if self._substitution_algorithm == SubstitutionAlgorithm.FIFO:
            self.next_to_exit = [0 for _ in range(self._num_sets)]
        elif self._substitution_algorithm == SubstitutionAlgorithm.LRU:
            self.lru_aux = [[i for i in range(self._associativity)] for _ in range(self._num_sets)]
            #[0, 1, 2, 3] # assoc = 4

        self._accessed_addreses: list = list()
        
        self._hits: int = 0
        self._accesses: int = 0
        self._compulsory_misses: int = 0
        self._capacity_misses: int = 0
        self._conflict_misses: int = 0

    def __call__(self, address: int):
        return self.get(address)

    def set_upper_level(self, upper_level):
        self.upper_level = upper_level

    def get(self, address: int):
        """
        """
        #logging.info(f"Requested address {address}")

        tag = address >> self._aux1
        index = address << self._tag_length
        index = index >> (self._aux2)
        index = index % self._aux3

        compulsory_flag = True
        capacity_flag = True
        hit_flag = False
  
        self._accesses += 1

        data = None

        data_index = 0

        for i, tab in enumerate(self.tables):
            if tab["VAL_BIT"][index] == True:
                compulsory_flag = False
                if tab["TAG"][index] == tag:
                    self._hits += 1
                    hit_flag = True
                    data_index = i
                    data = tab["DATA"][index]
                    break
            else:
                capacity_flag = False

        if hit_flag == False:
            if compulsory_flag:
                self._compulsory_misses += 1
            elif capacity_flag == True:
                self._capacity_misses += 1
            else:
                self._conflict_misses += 1
            
            return self.__handle_miss(address, tag, index)

        if self._substitution_algorithm == SubstitutionAlgorithm.LRU:
            for i, _ in enumerate(self.lru_aux[index]):
                self.lru_aux[index][i] += 1
            self.lru_aux[index][data_index] = 0

        return data 

    def __handle_miss(self, address: int, tag: int, index:int):
        data = self.upper_level(address)

        if self._substitution_algorithm == SubstitutionAlgorithm.RANDOM:
            num = random.randrange(0, self._associativity)
            self._tables[num]["TAG"][index] = tag
            self._tables[num]["VAL_BIT"][index] = True
            self._tables[num]["DATA"][index] = data

        elif self._substitution_algorithm == SubstitutionAlgorithm.FIFO:
            self._tables[self.next_to_exit[index]]["TAG"][index] = tag
            self._tables[self.next_to_exit[index]]["VAL_BIT"][index] = True
            self._tables[self.next_to_exit[index]]["DATA"][index] = data

            if self.next_to_exit[index] + 1 >= len(self._tables):
                self.next_to_exit[index] = 0
            else:
                self.next_to_exit[index] += 1

        elif self._substitution_algorithm == SubstitutionAlgorithm.LRU:
            # O MAIS USADO VAI TER VALOR 0
            # O MENOS USADO VAI TER VALOR SELF._ASSOCIATIVY - 1

            least_used_index = 0
            max_count = self.lru_aux[index][0]
            for i, val in enumerate(self.lru_aux[index]):
                if val > max_count:
                    least_used_index = i
                    max_count = val
                self.lru_aux[index][i] += 1 
            
            self.lru_aux[index][least_used_index] = 0
            self._tables[least_used_index]["TAG"][index] = tag
            self._tables[least_used_index]["VAL_BIT"][index] = True
            self._tables[least_used_index]["DATA"][index] = data

        return data

    def reset(self):
        """
        Resetando as variáveis para valor inicial
        """
        
        self._tables: list(dict[list[int], list[bool], list[int]]) = []
        for _ in range(self._associativity):
            self._tables.append({"TAG": [0 for _ in range(self._num_sets)], "VAL_BIT": [False for _ in range(self._num_sets)], "DATA": [0 for _ in range(self._num_sets)]})
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