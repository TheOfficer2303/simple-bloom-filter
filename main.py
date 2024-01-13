import random
import string
import time

from matplotlib import pyplot as plt
import numpy as np

from bloom import BloomFilter, CountingBloomFilter
from cuckoo.cuckoo import CuckooFilter
from filter import IFilter

ITERATIONS = 20
NUM_ELEMENTS = 10000
ELEMENT_SIZE = 3

def generate_data() -> list[str]:
  chars = string.ascii_lowercase
  unique_strings = set()

  while len(unique_strings) < NUM_ELEMENTS:
    random_string = ''.join(random.choice(chars) for _ in range(ELEMENT_SIZE))
    unique_strings.add(random_string)

  return list(unique_strings)

def plot(filter, it, lt):
  iterations = list(range(0, ITERATIONS))
  plt.plot(iterations, it, label='Insertion Time')
  plt.plot(iterations, lt, label='Lookup Time')
  plt.xlabel('Iteration')
  plt.ylabel('Time (ms)')
  plt.title(f'{filter.name} Filter Performance over 100 Iterations')
  plt.legend()
  plt.show()


def plot_lookup_time(l1, l2 , l3):
  iterations = list(range(0, ITERATIONS))

  plt.title(f"Filters Lookup Performance over {ITERATIONS} Iterations with {NUM_ELEMENTS} elements")
  plt.plot(iterations, l1, label="Bloom")
  plt.plot(iterations, l2, label="Counting")
  plt.plot(iterations, l3, label="Cuckoo")
  plt.xlabel("Iteration")
  plt.ylabel("Time (ms)")

  plt.legend()
  plt.show()

def test_effectiveness(filter: IFilter, wanna_plot = True):
  insertion_times = []
  lookup_times = []

  for _ in range(ITERATIONS):
    elements  = generate_data()

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
    print(f"Hits: {hits} / {len(elements)}")

    filter.reset()

  if wanna_plot:
    plot(filter, insertion_times, lookup_times)

  return lookup_times

def test_false_positive_rate(filter: IFilter):
  fp_rates = []

  for i in range(ITERATIONS):
    known_elements, test_elements  = [[''.join(random.choice(string.ascii_lowercase) for _ in range(ELEMENT_SIZE)) for _ in range(NUM_ELEMENTS)] for _ in range(2)]

    for el in known_elements:
      filter.insert(el)

    false_positives = 0
    for element in test_elements:
      if filter.lookup(element):
        if element not in known_elements:
          false_positives += 1
        else:
          test_elements.remove(element)

    false_positive_rate = false_positives / len(test_elements)
    fp_rates.append(false_positive_rate)
    print(f"False Positive Rate for {filter.name} in iteration {i}: {false_positive_rate}")
    filter.reset()

  avg = np.average(fp_rates)
  print(f"Average False Positive Rate for {filter.name}: {avg}")

  return avg

def test(filter: IFilter):
  return test_effectiveness(filter, False), test_false_positive_rate(filter)

def main():
  lookup_bloom, avg_fp_bloom = test(BloomFilter(NUM_ELEMENTS, nhashes=3))
  lookup_counting, avg_fp_counting = test(CountingBloomFilter(NUM_ELEMENTS, nhashes=3))
  lookup_cuckoo, avg_fp_cuckoo = test(CuckooFilter(NUM_ELEMENTS))

  print(avg_fp_bloom, avg_fp_counting, avg_fp_cuckoo)
  plot_lookup_time(lookup_bloom, lookup_counting, lookup_cuckoo)



if __name__ == "__main__":
  main()
