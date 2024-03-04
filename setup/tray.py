from datetime import datetime
from pathlib import Path
from pystray import Icon, MenuItem
from setup.process import Manager as manager
from PIL import Image

_state_times = 0


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
  global _state_times
  if manager.proc.is_alive():
    manager.stop()
    manager.proc.join()
    return

  try:
    manager.proc.start()
    _state_times += 1
    tray.update_menu()
  except AssertionError:
    # trying to start twice
    return


def on_quit(tray, item: MenuItem):
  manager.stop()
  tray.stop()


def set_today(tray, plus: bool | None = None):
  global _state_times
  path = Path("state/tray/today.txt")
  if not path.is_file():
    path.touch()
  with path.open("r+t") as today:
    try:
      content = today.read().strip()
      if content == "":
        today.write(f"{datetime.now().date()} 0")
        return "Today: 0"

      date, times = content.split(" ")
      times = int(times)
      t = datetime.fromisoformat(date)

      if t > datetime.now():
        t = datetime.fromisoformat(datetime.now().date())
        times = 0

      if _state_times <= times:
        _state_times = times

      today.seek(0)
      today.truncate()
      today.write(f"{t.date()} {_state_times}")
      return f"Today: {_state_times}"
    except:  # noqa
      return "Today: Error"


state_item = MenuItem(
  set_tooltip, state_action, default=True, visible=True, enabled=False
)

quit_item = MenuItem("Quit", on_quit)

start_item = MenuItem(set_start, on_start)

today_item = MenuItem(set_today, None, visible=True, enabled=False)

tray = Icon(
  "test",
  Image.open("setup/tray.ico"),
  menu=(state_item, today_item, start_item, quit_item),
)
