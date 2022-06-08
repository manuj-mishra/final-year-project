import csv
from random import random

import numpy as np
import pandas as pd

from lifelike.Population import Population
from lifelike.constants import CHROMOSOME_LEN
from util import binary

if __name__ == "__main__":
  for eval_step in (1, 5, 10):
    for max_step in np.logspace(0, 2, num=5):
      pop_size = 100
      elitism = 0.2
      mutation = 1 / CHROMOSOME_LEN
      epoch_n = 30
      hyperparams = {
        "max_step": max_step,
        "eval_step": eval_step
      }
      exp_name = f"exp_maxstep{max_step}_evalstep{eval_step}_multires"
      print(f"Running {exp_name}")
      rules = []
      conv_epochs = []
      num_visited = []
      best_rules = []
      best_fitnesses = []
      with open('lifelike/ics.npy', 'rb') as icfile:
        ics = np.load(icfile)
      with open('lifelike/goals.npy', 'rb') as goalfile:
        goals = np.load(goalfile)
      for goalarr in goals:
        binarrstr = ''.join(goalarr.astype(str))
        rules.append(int(binarrstr, 2))
        trueB = binary.ones(goalarr >> (CHROMOSOME_LEN // 2))
        smask = ((1 << ((CHROMOSOME_LEN // 2) + 1)) - 1)
        trueS = binary.ones(goalarr & smask)
        pop = Population(pop_size, elitism, mutation, trueB, trueS, ics, 'binary', hyperparams)
        counter = 0
        for _ in range(epoch_n):
          if pop.goal_found():
            break
          pop.iterate()
          counter += 1
        conv_epochs.append(counter)
        num_visited.append(len(pop.visited))
        best_rules.append(pop.inds[0].rstring)
        best_fitnesses.append(pop.best_fitness)

      df = pd.DataFrame({"rstring": rules,
                         "convtime": conv_epochs,
                         "visited": num_visited,
                         "bestfit": best_fitnesses,
                         "bestrule": best_rules})
      df.to_csv(f"./{exp_name}.csv")