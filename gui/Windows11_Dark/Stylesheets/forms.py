# ----------------------------------------------------------------------------------------------------------------------
from gui.Windows11_Dark import constants as const
# ----------------------------------------------------------------------------------------------------------------------


# Note to self from docs:
# 'font' statement is equivalent to specifying font-family, font-size, font-style, and/or font-weight, and
# the syntax is: "font: [weight] {style} {size} {family};"

# font: {const.FONT_WEIGHT} {const.FONT_STYLE} {const.FONT_SIZE_PX__TEXT}px "{const.FONT_FAMILY}";

# font-weight: {const.FONT_WEIGHT};
# font-style: {const.FONT_STYLE};
# font-size: {const.FONT_SIZE_PX__TEXT}px;
# font-family: "{const.FONT_FAMILY}";

stylesheet = f"""
    #FormFieldLabel {{
        background-color: transparent;
        color: {const.COLOR__TEXT};
        
        font-weight: {const.FONT_WEIGHT};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";   
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
    }}
    
    FormLabel {{
        background-color: transparent;
        color: {const.COLOR__TEXT};

        font-weight: {const.FONT_WEIGHT};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT_BIG}px;
        font-family: "{const.FONT_FAMILY}";    
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
    }}
    
    FormButton {{
        background-color: {const.COLOR__SOFTEST};
        color: {const.COLOR__TEXT};

        font-weight: {const.FONT_WEIGHT};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
    
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FIELD_BORDERS_IDLE};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__BUTTON_MIN_WIDTH};
        max-width: {const.DIMENSION__BUTTON_MAX_WIDTH};
    }}
    
    FormLineEdit {{
        background-color: {const.COLOR__FIELD_IDLE};
        color: {const.COLOR__TEXT};
        
        font-weight: {const.FONT_WEIGHT};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FIELD_BORDERS_IDLE};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};    
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__LINE_EDIT_MIN_WIDTH};
        max-width: {const.DIMENSION__LINE_EDIT_MAX_WIDTH};
    }}
    
    FormListWidget {{
        background-color: {const.COLOR__FIELD_IDLE};
        color: {const.COLOR__TEXT};
        
        font-weight: {const.FONT_WEIGHT};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FIELD_BORDERS_IDLE};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};
        
        padding-left: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__BUTTON_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__BUTTON_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__LIST_MIN_WIDTH};
        max-width: {const.DIMENSION__LIST_MAX_WIDTH};
    }}
"""
