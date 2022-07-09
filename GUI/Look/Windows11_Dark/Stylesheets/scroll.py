

# WIP / Unfinished


# area_stylesheet = f"""
#     QScrollArea {{
#         border: none;
#     }}
# """
#
# # There is no hover, so for now the scroll bar will not widen on hover like on Windows 11
# bar_stylesheet = f"""
#     QScrollBar {{
#         background: transparent;
#     }}
#     QScrollBar::horizontal {{
#         background-color: transparent;
#         min-height: 14px;
#         max-height: 14px;
#     }}
#     QScrollBar::vertical {{
#         background-color: transparent;
#         min-width: 14px;
#         max-width: 14px;
#     }}
# """
#
# handle_stylesheet = f"""
#     QScrollBar::handle {{
#         background-color: #999999;
#     }}
#     QScrollBar::handle:horizontal {{
#         margin: 4px 0px 4px 0px;
#         height: 10px;
#         border-width: 1px;
#         border-radius: 5px;
#     }}
#     QScrollBar::handle:vertical {{
#         margin: 0px 4px 0px 4px;
#         width: 10px;
#         border-width: 1px;
#         border-radius: 5px;
#     }}
# """
#
# arrows_stylesheet = f"""
# """
#
# stylesheet = area_stylesheet +\
#              bar_stylesheet +\
#              handle_stylesheet +\
#              arrows_stylesheet
