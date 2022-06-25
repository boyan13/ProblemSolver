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

form_title_offset = const.FONT_SIZE_PX__TEXT_BIG // 2 + const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL * 2

stylesheet_formgroup = f"""
    FormGroup {{
        border-style: solid;
        border-width: 2px;
        border-color: {const.COLOR__FORM_BUTTON_BORDER__DEFAULT};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};   
        
        margin-top: {form_title_offset}px;
        padding-top: {const.FONT_SIZE_PX__TEXT_BIG // 2}px;

        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT_BIG}px;
        font-family: "{const.FONT_FAMILY}";    
    }}

    FormGroup::title {{
        background-color: {const.COLOR__HARD};
        color: {const.COLOR__TEXT};

        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT_BIG}px;
        font-family: "{const.FONT_FAMILY}";
        
        top: {-form_title_offset}px;
        left: 10px;
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
    }}
"""

stylesheet_buttons = f"""
    FormButton {{
        background-color: {const.COLOR__FORM_BUTTON__DEFAULT};
        color: {const.COLOR__FORM_BUTTON_TEXT__DEFAULT};

        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
    
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FORM_BUTTON_BORDER__DEFAULT};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__FORM_INPUT_WIDGET_MIN_WIDTH};
        max-width: {const.DIMENSION__FORM_INPUT_WIDGET_MAX_WIDTH};
    }}
    FormButton::hover {{
        background-color: {const.COLOR__FORM_BUTTON__HOVERED};
        color: {const.COLOR__FORM_BUTTON_TEXT__HOVERED};
        border-color: {const.COLOR__FORM_BUTTON_BORDER__HOVERED};
    }}
    FormButton::pressed {{
        background-color: {const.COLOR__FORM_BUTTON__PRESSED};
        color: {const.COLOR__FORM_BUTTON_TEXT__PRESSED};
        border-color: {const.COLOR__FORM_BUTTON_BORDER__PRESSED};
    }}
    
    FormRadioButton {{
        background-color: transparent;
        color: {const.COLOR__FORM_FIELD_TEXT__DEFAULT};
        
        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
    }}
    
    FormRadioGroupBox {{
        background-color: {const.COLOR__FORM_FIELD__DEFAULT};
        color: {const.COLOR__FORM_FIELD_TEXT__DEFAULT};
        
        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FORM_FIELD_BORDERS__DEFAULT};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__FORM_INPUT_WIDGET_MIN_WIDTH};
        max-width: {const.DIMENSION__FORM_INPUT_WIDGET_MAX_WIDTH};
    }}
"""

stylesheet_lineedits = f"""
    FormLineEdit {{
        background-color: {const.COLOR__FORM_FIELD__DEFAULT};
        color: {const.COLOR__FORM_FIELD_TEXT__DEFAULT};
        
        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FORM_FIELD_BORDERS__DEFAULT};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};    
        border-bottom-width: 2px;
        border-bottom-color: {const.COLOR__FORM_FIELD_ACCENT__DEFAULT};
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__FORM_INPUT_WIDGET_MIN_WIDTH};
        max-width: {const.DIMENSION__FORM_INPUT_WIDGET_MAX_WIDTH};
    }}
    FormLineEdit::hover {{
        background-color: {const.COLOR__FORM_FIELD__HOVERED};
        color: {const.COLOR__FORM_FIELD_TEXT__HOVERED};
        border-color: {const.COLOR__FORM_FIELD_BORDERS__HOVERED};
        border-bottom-color: {const.COLOR__FORM_FIELD_ACCENT__HOVERED};
    }}
    FormLineEdit::focus {{
        background-color: {const.COLOR__FORM_FIELD__FOCUSED};
        color: {const.COLOR__FORM_FIELD_TEXT__FOCUSED};
        border-color: {const.COLOR__FORM_FIELD_BORDERS__FOCUSED};
        border-bottom-color: {const.COLOR__FORM_FIELD_ACCENT__FOCUSED};
    }}
    FormLineEdit QString {{
        color: green;
    }} 
"""

stylesheet_lists = f"""
    FormListWidget {{
        background-color: {const.COLOR__FORM_FIELD__DEFAULT};
        color: {const.COLOR__FORM_FIELD_TEXT__DEFAULT};
        
        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";    
        
        border-style: solid;
        border-width: 1px;
        border-color: {const.COLOR__FORM_FIELD_BORDERS__DEFAULT};
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS};
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        
        min-width: {const.DIMENSION__FORM_DISPLAY_WIDGET_MIN_WIDTH};
        max-width: {const.DIMENSION__FORM_DISPLAY_WIDGET_MAX_WIDTH};
        max-height: 9999px;
    }}
"""

stylesheet_labels = f"""
    
    #FormLabel {{
        background-color: transparent;
        color: {const.COLOR__TEXT};
        
        font-weight: {const.FONT_WEIGHT__FORM__PRIMARY};
        font-style: {const.FONT_STYLE};
        font-size: {const.FONT_SIZE_PX__TEXT}px;
        font-family: "{const.FONT_FAMILY}";   
        
        padding-left: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-right: {const.DIMENSION__FORM_ELEMENT_PADDING_HORIZONTAL}px;
        padding-top: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
        padding-bottom: {const.DIMENSION__FORM_ELEMENT_PADDING_VERTICAL}px;
    }}
"""

stylesheet = stylesheet_formgroup + \
             stylesheet_buttons + \
             stylesheet_lineedits + \
             stylesheet_lists + \
             stylesheet_labels
