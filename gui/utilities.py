# ----------------------------------------------------------------------------------------------------------------------
import typing
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout
# ----------------------------------------------------------------------------------------------------------------------


def nulled_layout(layout: typing.Union[QVBoxLayout, QHBoxLayout]):
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    return layout
