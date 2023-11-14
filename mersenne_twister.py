"""Mersenne Twister random number generator."""

import time

class MersenneTwister(object):
    """Mersenne Twister random number generator."""
    
    def __init__(self, seed: int = int(time.time()), n: int = 624) -> None:
        """Initialize the generator from a seed.
        
        :param seed: Seed for the generator. Defaults to current timestamp.
        :param n: Size of the generator. Defaults to 624.
        """
        self.n = n
        self.MT = [0] * self.n
        self.index = 0
        self._init_genrand(seed)
        
    def _init_genrand(self, seed: int) -> None:
        """Initialize the generator from a seed.
        
        :param seed: Seed for the generator.
        """
        self.MT[0] = seed
        for i in range(1, self.n):
            self.MT[i] = 1812433253 * (self.MT[i-1] ^ (self.MT[i-1] >> 30)) + i
            self.MT[i] = self.MT[i] & 0xffffffff

    def _generate_numbers(self) -> None:
        """Generate an array of N untempered numbers (624 by default)."""
        for i in range(self.n):
            y = (self.MT[i] & 0x80000000) + (self.MT[(i+1) % self.n] & 0x7fffffff)
            self.MT[i] = self.MT[(i + 397) % self.n] ^ (y >> 1)
            if y % 2 != 0:
                self.MT[i] = self.MT[i] ^ 2567483615
    
    def _extract_number(self) -> int:
        """Extract a tempered pseudorandom number based on the index-th value,
        calling generate_numbers() every N numbers (624 by default).
        
        :return: Random number.
        """
        if self.index == 0:
            self._generate_numbers()
            
        y = self.MT[self.index]
        y = y ^ (y >> 11)
        y = y ^ ((y << 7) & 2636928640)
        y = y ^ ((y << 15) & 4022730752)
        y = y ^ (y >> 18)
    
        self.index = (self.index + 1) % self.n

        return y

    def get_random_int(self, min: int = 0, max: int = 0xffffffff) -> int:
        """Extract a random integer between a specific range
        :param min: Minimum value. Defaults to 0.
        :param max: Maximum value. Defaults to 0xffffffff.

        :return: Random integer value in between the range of [min,max].
        """
        if min > max:
            min, max = max, min

        range_size = max - min + 1
        random_number = self._extract_number() % range_size

        return min + random_number
    
    def get_random_float(self) -> None:
        """Extract a random number between 0 and 1."""
        return self._extract_number() / 0xffffffff

    
if __name__ == '__main__':
    mt = MersenneTwister()
    for i in range(50):
        print(f"Random int: {mt.get_random_int()}")
        print(f"Random float: {mt.get_random_float()}")
