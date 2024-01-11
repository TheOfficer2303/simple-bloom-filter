import metrohash

def get_mask(i: int):
  return (1 << i) -1

def get_alt_hash(i: int):
   return metrohash.hash64(i)

def next_power_of_2(size: int):
    return 1 if size == 0 else 2**(size - 1).bit_length()

def get_fingerprint(data: int):
  return data % 255 + 1

def get_alt_index(data: any, i1: int, power: int):
  mask = get_mask(power)
  hashed = get_alt_hash(data) & mask

  return (i1 & mask) ^ hashed

def get_index_and_fingerprint(data: any, power: int) -> tuple[int, int]:
  hashed_data = metrohash.hash64(data)
  hashed_data_int = int.from_bytes(hashed_data, byteorder='little')

  fp = get_fingerprint(hashed_data_int)
  i: int = (hashed_data_int >> 32) & get_mask(power)

  return i, fp
