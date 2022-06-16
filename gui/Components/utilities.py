# ----------------------------------------------------------------------------------------------------------------------
import typing
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget
# ----------------------------------------------------------------------------------------------------------------------


def nulled_layout(layout: typing.Union[QVBoxLayout, QHBoxLayout]):
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    return layout


def purge_layout(self, layout: typing.Union[QVBoxLayout, QHBoxLayout]):
    for i in reversed(range(layout.count())):
        item = layout.itemAt(i)
        if hasattr(item, 'widget'):
            item.widget().setParent(QWidget())
        elif hasattr(item, 'layout'):
            purge_layout(self, item.layout())
        else:
            layout.removeItem(item)
