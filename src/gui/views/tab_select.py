import tkinter as t
from typing import Callable, NamedTuple
from collections.abc import Sequence


class ViewOption(NamedTuple):
    name: str
    widget: t.Widget


class ViewSelector(t.Frame):
    def __init__(
        self,
        parent: t.Widget,
        views: Sequence[ViewOption],
        default: str,
    ) -> None:
        super().__init__(parent)
        self.parent = parent
        self.master = parent
        self.views = views
        self.default = default
        self.grid_configure(column=0, row=0, sticky=t.W)

        for name, widget in views:
            btn = t.Button(
                self,
                text=name,
                name=name,
                command=self.on_pressed(name),
                state=("disabled" if name == default else "active"),
            )
            btn.pack(expand=True, side="left")

        self.on_pressed(default)()

    def on_pressed(self, view_name: str) -> Callable[[], None]:
        def func() -> None:
            for child_name, child in self.children.items():
                if child_name != view_name:
                    child["state"] = "active"
                    getattr(self.views, child_name).widget.grid_remove()
                else:
                    child["state"] = "disabled"
                    getattr(self.views, child_name).widget.grid()

        return func
