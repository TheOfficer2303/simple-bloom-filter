import sys
from typing import List

from bitmap import BitMap
from bloom import BloomFilter, CountingBloomFilter
from cuckoo.cuckoo import CuckooFilter
from filter import IFilter


def test_effectiveness(filter: IFilter, elements: List[str]):
  for el in elements:
    filter.insert(el)

  hits = sum(filter.lookup(el) for el in elements)
  print(f"{hits} / {len(elements)}")

def test_bloom():
  elements = ["abc", "dsa", "223", "sad", "fvc", "2ds", "sss", "ddd", "aaa", "ccc"]

  bloom = BloomFilter(8, 1)

  test_effectiveness(bloom, elements)

def test_counting():
  counting = CountingBloomFilter(8, 2)
  counting.insert("a")
  counting.insert("c")
  counting.insert("d")
  counting.insert("e")
  counting.insert("f")

  counting.delete("a")
  assert counting.lookup("a") == False

def test_cuckoo():
  cuckoo = CuckooFilter(capacity=10)
  elements = ["abc", "dsa", "223", "sad", "fvc", "2ds", "sss", "ddd", "aaa", "ccc"]

  test_effectiveness(cuckoo, elements)

def main():
  test_bloom()
  test_cuckoo()


if __name__ == "__main__":
  main()
