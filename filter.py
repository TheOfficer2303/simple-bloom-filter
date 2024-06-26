from abc import ABC, abstractmethod
import math
from random import randint

import mmh3
from my_bitmap import MyBitMap

class IFilter(ABC):
  def __init__(self, capacity: int, nhashes: int, name: str) -> None:
    self.nbits = math.ceil((nhashes * capacity) / math.log(2))
    self.bitmap = MyBitMap(self.nbits)
    self.nhashes = nhashes
    self.name = name

    self.seeds = [randint(0, 10000000) for _ in range(nhashes)]

  def _get_indices_for_element(self, element) -> list[int]:
    hashes: list[int] = [self._h(element, self.seeds[i]) for i in range(self.nhashes)]
    return [int(math.fabs(h)) % self.nbits for h in hashes]

  def _h(self, element, seed: int) -> None:
    return mmh3.hash(element, seed)

  def reset(self) -> None:
    self.bitmap.clear()

  @abstractmethod
  def insert(self, element) -> None:
    raise NotImplementedError

  @abstractmethod
  def lookup(self, element) -> bool:
    raise NotImplementedError
