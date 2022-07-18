# +====================================================================================================================+
# Internal
from GUI.Look.Windows11_Dark import constants as const
# +====================================================================================================================+


stylesheet = f"""
    #WindowStatusBar {{
        background-color: {const.COLOR__HARDER};
        color: {const.COLOR__TEXT};
        
    }}
    #WindowStatusBar::item {{
        border: none;
    }}
"""
