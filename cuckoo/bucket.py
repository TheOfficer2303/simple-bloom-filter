class Bucket:
  def __init__(self) -> None:
    self.size = 4
    self.fingerprints = [None for _ in range(self.size)]

  def insert(self, fingerprint: str) -> bool:
    for i, fp in enumerate(self.fingerprints):
      if fp is None:
        self.fingerprints[i] = fingerprint
        return True

    return False

  def delete(self, fingerprint: str) -> bool:
    for i, fp in enumerate(self.fingerprints):
      if fp == fingerprint:
        self.fingerprints[i] = None
        return True

    return False

  def get_fingerprint_index(self, fingerprint: int) -> int:
    for i, fp in enumerate(self.fingerprints):
      if fp == fingerprint:
        return i

    return -1

  def reset(self):
    for i, fp in enumerate(self.fingerprints):
      self.fingerprints[i] = None

  def __getitem__(self, index):
    return self.fingerprints[index]

  def __setitem__(self, index, value):
    self.fingerprints[index] = value
