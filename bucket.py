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

  def get_fingerprint_index(self, fingerprint: str) -> int:
    for i, fp in enumerate(self.fingerprints):
      if fp == fingerprint:
        return i

    return -1
