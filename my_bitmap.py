from __future__ import annotations

from array import array
from copy import copy

class MyBitMap():
  def __init__(self, number_of_bits: int) -> MyBitMap:
    number_of_bytes = (number_of_bits + 7) // 8

    self.BITMASK: list[int] = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]

    # array BAJTOVA
    self.bitmap: array[int] = array('B', [0 for _ in range(number_of_bytes)])

  def set(self, position: int) -> None:
    # position je mjesto bita
    self.bitmap[position // 8] |= self.BITMASK[position % 8]

  def reset(self, position: int) -> None:
    self.bitmap[position // 8] &= ~self.BITMASK[position % 8]

  def get(self, position: int) -> int:
    return int(self.bitmap[position // 8] & self.BITMASK[position % 8] != 0)

  def __str__(self) -> str:
    return "".join([("%s" % bin(x)[2:]).zfill(8) for x in self.bitmap[::-1]])
