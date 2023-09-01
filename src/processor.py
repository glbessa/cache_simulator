class Processor:
    """
    This class will identify if the address points to an instruction or to a data
    """
    def __init__(self, instruction_range: tuple = None, data_range: tuple = None):
        pass

    def __call__(self):
        if not instruction_range and not data_range:
            # Assume that its first level is unified
            
