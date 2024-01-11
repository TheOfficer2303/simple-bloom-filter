from copy import deepcopy
import math
import random
from typing import List
from bucket import Bucket
from cuckoo.util import get_alt_index, get_index_and_fingerprint, next_power_of_2
from filter import IFilter


class CuckooFilter(IFilter):
  def __init__(self, capacity: int, bucket_size = 4) -> None:
    self.bucket_size = bucket_size
    self.capacity = next_power_of_2(capacity) // bucket_size
    self.bucket_pow = int(math.log2(capacity))
    self.max_count = 500

    self.buckets: List[Bucket] = [Bucket() for _ in range(self.capacity)]


  def insert(self, element) -> bool:
    i1, fp = get_index_and_fingerprint(element, self.bucket_pow)
    if self._insert(fp, i1):
      return True

    i2 = get_alt_index(element, i1, self.bucket_pow)
    if self._insert(fp, i2):
      return True

    self._kick_and_insert(random.choice([i1, i2]))

  def _insert(self, element, index: int) -> bool:
    if self.buckets[index].insert(element):
      return True

    return False

  def _kick_and_insert(self, element, index: int) -> bool:
    for _ in range(self.max_count):
      bucket = self.buckets[index]

      victim = bucket[random.randint(0, self.bucket_size)]
      victim_alt_index = get_alt_index(bucket.get_fingerprint_index(victim))

      old = deepcopy(victim)
      victim = element

      if self._insert(old, victim_alt_index):
        return True

    return False


  def lookup(self, element) -> bool:
    return super().lookup(element)
