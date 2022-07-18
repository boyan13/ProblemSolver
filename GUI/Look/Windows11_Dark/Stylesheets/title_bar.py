
# +====================================================================================================================+
# Internal
from GUI.Look.Windows11_Dark import constants as const
# +====================================================================================================================+


stylesheet = f"""
    #WindowTitleBar {{
        background-color: {const.COLOR__HARD};
        color: {const.COLOR__TEXT};
    }}
    
    #WindowTitleBar QLabel {{
        color: {const.COLOR__TEXT};
        font-size: {const.FONT_SIZE_PX__TITLE}px;
    }}
    
    /*   Buttons   */
    
    #WindowTitleBar MinimizeButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    #WindowTitleBar MinimizeButton:hover {{
        background: {const.COLOR__HOVER__PRIMARY};
        color: {const.COLOR__TEXT};
    }}

    #WindowTitleBar FullscreenButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    #WindowTitleBar FullscreenButton:hover {{
        background: {const.COLOR__HOVER__PRIMARY};
        color: {const.COLOR__TEXT};
    }}
    
    #WindowTitleBar CloseButton {{
        background: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
        border-style: solid;
        border-top-right-radius: 7px;
        
        min-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        max-width: {const.DIMENSION__WINDOW_BUTTONS_WIDTH}px;
        min-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
        max-height: {const.DIMENSION__WINDOW_BUTTONS_HEIGHT}px;
    }}
    #WindowTitleBar CloseButton:hover {{
        background: {const.COLOR__DANGER};
        color: {const.COLOR__TEXT};
    }}
"""
