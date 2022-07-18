# +====================================================================================================================+
# Pythonic
import typing
import contextlib

# Libs
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QFormLayout
# +====================================================================================================================+


def null_layout(layout: typing.Union[QVBoxLayout, QHBoxLayout, QGridLayout]):
    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    return layout


def purge_layout(layout: typing.Union[QVBoxLayout, QHBoxLayout]):

    for i in reversed(range(layout.count())):
        item = layout.takeAt(i)

        if hasattr(item, 'widget') and item.widget() is not None:
            item.widget().setParent(None)

        elif hasattr(item, 'layout') and item.layout() is not None:
            purge_layout(item.layout())

        else:
            layout.removeItem(item)

    QWidget().setLayout(layout)


def wrap_in_scroll_area(widget: QWidget, parent=None):
    sarea = QScrollArea(parent)
    sarea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    sarea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
    sarea.setWidget(widget)
    sarea.setWidgetResizable(True)
    return sarea


def set_label_object_name(self, lay: QFormLayout, widget: QWidget, name: str):
    label = lay.labelForField(widget)
    label.setObjectName(name)
