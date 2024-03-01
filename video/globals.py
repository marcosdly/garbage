from typing_extensions import TypedDict


class InitConfigType(TypedDict):
  url: str
  host: str
  port: str


InitConfig = InitConfigType()  # type: ignore
