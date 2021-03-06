import glob
import os
import shutil

import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap

root = "."

def make_files_clustered(final_state, fname, rname):
  frame_folder = fname[:3] + "_frames"
  dirname = f"{root}/out/{rname}"
  if not os.path.exists(dirname):
    os.makedirs(dirname)
  frames = [Image.open(image) for image in sorted(glob.glob(f"{root}/temp/{frame_folder}/*.png"))]
  frames[0].save(f"{dirname}/{fname}.gif", format="GIF", append_images=frames[1:],
                 save_all=True, duration=50)
  frame_last = frames[-1]
  frame_last.save(f"{dirname}/{fname}.png")
  fname = f"{dirname}/{fname}.npy"
  with open(fname, 'wb') as f:
    np.save(f, final_state)


def create_conv_gif(rname):
  frame_folder = "conv_frames"
  dirname = f"{root}/out/{rname}"
  if not os.path.exists(dirname):
    os.makedirs(dirname)

  frames = [Image.open(image) for image in sorted(glob.glob(f"{root}/temp/{frame_folder}/*.png"))]
  frames[0].save(f"{dirname}/convergence.gif", format="GIF", append_images=frames[1:],
                 save_all=True, duration=200)

def make_files(final_state, fname, rname, clear=False):
  frame_folder = fname[:3] + "_frames"
  dirname = f"{root}/out/{rname}"

  dirs = ["gifs", "final_frames", "np_arrays"]
  if os.path.exists(dirname):
    if clear:
      shutil.rmtree(dirname)
      for dir in dirs:
        os.makedirs(f"{dirname}/{dir}")
  else:
    for dir in dirs:
      os.makedirs(f"{dirname}/{dir}")

  frames = [Image.open(image) for image in sorted(glob.glob(f"{root}/temp/{frame_folder}/*.png"))]
  frames[0].save(f"{dirname}/gifs/{fname}.gif", format="GIF", append_images=frames[1:],
                 save_all=True, duration=50)
  frame_last = frames[-1]
  frame_last.save(f"{dirname}/final_frames/{fname}.png")

  fname = f"{dirname}/np_arrays/{fname}.npy"
  with open(fname, 'wb') as f:
    np.save(f, final_state)




def init_image(width=500, height=500, dpi=10):
  fig = plt.figure(figsize=(width / dpi, height / dpi), dpi=dpi)
  ax = fig.add_subplot(111)
  return fig, ax


def save_image(M, i, ax, folder, cmap=ListedColormap(["w", "k", "y", "g", "r"]), dpi=10):
  im = ax.imshow(M, cmap=cmap, interpolation='nearest')
  plt.axis('off')
  plt.savefig('{:s}/{:s}/_img{:04d}.png'.format(root, folder, i), dpi=dpi)
  plt.cla()


def save_final_image(M, path, ax, cmap=ListedColormap(["w", "k", "y", "g", "r"]), dpi=10):
  im = ax.imshow(M, cmap=cmap, interpolation='nearest')
  plt.axis('off')
  plt.savefig(f'{root}/{path}', dpi=dpi)
  plt.cla()


def clear_temp_folders():
  parent = f"{root}/temp"
  dirs = next(os.walk(parent))[1]
  for dir in dirs:
    droot, _, files = next(os.walk(f"{parent}/{dir}"))
    for file in files:
      os.remove(os.path.join(droot, file))
