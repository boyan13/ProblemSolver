# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


stylesheet = f"""
    Window TitleBar {{
        background-color: {const.COLOR__HARD};
        color: {const.COLOR__TEXT};
    }}
    
    Window TitleBar QLabel {{
        color: {const.COLOR__TEXT};
        font-size: {const.FONT_SIZE_PX__TITLE}px;
    }}
    
    /*   Buttons   */
    
    Window TitleBar MinimizeButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    Window TitleBar MinimizeButton:hover {{
        background: {const.COLOR__HOVER__PRIMARY};
        color: {const.COLOR__TEXT};
    }}

    Window TitleBar FullscreenButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    Window TitleBar FullscreenButton:hover {{
        background: {const.COLOR__HOVER__PRIMARY};
        color: {const.COLOR__TEXT};
    }}
    
    Window TitleBar CloseButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        border-top-right-radius: 9px;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    Window TitleBar CloseButton:hover {{
        background: {const.COLOR__DANGER};
        color: {const.COLOR__TEXT};
    }}
"""
