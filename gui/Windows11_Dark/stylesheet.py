from gui.Windows11_Dark.Stylesheets import window, title_bar, menu_bar, status_bar, view, forms

extra_stylesheet = """
    Window {
        background-color green;
        border-top-left-radius: 50px;
        border-bottom-left-radius:50px;
        border-top-right-radius: 50px;
        border-bottom-right-radius: 50px;
    }
"""

Windows11_Dark_stylesheet = window.stylesheet + \
                            title_bar.stylesheet + \
                            menu_bar.stylesheet + \
                            view.stylesheet + \
                            status_bar.stylesheet + \
                            forms.stylesheet + \
                            extra_stylesheet