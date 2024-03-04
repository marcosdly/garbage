import os


def init_dirs():
  dirs = ["state/tray"]
  for d in dirs:
    os.makedirs(d, exist_ok=True)


def app_setup():
  init_dirs()
