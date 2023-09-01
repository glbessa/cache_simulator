from cache_type import CacheType

class CacheLevel:
    def __init__(self, level: list):
        if len(level) == 1:
            self.instruction_cache = level[0]
            self.data_cache = level[0]
            self.cache_type = CacheType.UNIFIED
        elif len(level) == 2:
            self.instruction_cache = level[0]
            self.data_cache = level[1]
            self.cache_type = CacheType.SEPARETED
        else:
            raise Exception("CacheLevel Error")

    def reset(self):
        self.instruction_cache.reset()
        self.data_cache.reset()
