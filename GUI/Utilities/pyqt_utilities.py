# +====================================================================================================================+
# Pythonic
import typing

# Libs
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QGridLayout, QWidget, QScrollArea, QFormLayout
# +====================================================================================================================+


class AutoGridPos:

    def __init__(self, max_rows=None, max_cols=None):
        self.max_rows = max_rows
        self.max_cols = max_cols
        self.gen = self.__next()
        self.__row_count = 0
        self.__col_count = 0
        self._populate_new_row = None

    def next_pos(self):
        return self.gen.__next__()

    def __next(self):

        while True:
            if self._populate_new_row:
                for j in range(self.__col_count):
                    yield self.__row_count - 1, j
            else:
                for i in range(self.__row_count):
                    yield i, self.__col_count - 1

            if self.max_rows is not None and self.__row_count == self.max_rows:
                self.__col_count += 1
                self._populate_new_row = False

            elif self.max_cols is not None and self.__col_count == self.max_cols:
                self.__row_count += 1
                self._populate_new_row = True

            elif self.__row_count == self.__col_count:
                self.__col_count += 1
                self._populate_new_row = False

            else:
                self.__row_count += 1
                self._populate_new_row = True


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
