import random

import numpy as np
from collections import deque, defaultdict

from generator.media import intmap, save_image, init_image


def near(x, y, n):
  adj = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
  return set((i, j) for (i, j) in adj if 0 <= i < n and 0 <= j < n)


def get_regions(M, folder="reg_frames"):
  # cells = {(x,y):region}
  # regions = {region:set((x1, y1), ... , (xn, yn))}

  n = M.shape[0]

  cells = dict()
  regions = defaultdict(set)

  spaces = set()
  for i in range(n):
    for j in range(n):
      if M[i][j] == 0:
        spaces.add((i, j))

  regnum = 1
  start = (n - 1, 0)
  r1 = bfs(start, M, n)
  M_copy = M.copy()
  for cell in r1:
    M_copy[cell[0], cell[1]] = 3
    cells[cell] = regnum
    regions[regnum].add(cell)
  spaces.difference_update(r1)

  ax = init_image()
  reg = r1
  save_image(M_copy, regnum, ax, folder=folder)
  n_iter = 0
  #TODO: Remove hard cap on n_iter
  while spaces and n_iter < 300:
    regnum += 1
    start = spaces.pop()
    for cell in reg:
      M_copy[cell[0], cell[1]] = 2
    save_image(M_copy, regnum, ax, folder=folder)
    reg = bfs(start, M, n)
    for cell in reg:
      M_copy[cell[0], cell[1]] = 3
      cells[cell] = regnum
      regions[regnum].add(cell)
    spaces.difference_update(reg)
    n_iter += 1

  return cells, regions, M, n


def bfs(start, M, n):
  q = deque([start])
  visited = set()
  while q:
    curr = q.popleft()
    visited.add(curr)
    adj = near(curr[0], curr[1], n)
    for x, y in adj:
      if M[x, y] == 0 and (x, y) not in visited:
        q.append((x, y))
  return visited


def region_merge(regions, cells, M, n, folder="merge_frames"):
  curr = regions[1]
  ax = init_image()
  for i in range(300):
    fringe = set().union(*(near(c[0], c[1], n) for c in curr)) - curr

    if (0, n - 1) in fringe:
      save_image(M, i, ax, folder=folder)
      return M

    M_copy = M.copy()
    for x, y in curr:
      M_copy[x, y] = 2
    for x, y in fringe:
      M_copy[x, y] = 3
    save_image(M_copy, i, ax, folder=folder)

    cands = []
    for f in fringe:
      zeros = set(z for z in near(f[0], f[1], n) if M[z[0], z[1]] == 0)
      if len(zeros - curr) > 0:
        cands.append(f)
    if len(cands) > 0:
      cx, cy = random.choice(cands)
      curr.add((cx, cy))
      M[cx, cy] = 0
      new_regs = [cells[around] for around in near(cx, cy, n) if around in cells]
      curr = curr.union(*(regions[r] for r in new_regs))
    #TODO: Else (what if no valid candidates)
  return M
