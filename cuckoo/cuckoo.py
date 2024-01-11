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
    self.bucket_pow = int(math.log2(self.capacity))
    self.max_count = 500

    self.buckets: List[Bucket] = [Bucket() for _ in range(self.capacity)]


  def insert(self, element) -> bool:
    i1, fp = get_index_and_fingerprint(element, self.bucket_pow)
    if self._insert(fp, i1):
      return True

    i2 = get_alt_index(fp, i1, self.bucket_pow)
    if self._insert(fp, i2):
      return True

    self._kick_and_insert(fp, random.choice([i1, i2]))

  def _insert(self, fp, index: int) -> bool:
    if self.buckets[index].insert(fp):
      return True

    return False

  def _kick_and_insert(self, fp, index: int) -> bool:
    for _ in range(self.max_count):
      bucket = self.buckets[index]

      victim_index_in_bucket = random.randint(0, self.bucket_size - 1)
      victim = bucket.fingerprints[victim_index_in_bucket]
      victim_alt_index = get_alt_index(victim, index, self.bucket_pow)

      bucket.fingerprints[victim_index_in_bucket] = fp

      if self._insert(victim, victim_alt_index):
        return True

    return False


  def lookup(self, element) -> bool:
    return super().lookup(element)
