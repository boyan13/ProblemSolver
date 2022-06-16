# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


stylesheet = f"""
    Window QMenuBar {{
        font-size: {const.FONT_SIZE_PX__MENU_ITEM}px;
        background: {const.COLOR__HARD};
    }}
    Window QMenuBar::item {{
        color: {const.COLOR__TEXT};
        
        padding-left: {const.DIMENSION__MENU_BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__MENU_BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__MENU_BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__MENU_BUTTON_PADDING_VERTICAL}px;
        
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS}px;
        
        margin-left: 4px;
        margin-right: 4px;
        margin-top: 4px;
        margin-bottom: 4px;
    }}
    /* selected means hover */
    Window QMenuBar::item:selected {{
        background: {const.COLOR__HOVER__PRIMARY};
    }}
    Window QMenuBar::item:pressed {{
        background: {const.COLOR__PRESSED_PRIMARY};
    }}
    Window QMenuBar QMenu {{
        color: {const.COLOR__TEXT};
        background: {const.COLOR__SOFTEST};
    }}
    Window QMenuBar QMenu::item {{
    }}
    Window QMenuBar QMenu::item:selected {{
        background: {const.COLOR__HOVER__SECONDARY};
    }}
    Window QMenuBar QMenu::item:pressed {{
        background: {const.COLOR__PRESSED_SECONDARY};
    }}
"""
