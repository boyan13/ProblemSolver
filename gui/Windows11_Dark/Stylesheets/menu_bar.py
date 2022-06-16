# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


stylesheet = f"""
    Window QMenuBar {{
        font-size: {const.FONT_SIZE__MENU_BAR_ITEM}px;
        background: {const.COLOR__MENU_BAR};
    }}
    Window QMenuBar::item {{
        color: {const.COLOR__MENU_BAR_ITEM_TEXT};
        
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 5px;
        padding-bottom: 5px;
        
        border-radius: {const.DIMENSION__MENU_BAR_BORDER_RADIUS}px;
        
        margin-left: 4px;
        margin-right: 4px;
        margin-top: 4px;
        margin-bottom: 4px;
    }}
    /* selected means hover */
    Window QMenuBar::item:selected {{
        background: {const.COLOR__MENU_BAR_ITEM__HOVERED};
    }}
    Window QMenuBar::item:pressed {{
        background: {const.COLOR__MENU_BAR_ITEM__PRESSED};
    }}
    Window QMenuBar QMenu {{
        color: {const.COLOR__MENU_BAR_ITEM_TEXT};
        background: {const.COLOR__SUBMENU};
    }}
    Window QMenuBar QMenu::item {{
    }}
    Window QMenuBar QMenu::item:selected {{
        background: {const.COLOR__SUBMENU_ITEM__HOVERED};
    }}
    Window QMenuBar QMenu::item:pressed {{
        background: {const.COLOR__SUBMENU_ITEM__PRESSED};
    }}
"""
