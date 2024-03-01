from typing import NamedTuple, cast, Tuple


class InitConfigType(NamedTuple):
  url: str
  host: str
  port: str
  size: Tuple[int, int]


InitConfig = cast(InitConfigType, None)


def set_config(**kw) -> None:
  global InitConfig
  InitConfig = InitConfigType(**kw)
