import random
import string
import time

from matplotlib import pyplot as plt

from bloom import BloomFilter, CountingBloomFilter
from cuckoo.cuckoo import CuckooFilter
from filter import IFilter

ITERATIONS = 100

def plot(filter, it, lt):
  iterations = list(range(0, ITERATIONS))
  plt.plot(iterations, it, label='Insertion Time')
  plt.plot(iterations, lt, label='Lookup Time')
  plt.xlabel('Iteration')
  plt.ylabel('Time (ms)')
  plt.title(f'{filter.name} Filter Performance over 100 Iterations')
  plt.legend()
  plt.show()


def test_effectiveness(filter: IFilter, wanna_plot = True):
  insertion_times = []
  lookup_times = []

  for _ in range(ITERATIONS):
    elements  = [''.join(random.choice(string.ascii_lowercase) for _ in range(3)) for _ in range(1000)]

    insertion_start = time.time_ns()
    for el in elements:
      filter.insert(el)
    insertion_time = (time.time_ns() - insertion_start) / 10e3
    insertion_times.append(insertion_time)

    lookup_start = time.time_ns()
    hits = sum(filter.lookup(el) for el in elements)
    lookup_time = (time.time_ns() - lookup_start) / 10e3
    lookup_times.append(lookup_time)

    print(f"Insertion time for {filter.name}: {insertion_time:.2f} ms")
    print(f"Lookup time for {filter.name}: {lookup_time:.2f} ms")
    print(f"{hits} / {len(elements)}")

    filter.reset()

  if wanna_plot:
    plot(filter, insertion_times, lookup_times)

  return lookup_times

def test_bloom():
  bloom = BloomFilter(2885, 2)
  return test_effectiveness(bloom, False)

def test_counting():
  counting = CountingBloomFilter(2885, 2)
  return test_effectiveness(counting, False)

def test_cuckoo():
  cuckoo = CuckooFilter(capacity=1000)
  return test_effectiveness(cuckoo, False)

def main():
  lookup_times1 = test_bloom()
  lookup_times2 = test_counting()
  lookup_times3 = test_cuckoo()
  iterations = list(range(0, ITERATIONS))


  plt.title(f'Filters Lookup Performance over 100 Iterations')
  plt.plot(iterations, lookup_times1, label="Bloom")
  plt.plot(iterations, lookup_times2, label="Counting")
  plt.plot(iterations, lookup_times3, label="Cuckoo")
  plt.xlabel('Iteration')
  plt.ylabel('Time (ms)')

  plt.legend()
  plt.show()



if __name__ == "__main__":
  main()
