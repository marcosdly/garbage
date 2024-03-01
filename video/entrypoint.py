from typing import Dict, Any
from video.globals import set_config


def main(**kw: Dict[str, Any]):
  set_config(**kw)

  from video.mainloop import mainloop

  mainloop()
