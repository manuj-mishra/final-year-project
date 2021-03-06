import random

from maze.maze_ca import MazeCA

SUCCESS_RATE = 0.8


class Rulestring:
  def __init__(self, rstring=None):
    if rstring is None:
      rstring = random.randint(0, 2 ** 16 - 1)

    self._rstring = rstring
    self.b = self._ones(rstring >> 8)
    self.s = self._ones(rstring)

  @property
  def rstring(self):
    return self._rstring

  def get_rstring(self):
    return format(self._rstring, 'b').zfill(16)

  @rstring.setter
  def rstring(self, rstring):
    self.b = self._ones(rstring >> 8)
    self.s = self._ones(rstring)
    self._rstring = rstring

  def _ones(self, rstring):
    ixs = []
    for i in range(8, 0, -1):
      if rstring & 1:
        ixs.append(i)
      rstring >>= 1
    return sorted(ixs)

  def mutate(self, p):
    mask = 0
    for _ in range(16):
      if random.random() < p:
        mask |= 1
      mask <<= 1

    mask >>= 1
    self.rstring = self.rstring ^ mask
    return self.rstring

  def evaluate(self, n_iters):
    path_lens = []
    dead_ends = []
    reachables = []
    n_success = 0
    for _ in range(n_iters):
      ca = MazeCA(self.b, self.s)
      success = ca.run()
      if success:
        dead_end, path_len, reachable = ca.metrics()
        dead_ends.append(dead_end)
        path_lens.append(path_len)
        reachables.append(reachable)
        n_success += 1

    if n_success < SUCCESS_RATE * n_iters:
      return 0, 0, 0

    return sum(dead_ends) / n_success, sum(path_lens) / n_success, sum(reachables) / n_success
