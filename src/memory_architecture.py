from main_memory import MainMemory
from cache_level import CacheLevel

class MemoryArchitecture:
    def __init__(self,
                 levels: list,
                 instruction_range: tuple = None,
                 data_range: tuple = None):
        self.instruction_range = instruction_range
        self.data_range = data_range

        self.arch = levels
        self.main_memory = MainMemory()
        
        for i in range(0, len(self.arch) - 1):
            self.arch[i].instruction_cache.set_upper_level(self.arch[i + 1].instruction_cache)
            self.arch[i].data_cache.set_upper_level(self.arch[i + 1].data_cache)

        
        self.arch[-1].instruction_cache.set_upper_level(self.main_memory)
        self.arch[-1].data_cache.set_upper_level(self.main_memory)

    def add(self, level:CacheLevel):
        self.arch[-1].instruction_cache.set_upper_level(level.instruction_cache)
        self.arch[-1].data_cache.set_upper_level(level.data_cache)

        level.instruction_cache.set_upper_level(self.main_memory)
        level.data_cache.set_upper_level(self.main_memory)

        self.arch.append(level)

    def __call__(self, address):
        if not self.instruction_range and not self.data_range:
            # Assume that its first level is unified
            self.arch[0].instruction_cache(address)

    def __getitem__(self, index):
        return self.arch[index]

    def reset(self):
        for level in self.arch:
            level.reset()
    