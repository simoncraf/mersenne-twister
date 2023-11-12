"""Mersenne Twister random number generator."""

import time

class MersenneTwister(object):
    """Mersenne Twister random number generator."""
    
    def __init__(self, seed: int = int(time.time()), n: int = 624) -> None:
        """Initialize the generator from a seed.
        
        :param seed: seed for the generator.
        :param n: size of the generator.
        """
        self.n = n
        self.MT = [0] * self.n
        self.index = 0
        self._init_genrand(seed)
        
    def _init_genrand(self, seed: int) -> None:
        """Initialize the generator from a seed.
        
        :param seed: seed for the generator.
        """
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = 1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i
            self.MT[i] = self.MT[i] & 0xffffffff
    
    def extract_number(self) -> int:
        """Extract a tempered pseudorandom number based on the index-th value,
        calling generate_numbers() every N numbers (624 by default).
        
        :return: a random number.
        """
        if self.index == 0:
            self.generate_numbers()
            
        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 2636928640)
        y = y ^ ((y << 15) & 4022730752)
        y = y ^ (y >> 18)
    
        self.index = (self.index + 1) % self.n
        return y
    
    def generate_numbers(self) -> None:
        """Generate an array of N untempered numbers (624 by default)."""
        for i in range(self.n):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % self.n] & 0x7fffffff)
            self.MT[i] = self.MT[(i + 397) % self.n] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] = self.MT[i] ^ 2567483615

    
if __name__ == '__main__':
    mt = MersenneTwister()
    for i in range(50):
        print(mt.extract_number())
    