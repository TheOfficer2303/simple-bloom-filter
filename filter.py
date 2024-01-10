from abc import ABC, abstractmethod
import math

import mmh3
from my_bitmap import MyBitMap

class Filter(ABC):
  def __init__(self, nbits: int, nhashes: int) -> None:
    self.bitmap = MyBitMap(nbits)
    self.nbits = nbits
    self.nhashes = nhashes

  @abstractmethod
  def _h(self, element) -> None:
    raise NotImplementedError

  @abstractmethod
  def insert(self, element) -> None:
    raise NotImplementedError

  @abstractmethod
  def lookup(self, element) -> bool:
    raise NotImplementedError

class BloomFilter(Filter):
  def __init__(self, nbits: int, nhashes) -> None:
    super().__init__(nbits, nhashes)

  def _h(self, element) -> None:
    return mmh3.hash(element)

  def _get_indices_for_element(self, element) -> list[int]:
    hashes: list[int] = [self._h(element) for _ in range(self.nhashes)]
    return [int(math.fabs(h)) % self.nbits for h in hashes]

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
