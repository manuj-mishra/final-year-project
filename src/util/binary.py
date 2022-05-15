from lifelike.constants import CHROMOSOME_LEN


def ones(rstring):
  ixs = []
  for i in range(CHROMOSOME_LEN // 2, 0, -1):
    if rstring & 1:
      ixs.append(i)
    rstring >>= 1
  return sorted(ixs)