from filter import IFilter

class BloomFilter(IFilter):
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


class CountingBloomFilter(IFilter):
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
