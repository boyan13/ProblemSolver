
# +====================================================================================================================+
# Internal
from GUI.Look.Windows11_Dark import constants as const
# +====================================================================================================================+


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

    FormBox {{
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
    FormBox::title {{
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
    CheckButton {{
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
    }}
    CheckButton::hover {{
        background-color: {const.COLOR__FORM_BUTTON__HOVERED};
        color: {const.COLOR__FORM_BUTTON_TEXT__HOVERED};
        border-color: {const.COLOR__FORM_BUTTON_BORDER__HOVERED};
    }}
    CheckButton::pressed {{
        background-color: {const.COLOR__FORM_BUTTON__PRESSED};
        color: {const.COLOR__FORM_BUTTON_TEXT__PRESSED};
        border-color: {const.COLOR__FORM_BUTTON_BORDER__PRESSED};
    }}

    RadioButton {{
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
    
    ColumnRadioGroup, GridRadioGroup {{
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
    }}
"""

stylesheet_lineedits = f"""
    LineEdit {{
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
    }}
    LineEdit::hover {{
        background-color: {const.COLOR__FORM_FIELD__HOVERED};
        color: {const.COLOR__FORM_FIELD_TEXT__HOVERED};
        border-color: {const.COLOR__FORM_FIELD_BORDERS__HOVERED};
        border-bottom-color: {const.COLOR__FORM_FIELD_ACCENT__HOVERED};
    }}
    LineEdit::focus {{
        background-color: {const.COLOR__FORM_FIELD__FOCUSED};
        color: {const.COLOR__FORM_FIELD_TEXT__FOCUSED};
        border-color: {const.COLOR__FORM_FIELD_BORDERS__FOCUSED};
        border-bottom-color: {const.COLOR__FORM_FIELD_ACCENT__FOCUSED};
    }}
"""

stylesheet_comboboxes = f"""
    ComboBox {{
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
    }}
    ComboBox::hover {{
        background-color: {const.COLOR__FORM_BUTTON__HOVERED};
        color: {const.COLOR__FORM_BUTTON_TEXT__HOVERED};
        border-color: {const.COLOR__FORM_BUTTON_BORDER__HOVERED};
    }}
    ComboBox::drop-down {{
    }}
    ComboBox::drop-down:button {{
        image: url(resources/down_arrow_white.svg);
        top: 8px;
        right: 6px;
        width: 10px;
        height: 10px;
        border-radius: {const.DIMENSION__BUTTONS_BORDER_RADIUS}px;
    }}
"""

stylesheet_lists = f"""
    ListWidget {{
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
    }}
"""

stylesheet_labels = f"""
    
    #FormLabel, Label {{
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
    
    #FormLabelMuted, LabelMuted {{
        background-color: transparent;
        color: {const.COLOR__TEXT_MUTED};
        
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
             stylesheet_comboboxes + \
             stylesheet_lists + \
             stylesheet_labels
