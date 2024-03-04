from pystray import Icon, MenuItem
from setup.process import Manager as manager
from PIL import Image


def set_tooltip(tray):
  try:
    if manager.proc.is_alive():
      return "Running"
    return "Stopped"
  except:  # noqa
    return ""


def state_action(tray, item: MenuItem):
  tray.notify(set_tooltip(tray))


def set_start(tray):
  if manager.proc.is_alive():
    return "Stop"
  return "Start"


def on_start(tray):
  if manager.proc.is_alive():
    manager.stop()
    manager.proc.join()
    return

  try:
    manager.proc.start()
  except AssertionError:
    # trying to start twice
    return


def on_quit(tray, item: MenuItem):
  manager.stop()
  tray.stop()


state_item = MenuItem(
  set_tooltip, state_action, default=True, visible=True, enabled=False
)

quit_item = MenuItem("Quit", on_quit)

start_item = MenuItem(set_start, on_start)

tray = Icon(
  "test", Image.open("setup/tray.ico"), menu=(state_item, start_item, quit_item)
)
