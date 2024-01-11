from abc import ABC, abstractmethod
import math
from random import randint

import mmh3
from my_bitmap import MyBitMap

class Filter(ABC):
  def __init__(self, nbits: int, nhashes: int) -> None:
    self.bitmap = MyBitMap(nbits)
    self.nbits = nbits
    self.nhashes = nhashes

    self.seeds = [randint(0, 1000) for _ in range(nhashes)]

  def _get_indices_for_element(self, element) -> list[int]:
    hashes: list[int] = [self._h(element, self.seeds[i]) for i in range(self.nhashes)]
    return [int(math.fabs(h)) % self.nbits for h in hashes]

  def _h(self, element, seed: int) -> None:
    return mmh3.hash(element, seed)

  @abstractmethod
  def insert(self, element) -> None:
    raise NotImplementedError

  @abstractmethod
  def lookup(self, element) -> bool:
    raise NotImplementedError

class BloomFilter(Filter):
  def __init__(self, nbits: int, nhashes) -> None:
    super().__init__(nbits, nhashes)

  def insert(self, element: any) -> None:
    indices = self._get_indices_for_element(element)

    for i in range(self.nhashes):
      self.bitmap.set(indices[i])

  def lookup(self, element) -> bool:
    indices = self._get_indices_for_element(element)

    for index in indices:
      if self.bitmap.get(index) == 0:
        return False

    return True


class CountingBloomFilter(Filter):
  def __init__(self, nbits: int, nhashes: int) -> None:
    super().__init__(nbits, nhashes)
    self.counter = [0 for _ in range(nbits)]

  def insert(self, element) -> None:
    indices = self._get_indices_for_element(element)

    for index in indices:
      self.bitmap.set(index)
      self.counter[index] += 1

  def lookup(self, element) -> bool:
    indices = self._get_indices_for_element(element)

    for index in indices:
      if self.counter[index] == 0:
        return False

    return True

  def delete(self, element) -> None:
    indices = self._get_indices_for_element(element)

    for index in indices:
      if self.counter[index] > 0:
        self.bitmap.reset(index)
        self.counter[index] -= 1
