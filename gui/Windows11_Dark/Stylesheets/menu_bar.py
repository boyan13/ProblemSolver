stylesheet = """

    Window QMenuBar {
        font-size: 16px;
        background: #21201f;
    }
    Window QMenuBar::item {
        color: white;
        padding-left: 10px;
        padding-right: 10px;
        padding-top: 5px;
        padding-bottom: 5px;
        border-radius: 6px;
        margin-left: 4px;
        margin-right: 4px;
        margin-top: 4px;
        margin-bottom: 4px;
    }
    Window QMenuBar::item:selected {
        background: #2e2d2b;
    }
    Window QMenuBar::item:pressed {
        background: #2a2927;
    }
    Window QMenuBar QMenu {
        color: white;
        background: #2e2d2b;
    }
    Window QMenuBar QMenu::item {
    }
    Window QMenuBar QMenu::item:selected {
        background: #383838;
    }
    Window QMenuBar QMenu::item:pressed {
        background: #343434;
    }

"""
