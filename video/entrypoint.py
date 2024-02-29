from video.globals import InitConfig, InitConfigType
from pyrsistent import freeze


def main(**kw: InitConfigType):
    InitConfig.update(kw.items())
    freeze(InitConfig)

    from video.mainloop import mainloop

    mainloop()
