# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


# TODO: Figure out why the background-color of the Status Bar does not actually change?

stylesheet = f"""
    Window QStatusBar {{
        background-color: {const.COLOR__HARDER};
        color: {const.COLOR__TEXT};
    }}
"""
