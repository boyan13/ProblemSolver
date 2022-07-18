# +====================================================================================================================+
# Libs
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout

# Internal
from GUI.Components.mixins import ExtendedQBoxAPIMixin
# +====================================================================================================================+


class ExtendedHBox(ExtendedQBoxAPIMixin, QHBoxLayout):
    pass


class ExtendedVBox(ExtendedQBoxAPIMixin, QVBoxLayout):
    pass
