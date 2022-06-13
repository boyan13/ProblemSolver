from gui.Windows11_Dark import constants as const

stylesheet = f"""
    Window TitleBar {{
        color: white;
        background-color: #202020;
    }}
    
    Window TitleBar QLabel {{
        color: white;
    }}
    
    /*   Buttons   */
    
    Window TitleBar MinimizeButton {{
        background: #202020;
        color: white;
        
        border-style: solid;
        
        min-width: 45;
        max-width: 45;
        min-height: 30;
        max-height: 30;
    }}
    Window TitleBar MinimizeButton:hover {{
        background: #2e2d2b;
    }}

    Window TitleBar FullscreenButton {{
        background: #202020;
        color: white;
        
        border-style: solid;
        
        min-width: 45;
        max-width: 45;
        min-height: 30;
        max-height: 30;
    }}
    Window TitleBar FullscreenButton:hover {{
        background: #2e2d2b;
    }}
    
    Window TitleBar CloseButton {{
        background: #202020;
        color: white;
        
        border-style: solid;
        border-top-right-radius: 9px;
        
        min-width: 45;
        max-width: 45;
        min-height: 30;
        max-height: 30;
    }}
    Window TitleBar CloseButton:hover {{
        background: red;
    }}
    Window TitleBar QLabel {{
        font-size: 13px;
    }}
"""
