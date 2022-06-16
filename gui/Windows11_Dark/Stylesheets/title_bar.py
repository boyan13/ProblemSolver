# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


stylesheet = f"""
    Window TitleBar {{
        background-color: {const.COLOR__TITLE_BAR};
        color: {const.COLOR__TITLE_BAR_BUTTON_TEXT};
    }}
    
    Window TitleBar QLabel {{
        color: {const.COLOR__TITLE_BAR_TITLE_TEXT};
        font-size: {const.FONT_SIZE__TITLE_BAR_TITLE}px;
    }}
    
    /*   Buttons   */
    
    Window TitleBar MinimizeButton {{
        background: {const.COLOR__TITLE_BAR_BUTTON};
        color: {const.COLOR__TITLE_BAR_BUTTON_TEXT};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__TITLE_BAR_BUTTON_WIDTH}px;
        max-width: {const.DIMENSION__TITLE_BAR_BUTTON_WIDTH}px;
        min-height: {const.DIMENSION__TITLE_BAR_BUTTON_HEIGHT}px;
        max-height: {const.DIMENSION__TITLE_BAR_BUTTON_HEIGHT}px;
    }}
    Window TitleBar MinimizeButton:hover {{
        background: {const.COLOR__TITLE_BAR_BUTTON__HOVERED};
        color: {const.COLOR__TITLE_BAR_BUTTON_TEXT__HOVERED};
    }}

    Window TitleBar FullscreenButton {{
        background: {const.COLOR__TITLE_BAR_BUTTON};
        color: {const.COLOR__TITLE_BAR_BUTTON_TEXT};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__TITLE_BAR_BUTTON_WIDTH}px;
        max-width: {const.DIMENSION__TITLE_BAR_BUTTON_WIDTH}px;
        min-height: {const.DIMENSION__TITLE_BAR_BUTTON_HEIGHT}px;
        max-height: {const.DIMENSION__TITLE_BAR_BUTTON_HEIGHT}px;
    }}
    Window TitleBar FullscreenButton:hover {{
        background: {const.COLOR__TITLE_BAR_BUTTON__HOVERED};
        color: {const.COLOR__TITLE_BAR_BUTTON_TEXT__HOVERED};
    }}
    
    Window TitleBar CloseButton {{
        background: {const.COLOR__TITLE_BAR_CLOSE_BUTTON};
        color: {const.COLOR__TITLE_BAR_CLOSE_BUTTON_TEXT};
        
        border-style: solid;
        border-top-right-radius: 9px;
        
        min-width: {const.DIMENSION__TITLE_BAR_CLOSE_BUTTON_WIDTH}px;
        max-width: {const.DIMENSION__TITLE_BAR_CLOSE_BUTTON_WIDTH}px;
        min-height: {const.DIMENSION__TITLE_BAR_CLOSE_BUTTON_HEIGHT}px;
        max-height: {const.DIMENSION__TITLE_BAR_CLOSE_BUTTON_HEIGHT}px;
    }}
    Window TitleBar CloseButton:hover {{
        background: {const.COLOR__TITLE_BAR_CLOSE_BUTTON__HOVERED};
        color: {const.COLOR__TITLE_BAR_CLOSE_BUTTON_TEXT__HOVERED};
    }}
"""
