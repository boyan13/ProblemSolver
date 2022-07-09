# +====================================================================================================================+
# Internal
from GUI.Look.Windows11_Dark.Stylesheets import status_bar, view, forms, menu_bar, title_bar
# +====================================================================================================================+


extra_stylesheet = """
"""

Windows11_Dark_stylesheet = title_bar.stylesheet + \
                            menu_bar.stylesheet + \
                            view.stylesheet + \
                            status_bar.stylesheet + \
                            forms.stylesheet + \
                            extra_stylesheet
