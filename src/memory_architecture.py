from main_memory import MainMemory

class MemoryArchitecture:
    def __init__(self,
                 levels: list,
                 instruction_range: tuple = None,
                 data_range: tuple = None):
        self.instruction_range = instruction_range
        self.data_range = data_range

        self.arch = levels
        self.arch.append(MainMemory())
        
        for i in range(0, len(self.arch) - 2):
            self.arch[i].instruction_cache.set_upper_level(self.arch[i + 1].instruction_cache)
            self.arch[i].data_cache.set_upper_level(self.arch[i + 1].data_cache)

        
        self.arch[-2].instruction_cache.set_upper_level(self.arch[-1])
        self.arch[-2].data_cache.set_upper_level(self.arch[-1])

    def __call__(self,
                 address):
        if not self.instruction_range and not self.data_range:
            # Assume that its first level is unified
            self.arch[0].instruction_cache(address)

    def __getitem__(self, index):
        return self.arch[index]

    def reset(self):
        for level in self.arch[:-1]:
            level.reset()
    